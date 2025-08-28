# -*- coding: utf-8 -*-

# import modules
import streamlit as st
import time

# local imports
from ..styles.css import create_status_badge

def create_progress_tracker():
    """Create and return progress tracking components"""
    # Create status container
    status_container = st.container()
    
    with status_container:
        st.markdown("### 🔄 Collection Progress")
        
        # Create progress indicators
        overall_progress = st.progress(0)
        status_text = st.empty()
        step_container = st.container()
        
        # Collection steps with icons and descriptions
        steps = [
            ("🔍", "Initializing search parameters..."),
            ("📡", "Collecting search results..."),
            ("🖼️", "Gathering image thumbnails..."),
            ("🚀", "Running Apify integration..."),
            ("📁", "Generating data files..."),
            ("📹", "Downloading videos..."),
            ("🎞️", "Extracting keyframes..."),
            ("✅", "Collection complete!")
        ]
        
        step_progress = {}
        for i, (icon, desc) in enumerate(steps):
            step_progress[i] = step_container.empty()
    
    return overall_progress, status_text, step_progress, steps

def update_progress(step_num, overall_progress, status_text, step_progress, steps, message=None, progress_value=None):
    """Update progress indicators"""
    if step_num < len(steps):
        icon, desc = steps[step_num]
        step_progress[step_num].markdown(f"{icon} {desc}")
    
    if message:
        status_text.markdown(create_status_badge(message, "warning"), unsafe_allow_html=True)
    
    if progress_value is not None:
        overall_progress.progress(progress_value)
    
    time.sleep(0.1)  # Allow UI to update

def mark_step_complete(step_num, step_progress, message):
    """Mark a step as completed"""
    step_progress[step_num].markdown(f"✅ {message}")