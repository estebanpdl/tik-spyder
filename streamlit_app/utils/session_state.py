# -*- coding: utf-8 -*-

# import modules
import streamlit as st
import time

def initialize_session_state():
    """Initialize session state variables"""
    if 'output_dir' not in st.session_state:
        timestamp = int(time.time())
        st.session_state.output_dir = f'./tikspyder-data/{timestamp}'