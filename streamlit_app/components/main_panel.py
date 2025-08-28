# -*- coding: utf-8 -*-

# import modules
import streamlit as st

# local imports
from dataclasses import dataclass
from ..utils.file_browser import select_directory

@dataclass
class CollectionConfig:
    """Configuration for collection settings"""
    download_videos: bool = True
    use_tor: bool = False
    max_workers: int = 5
    output_dir: str = ''

def render_main_panel():
    """Render main content panels and return configuration"""
    
    # Main Content Area - Better organized panels
    st.markdown("## ⚙️ Collection Settings")
    
    # Download Settings Panel
    with st.container():
        st.markdown("### 📥 Download & Processing Settings")
        st.markdown("")  # Add consistent spacing
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown("**📹 Download Videos**")
            download_videos = st.toggle(
                "Enable video downloads", 
                value=True,
                help="Download TikTok videos to local storage",
                label_visibility="collapsed"
            )
            
        with col2:
            st.markdown("**🔒 Use Tor Network**")
            use_tor = st.toggle(
                "Enable Tor for downloads", 
                help="Enable Tor for anonymous downloads",
                label_visibility="collapsed"
            )
            
        with col3:
            max_workers = st.number_input(
                '⚡ **Concurrent Workers**',
                min_value=1,
                max_value=20,
                value=5,
                help='Number of concurrent download workers'
            )
    
    st.markdown("---")
    
    # Output Configuration Panel  
    with st.container():
        st.markdown("### 📂 Output Configuration")
        
        # Properly aligned output directory input and browse button
        col1, col2 = st.columns([6, 1])
        
        with col1:
            output_dir = st.text_input(
                '**Output Directory**',
                value=st.session_state.output_dir,
                help='Directory where all collected data will be saved',
                placeholder='Enter output directory path...',
                label_visibility="visible"
            )
            if output_dir != st.session_state.output_dir:
                st.session_state.output_dir = output_dir
        
        with col2:
            # Add spacing to align button with input field
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button('📁', help="Browse for directory", use_container_width=True):
                path = select_directory()
                if path:
                    st.session_state.output_dir = path
                    st.rerun()
    
    st.markdown("---")
    
    # Centered Action Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        start_collection = st.button(
            '🚀 **Start Data Collection**', 
            use_container_width=True,
            type="primary"
        )
    
    return CollectionConfig(
        download_videos=download_videos,
        use_tor=use_tor,
        max_workers=max_workers,
        output_dir=st.session_state.output_dir
    ), start_collection