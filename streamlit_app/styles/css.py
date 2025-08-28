# -*- coding: utf-8 -*-

# import modules
import streamlit as st

def load_css():
    """Load custom CSS for TikTok-inspired theme"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for TikTok color scheme */
    :root {
        --primary-color: #000000;
        --secondary-color: #ff0050;
        --accent-color: #25f4ee;
        --background-dark: #161823;
        --background-light: #1e2139;
        --text-primary: #ffffff;
        --text-secondary: #a0a0a0;
        --success-color: #00ff88;
        --warning-color: #ffb800;
        --error-color: #ff3366;
    }
    
    /* Main app styling */
    .main .block-container {
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #161823 0%, #1e2139 100%);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, var(--secondary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(255, 0, 80, 0.3);
    }
    
    /* Card styling */
    .stCard {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, var(--secondary-color), var(--accent-color));
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 80, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 0, 80, 0.5);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #161823 0%, #1e2139 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Enhanced input field styling - work with theme */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid var(--accent-color);
    }
    
    /* Select box styling - work with theme */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* Date input styling - work with theme */
    .stDateInput input {
        border-radius: 10px;
    }
    
    /* Number input styling - work with theme */
    .stNumberInput input {
        border-radius: 10px;
    }
    
    /* Metrics styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--secondary-color), var(--accent-color));
        border-radius: 10px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, var(--secondary-color), var(--accent-color));
    }
    
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .status-success {
        background: rgba(0, 255, 136, 0.2);
        color: var(--success-color);
        border: 1px solid var(--success-color);
    }
    
    .status-warning {
        background: rgba(255, 184, 0, 0.2);
        color: var(--warning-color);
        border: 1px solid var(--warning-color);
    }
    
    .status-error {
        background: rgba(255, 51, 102, 0.2);
        color: var(--error-color);
        border: 1px solid var(--error-color);
    }
    
    /* Animation keyframes */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Hide default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def create_status_badge(text, status_type):
    """Create a status badge with specified type"""
    return f'<span class="status-badge status-{status_type}">{text}</span>'