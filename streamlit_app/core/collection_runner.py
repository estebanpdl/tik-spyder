# -*- coding: utf-8 -*-

# import modules
import streamlit as st
import asyncio
import time

# import submodules
from concurrent.futures import ThreadPoolExecutor

# local imports
from data_collectors import TikTokDataCollector
from media_handlers import VideoDownloader
from utils import create_output_data_path
from ..components.progress import create_progress_tracker, update_progress, \
    mark_step_complete
from ..styles.css import create_status_badge
from .keyframes_processor import extract_keyframes_sync

def build_args_dict(search_config, apify_config, collection_config, config_attrs):
    """Build arguments dictionary for collection"""
    args = {
        'q': search_config.query,
        'user': search_config.user,
        'tag': search_config.tag,
        'google_domain': search_config.google_domain,
        'gl': search_config.gl,
        'hl': search_config.hl,
        'cr': search_config.cr,
        'lr': search_config.lr,
        'safe': search_config.safe,
        'depth': search_config.depth,
        'before': search_config.before_date.strftime('%Y-%m-%d') if search_config.before_date else None,
        'after': search_config.after_date.strftime('%Y-%m-%d') if search_config.after_date else None,
        'download': collection_config.download_videos,
        'use_tor': collection_config.use_tor,
        'max_workers': collection_config.max_workers,
        'output': collection_config.output_dir,
        'apify': apify_config.use_apify,
        'number_of_results': apify_config.number_of_results
    }
    
    # Add Apify-specific arguments if enabled
    if apify_config.use_apify:
        args.update({
            'oldest_post_date': apify_config.oldest_post_date.strftime('%Y-%m-%d') if apify_config.oldest_post_date else None,
            'newest_post_date': apify_config.newest_post_date.strftime('%Y-%m-%d') if apify_config.newest_post_date else None
        })
    
    # Merge configuration attributes with user arguments
    args = {**args, **config_attrs}
    
    return args

def validate_input(search_config):
    """Validate search input"""
    if not search_config.query and not search_config.user and not search_config.tag:
        st.error('🚨 Please enter a search term, username, or hashtag to continue!')
        return False
    return True

def run_collection(search_config, apify_config, collection_config, config_attrs):
    """Enhanced collection function with better progress tracking and feedback"""
    
    # Build arguments
    args = build_args_dict(search_config, apify_config, collection_config, config_attrs)
    
    # Create progress tracker
    overall_progress, status_text, step_progress, steps = create_progress_tracker()
    
    def run_collection_thread():
        """Run collection in separate thread with own event loop"""
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Create collector in this thread
            collector = TikTokDataCollector(args=args)
            
            # Execute the main collection process
            collector.collect_search_data()
            
            # Generate files
            collector.generate_data_files()
            
            # Get collected videos for download
            collected_videos = collector.get_collected_videos() if args['download'] else []
            
            return collector, collected_videos
            
        finally:
            loop.close()
    
    try:
        # Create output directory
        create_output_data_path(args['output'])
        
        # Step 1: Initialize
        update_progress(0, overall_progress, status_text, step_progress, steps, progress_value=10)
        
        # Step 2: Start data collection process
        update_progress(1, overall_progress, status_text, step_progress, steps, "Searching...", 25)
        
        # Step 3: Show image collection
        update_progress(2, overall_progress, status_text, step_progress, steps, progress_value=35)
        
        # Step 4: Show Apify preparation
        if args['apify']:
            update_progress(3, overall_progress, status_text, step_progress, steps, "Preparing Apify...", 45)
        else:
            step_progress[3].markdown(f"⏭️ Apify integration skipped")
            overall_progress.progress(45)
            time.sleep(0.1)
        
        # Run collection in separate thread to avoid asyncio conflicts
        with ThreadPoolExecutor() as executor:
            future = executor.submit(run_collection_thread)
            collector, collected_videos = future.result()
        
        # Mark data collection steps as complete
        mark_step_complete(1, step_progress, "Search results collected")
        mark_step_complete(2, step_progress, "Image thumbnails gathered")
        if args['apify']:
            mark_step_complete(3, step_progress, "Apify integration completed")
        
        overall_progress.progress(65)
        
        # Step 5: Generate files (already done in thread)
        update_progress(4, overall_progress, status_text, step_progress, steps, "Generating Files...", 75)
        mark_step_complete(4, step_progress, "Data files generated")
        
        # Step 6: Download videos
        if args['download']:
            update_progress(5, overall_progress, status_text, step_progress, steps, "Downloading...", 80)
            
            if collected_videos:
                st.info(f'📹 Found {len(collected_videos)} videos to download')
                
                downloader = VideoDownloader(
                    output=args['output'],
                    use_tor=args['use_tor']
                )
                downloader.start_download(
                    urls=collected_videos,
                    max_workers=args['max_workers']
                )
                
                mark_step_complete(5, step_progress, f"{len(collected_videos)} videos downloaded")
                
                # Step 7: Extract keyframes
                update_progress(6, overall_progress, status_text, step_progress, steps, "Extracting Keyframes...", 90)
                
                # Extract keyframes directly
                try:
                    extract_keyframes_sync(args['output'], args['max_workers'])
                    mark_step_complete(6, step_progress, "Keyframes extracted")
                except Exception as e:
                    step_progress[6].markdown(f"⚠️ Keyframe extraction failed: {str(e)}")
                    
            else:
                mark_step_complete(5, step_progress, "No new videos to download")
                step_progress[6].markdown(f"⏭️ Keyframe extraction skipped (no videos)")
        else:
            mark_step_complete(5, step_progress, "Video download disabled")
            step_progress[6].markdown(f"⏭️ Keyframe extraction skipped (download disabled)")
        
        # Step 8: Complete
        overall_progress.progress(100)
        update_progress(7, overall_progress, status_text, step_progress, steps)
        status_text.markdown(create_status_badge("Success", "success"), unsafe_allow_html=True)
        
        # Success message with results
        st.success('🎉 Collection completed successfully!')
        
        # Show output location
        st.metric("📂 Output Location", args['output'])
        
        # Show file explorer link
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 1rem; background: rgba(0, 255, 136, 0.1); border-radius: 10px; border-left: 4px solid var(--success-color);">
            <strong>📁 Results saved to:</strong><br>
            <code>{args['output']}</code>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        status_text.markdown(create_status_badge("Error", "error"), unsafe_allow_html=True)
        st.error(f'❌ An error occurred during collection: {str(e)}')
        st.exception(e)