# -*- coding: utf-8 -*-

# import modules
import streamlit as st

# import submodules
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class SearchConfig:
    """Configuration for search parameters"""
    query: Optional[str] = None
    user: Optional[str] = None
    tag: Optional[str] = None
    after_date: Optional[date] = None
    before_date: Optional[date] = None
    google_domain: str = 'google.com'
    gl: Optional[str] = None
    hl: Optional[str] = None
    cr: Optional[str] = None
    lr: Optional[str] = None
    safe: str = 'active'
    depth: int = 3

@dataclass
class ApifyConfig:
    """Configuration for Apify integration"""
    use_apify: bool = False
    number_of_results: int = 25
    oldest_post_date: Optional[date] = None
    newest_post_date: Optional[date] = None

def render_sidebar():
    """Render sidebar components and return configuration"""
    with st.sidebar:
        st.markdown("### 🎯 Search Configuration")
        st.markdown("")  # Add consistent spacing
        
        # Search Type Selection
        search_tab = st.radio(
            "**Search Type**",
            ["🔍 Keyword", "👤 User Profile", "🏷️ Hashtag"],
            horizontal=True
        )
        
        st.markdown("")  # Add spacing after radio buttons
        
        # Search input based on type
        query = user = tag = None
        
        if search_tab == "🔍 Keyword":
            query = st.text_input(
                'Search Keywords',
                placeholder='Enter keywords to search for...',
                help='Search for TikTok content using keywords'
            )
        elif search_tab == "👤 User Profile":
            user = st.text_input(
                'TikTok Username',
                placeholder='username (without @)',
                help='Enter TikTok username without @ symbol'
            )
        else:  # Hashtag search
            tag = st.text_input(
                'Hashtag',
                placeholder='hashtag (with or without #)',
                help='Enter hashtag with or without # symbol'
            )
        
        st.markdown("")  # Add spacing before divider
        st.markdown("---")
        st.markdown("")  # Add spacing after divider
        
        # Date Filters Section
        st.markdown("### 📅 Date Filters")
        st.markdown("")  # Add consistent spacing
        col1, col2 = st.columns(2)
        with col1:
            after_date = st.date_input(
                'After Date',
                value=None,
                help='Posts after this date'
            )
        with col2:
            before_date = st.date_input(
                'Before Date', 
                value=None,
                help='Posts before this date'
            )
        
        st.markdown("")  # Add spacing before divider
        st.markdown("---")
        st.markdown("")  # Add spacing after divider
        
        # Apify Integration Section
        st.markdown("### 🚀 Apify Integration")
        st.markdown("")  # Add consistent spacing
        
        use_apify = st.toggle(
            "**Enable Apify**", 
            help="Enhanced data collection with Apify"
        )
        
        st.markdown("")  # Add spacing after toggle
        
        if use_apify:
            number_of_results = st.number_input(
                'Results Count',
                min_value=1,
                max_value=1000,
                value=25,
                help='Number of results to collect'
            )
            
            st.markdown("")  # Add spacing before subsection
            st.markdown("**Apify Date Filters**")
            st.markdown("")  # Add spacing after subsection title
            
            col1, col2 = st.columns(2)
            with col1:
                oldest_post_date = st.date_input(
                    'Oldest Post',
                    help='Oldest post date'
                )
            with col2:
                newest_post_date = st.date_input(
                    'Newest Post',
                    help='Newest post date'
                )
        else:
            number_of_results = 25
            oldest_post_date = None
            newest_post_date = None
        
        st.markdown("---")
        
        # Advanced Search Options
        with st.expander("⚙️ Advanced Search Options"):
            st.markdown("**Google Search Settings**")
            
            # Domain setting (full width)
            google_domain = st.text_input(
                'Domain',
                value='google.com',
                help='e.g., google.com, google.co.uk'
            )
            
            # Country and Language settings (2 columns)
            col1, col2 = st.columns(2)
            with col1:
                gl = st.text_input(
                    'Country Code (GL)', 
                    help='e.g., us, uk, de',
                    placeholder='us'
                )
                cr = st.text_input(
                    'Country Restriction', 
                    help='Restrict to specific countries',
                    placeholder='countryUS'
                )
            with col2:
                hl = st.text_input(
                    'Language Code (HL)', 
                    help='e.g., en, es, fr',
                    placeholder='en'
                )
                lr = st.text_input(
                    'Language Restriction', 
                    help='Restrict to specific languages',
                    placeholder='lang_en'
                )
            
            # Search settings (2 columns)
            col3, col4 = st.columns(2)
            with col3:
                safe = st.selectbox(
                    'Safe Search',
                    options=['active', 'off'],
                    index=0,
                    help='Adult content filter'
                )
            with col4:
                depth = st.slider(
                    'Search Depth',
                    min_value=1,
                    max_value=10,
                    value=3,
                    help='Related content iterations'
                )
    
    # Return configuration objects
    search_config = SearchConfig(
        query=query,
        user=user,
        tag=tag,
        after_date=after_date,
        before_date=before_date,
        google_domain=google_domain,
        gl=gl if gl else None,
        hl=hl if hl else None,
        cr=cr if cr else None,
        lr=lr if lr else None,
        safe=safe,
        depth=depth
    )
    
    apify_config = ApifyConfig(
        use_apify=use_apify,
        number_of_results=number_of_results,
        oldest_post_date=oldest_post_date,
        newest_post_date=newest_post_date
    )
    
    return search_config, apify_config