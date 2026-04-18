"""
Custom CSS for Inventory System
Soft, bright, elegant theme with subtle gradations
Inspired by nature colors: soft greens, blues, and peachy tones
"""

def get_theme_css_vars(theme_name='sage'):
    """Get CSS variables for selected theme"""
    from utils.constants import THEME_OPTIONS
    
    theme = THEME_OPTIONS.get(theme_name, THEME_OPTIONS['sage'])
    
    # Create lighter/darker variants
    primary_light = theme['primary_light']
    primary = theme['primary']
    primary_dark = theme['primary_dark']
    secondary_light = theme['secondary_light']
    secondary = theme['secondary']
    
    # Determine text color based on theme
    is_dark_theme = theme_name == 'abyss'
    text_dark = theme.get('nav_text', '#2C3E50') if is_dark_theme else '#2C3E50'
    text_light = '#B0B0B0' if is_dark_theme else '#7F8C8D'
    bg_main = '#0A0E27' if is_dark_theme else '#FAFBFC'
    bg_secondary = '#151932' if is_dark_theme else '#F0F4F8'
    border_color = '#2D3561' if is_dark_theme else '#E8EAED'
    card_bg = '#1A1A2E' if is_dark_theme else '#FFFFFF'
    
    return f"""
    :root {{
        --primary-soft: {primary_light};
        --primary-light: {primary_light};
        --primary: {primary};
        --primary-medium: {primary};
        --primary-dark: {primary_dark};
        
        --secondary-soft: {secondary_light};
        --secondary-light: {secondary_light};
        --secondary: {secondary};
        --secondary-medium: {secondary};
        
        --accent-pink: #F8BBD0;
        --accent-orange: #FFE0B2;
        --accent-purple: #E1BEE7;
        
        --text-dark: {text_dark};
        --text-light: {text_light};
        --border-light: {border_color};
        --bg-soft: {bg_main};
        --bg-secondary: {bg_secondary};
        --card-bg: {card_bg};
        
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}"""

