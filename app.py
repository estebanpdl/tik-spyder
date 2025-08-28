# -*- coding: utf-8 -*-

# import modules
import streamlit as st
import os

# local imports
from streamlit_app.styles.css import load_css
from streamlit_app.utils.session_state import initialize_session_state
from streamlit_app.components.sidebar import render_sidebar
from streamlit_app.components.main_panel import render_main_panel
from streamlit_app.core.collection_runner import run_collection, validate_input
from utils import get_config_attrs, get_project_root

# Configure Streamlit page
st.set_page_config(
    page_title="TikSpyder - TikTok Data Collection",
    page_icon="🕷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set theme programmatically to dark
st._config.set_option('theme.base', 'dark')
st._config.set_option('theme.backgroundColor', '#0e1117')
st._config.set_option('theme.secondaryBackgroundColor', '#262730')
st._config.set_option('theme.textColor', '#ffffff')

def main():
    """Main application entry point"""
    # Load styling
    load_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Get project configuration
    project_root = get_project_root()
    config_path = os.path.join(project_root, 'config')
    config_attrs = get_config_attrs(config_path)
    
    # Main header
    st.markdown('<h1 class="main-header">🕷️ TikSpyder</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: var(--text-secondary); font-size: 1.2rem; margin-bottom: 2rem;">Advanced TikTok Data Collection</p>', unsafe_allow_html=True)
    
    # Render UI components
    search_config, apify_config = render_sidebar()
    collection_config, start_collection = render_main_panel()
    
    # Handle collection start
    if start_collection:
        if validate_input(search_config):
            run_collection(search_config, apify_config, collection_config, config_attrs)

if __name__ == '__main__':
    main()