def inject_custom_css(theme_name='sage'):
    """Inject custom CSS for inventory system UI"""
    import streamlit as st
    
    theme_vars = get_theme_css_vars(theme_name)
    from utils.constants import THEME_OPTIONS
    theme = THEME_OPTIONS.get(theme_name, THEME_OPTIONS['sage'])
    
    css = f"""
    <style>
    /* ================================================================
       ROOT VARIABLES & THEME SETUP
       ================================================================ */
    {theme_vars}
    
    /* ================================================================
       ANIMATIONS
       ================================================================ */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes scaleIn {{
        from {{
            opacity: 0;
            transform: scale(0.95);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}
    
    /* ================================================================
       GENERAL STYLING
       ================================================================ */
    html, body, [data-testid="stAppViewContainer"] {{
        background: {theme['gradient_bg']};
        color: var(--text-dark);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* ================================================================
       SIDEBAR
       ================================================================ */
    [data-testid="stSidebar"] {{
        background: {theme['gradient_bg']};
        border-right: 1px solid var(--border-light);
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
        animation: fadeInUp 0.6s ease-out;
    }}
    
    /* ================================================================
       HEADER & TITLE
       ================================================================ */
    h1, h2, h3 {{
        color: var(--text-dark);
        font-weight: 700;
        animation: fadeInUp 0.5s ease-out;
    }}
    
    h1 {{
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-medium) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }}
    
    /* ================================================================
       BUTTONS
       ================================================================ */
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-medium) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: 0 2px 8px rgba(165, 214, 167, 0.25);
        animation: slideDown 0.4s ease-out;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, var(--primary-medium) 0%, var(--primary-dark) 100%);
        box-shadow: 0 4px 12px rgba(165, 214, 167, 0.4);
        transform: translateY(-2px);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(165, 214, 167, 0.25);
    }}
    
    /* Primary Buttons */
    [data-testid="stButton"] > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-medium) 100%);
    }}
    
    /* Secondary Buttons */
    [data-testid="stButton"] > button[kind="secondary"] {{
        background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-medium) 100%);
        color: white;
    }}
    
    /* ================================================================
       TABS
       ================================================================ */
    [data-testid="stTabs"] [role="tablist"] {{
        border-bottom: 2px solid var(--border-light);
        gap: 0;
    }}
    
    [data-testid="stTabs"] button[role="tab"] {{
        padding: 12px 24px;
        border: none;
        background: transparent;
        color: var(--text-light);
        font-weight: 600;
        border-bottom: 3px solid transparent;
        transition: var(--transition);
    }}
    
    [data-testid="stTabs"] button[role="tab"]:hover {{
        color: var(--primary-dark);
        background: rgba(165, 214, 167, 0.1);
    }}
    
    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {{
        color: var(--primary-dark);
        background: rgba(165, 214, 167, 0.1);
        border-bottom-color: var(--primary-dark);
    }}
    
    /* ================================================================
       INPUT FIELDS
       ================================================================ */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select,
    .stTextArea textarea {{
        border: 1.5px solid var(--border-light) !important;
        border-radius: 6px !important;
        background-color: var(--card-bg) !important;
        color: var(--text-dark) !important;
        transition: var(--transition) !important;
        padding: 8px 12px !important;
        font-size: 14px !important;
    }}
    
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stSelectbox select:focus,
    .stTextArea textarea:focus {{
        border-color: var(--primary-dark) !important;
        box-shadow: 0 0 0 3px rgba(165, 214, 167, 0.15) !important;
        outline: none !important;
    }}
    
    .stTextInput input::placeholder {{
        color: var(--text-light) !important;
    }}
    
    /* ================================================================
       CARDS & CONTAINERS
       ================================================================ */
    .streamlit-container {{
        background: transparent;
    }}
    
    [data-testid="stVerticalBlock"] > [style*="flex-direction"] {{
        animation: fadeInUp 0.4s ease-out;
    }}
    
    /* ================================================================
       EXPANDER
       ================================================================ */
    [data-testid="stExpander"] details > summary {{
        background: linear-gradient(135deg, var(--primary-soft) 0%, var(--secondary-soft) 100%);
        border: 1px solid var(--border-light);
        border-radius: 6px;
        padding: 12px 16px !important;
        font-weight: 600;
        color: var(--text-dark);
        transition: var(--transition);
        cursor: pointer;
    }}
    
    [data-testid="stExpander"] details > summary:hover {{
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary-light) 100%);
    }}
    
    [data-testid="stExpander"] details[open] > summary {{
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
    }}
    
    /* ================================================================
       METRIC/STAT BOXES
       ================================================================ */
    [data-testid="stMetricValue"] {{
        color: var(--primary-dark) !important;
        font-weight: 700 !important;
    }}
    
    [data-testid="stMetric"] {{
        background: linear-gradient(135deg, var(--primary-soft) 0%, rgba(227, 242, 253, 0.5) 100%);
        padding: 16px;
        border-radius: 8px;
        border: 1px solid var(--border-light);
        animation: scaleIn 0.4s ease-out;
    }}
    
    /* ================================================================
       RADIO & CHECKBOX
       ================================================================ */
    .stRadio > label {{
        cursor: pointer;
        transition: var(--transition);
        padding: 8px 12px;
        border-radius: 6px;
        color: var(--text-dark) !important;
        font-weight: 500;
    }}
    
    .stRadio > label:hover {{
        background: rgba(165, 214, 167, 0.1);
    }}
    
    .stCheckbox > label {{
        cursor: pointer;
        transition: var(--transition);
        padding: 8px 12px;
        border-radius: 6px;
        color: var(--text-dark) !important;
        font-weight: 500;
    }}
    
    .stCheckbox > label:hover {{
        background: rgba(165, 214, 167, 0.1);
    }}
    
    /* ================================================================
       DATAFRAME/TABLE
       ================================================================ */
    [data-testid="stDataFrame"] {{
        border: 1px solid var(--border-light);
        border-radius: 6px;
        overflow: hidden;
    }}
    
    [data-testid="stDataFrame"] th {{
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 12px !important;
    }}
    
    [data-testid="stDataFrame"] tr:hover {{
        background: rgba(165, 214, 167, 0.1) !important;
    }}
    
    [data-testid="stDataFrame"] td {{
        padding: 10px 12px !important;
        border-color: var(--border-light) !important;
    }}
    
    /* ================================================================
       ALERTS & MESSAGES
       ================================================================ */
    .stAlert {{
        border-radius: 6px;
        border: 1px solid transparent;
        animation: slideDown 0.4s ease-out;
    }}
    
    .stSuccess {{
        background: linear-gradient(135deg, rgba(102, 187, 106, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%) !important;
        border-left: 4px solid #66BB6A !important;
    }}
    
    .stWarning {{
        background: linear-gradient(135deg, rgba(255, 152, 0, 0.1) 0%, rgba(255, 193, 7, 0.05) 100%) !important;
        border-left: 4px solid #FFA726 !important;
    }}
    
    .stError {{
        background: linear-gradient(135deg, rgba(239, 83, 80, 0.1) 0%, rgba(244, 67, 54, 0.05) 100%) !important;
        border-left: 4px solid #EF5350 !important;
    }}
    
    .stInfo {{
        background: linear-gradient(135deg, rgba(66, 165, 245, 0.1) 0%, rgba(25, 103, 210, 0.05) 100%) !important;
        border-left: 4px solid #42A5F5 !important;
    }}
    
    /* ================================================================
       FILE UPLOADER
       ================================================================ */
    [data-testid="stFileUploadDropzone"] {{
        border: 2px dashed var(--primary-medium) !important;
        border-radius: 8px !important;
        background: linear-gradient(135deg, rgba(165, 214, 167, 0.05) 0%, rgba(227, 242, 253, 0.05) 100%) !important;
        padding: 24px !important;
        transition: var(--transition) !important;
    }}
    
    [data-testid="stFileUploadDropzone"]:hover {{
        border-color: var(--primary-dark) !important;
        background: linear-gradient(135deg, rgba(165, 214, 167, 0.1) 0%, rgba(227, 242, 253, 0.1) 100%) !important;
    }}
    
    /* ================================================================
       DIVIDER
       ================================================================ */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-light), transparent);
        margin: 20px 0;
    }}
    
    /* ================================================================
       MARKDOWN TEXT
       ================================================================ */
    [data-testid="stMarkdownContainer"] {{
        animation: fadeIn 0.4s ease-out;
    }}
    
    [data-testid="stMarkdownContainer"] strong {{
        color: var(--primary-dark);
        font-weight: 700;
    }}
    
    [data-testid="stMarkdownContainer"] em {{
        color: var(--text-light);
    }}
    
    /* ================================================================
       RESPONSIVE ADJUSTMENTS
       ================================================================ */
    @media (max-width: 640px) {{
        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 20px; }}
        h3 {{ font-size: 16px; }}
        
        .stButton > button {{
            width: 100%;
            padding: 12px 16px;
        }}
        
        [data-testid="stTabs"] button[role="tab"] {{
            padding: 10px 12px;
            font-size: 12px;
        }}
    }}
    
    /* ================================================================
       SCROLLBAR STYLING
       ================================================================ */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: transparent;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: var(--primary);
        border-radius: 4px;
        transition: var(--transition);
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--primary-dark);
    }}
    
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# REALTIME STATISTICS FUNCTIONS
# ============================================================================

def init_stats_cache():
    """Initialize statistics cache in session state"""
    import streamlit as st
    
    if 'stats_cache' not in st.session_state:
        st.session_state.stats_cache = {
            'total_items': 0,
            'total_value': 0,
            'total_equipment': 0,
            'last_update': None,
            'is_stale': True
        }


def calculate_realtime_stats():
    """Calculate realtime statistics optimally from managers"""
    import streamlit as st
    
    try:
        equipment_manager = st.session_state.equipment_manager
        all_equipment = equipment_manager.get_all_equipment()
        
        # Calculate totals efficiently
        total_items = 0
        total_value = 0
        total_equipment = len(all_equipment)
        
        for eq in all_equipment:
            try:
                qty = float(eq.get('jumlah', 0))
                value = float(eq.get('harga_keseluruhan', 0))
                total_items += qty
                total_value += value
            except (ValueError, TypeError):
                continue
        
        # Update cache
        st.session_state.stats_cache = {
            'total_items': int(total_items),
            'total_value': total_value,
            'total_equipment': total_equipment,
            'last_update': datetime.now().isoformat(),
            'is_stale': False
        }
        
        return st.session_state.stats_cache
    
    except Exception as e:
        print(f"Error calculating stats: {e}")
        return st.session_state.stats_cache


def get_cached_stats():
    """Get statistics from cache, recalculate if stale"""
    import streamlit as st
    
    init_stats_cache()
    
    if st.session_state.stats_cache.get('is_stale', True):
        return calculate_realtime_stats()
    
    return st.session_state.stats_cache


def mark_stats_stale():
    """Mark stats cache as stale to trigger recalculation"""
    import streamlit as st
    
    init_stats_cache()
    st.session_state.stats_cache['is_stale'] = True


def refresh_stats_immediately():
    """Immediately refresh statistics (used after add/update/delete)"""
    import streamlit as st
    
    mark_stats_stale()
    return calculate_realtime_stats()


# ============================================================================
# IMPORT DATETIME FOR STATS
# ============================================================================

from datetime import datetime
