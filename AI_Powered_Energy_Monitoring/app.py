import streamlit as st
import home
import solar
import wind
import hydro
import biomass
from utils import load_css

# Initialize session state for variables
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "current_index" not in st.session_state:  # Initialize 'current_index' here
    st.session_state.current_index = 0

# Set page configuration
# st.set_page_config(
#     page_title="Renewable Energy Solutions",
#     page_icon="🌿",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Load custom CSS
load_css()



# Create a dictionary for page navigation
pages = {
    "Home": {"id": "home", "icon": "🏠", "module": home},
    "Solar Energy": {"id": "solar", "icon": "☀️", "module": solar},
    "Wind Energy": {"id": "wind", "icon": "🌬️", "module": wind},
    "Adavanced Solar Calculator": {"id": "hydro", "icon": "💧", "module": hydro},
    "Energy Forecasting": {"id": "biomass", "icon": "🌱", "module": biomass}
}

# Sidebar navigation
st.sidebar.markdown("# 🌿")  # Add icon emoji above Navigation text
st.sidebar.title("Navigation")

# Create navigation boxes
st.sidebar.markdown('<div class="nav-box-container">', unsafe_allow_html=True)
for page_name, page_info in pages.items():
    page_id = page_info["id"]
    icon = page_info["icon"]
    
    # Create clickable box for each navigation option
    if st.sidebar.button(f"{icon} {page_name}", key=f"nav_{page_id}"):
        st.session_state.current_page = page_id

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Add some sidebar information
st.sidebar.markdown("---")
st.sidebar.info("""
### About
This application showcases various renewable energy technologies and their potential impact.

© 2025 Eco Energy Solutions
""")

# Initialize session state for navigation if it doesn't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Display the selected page
current_page = st.session_state.current_page
for page_name, page_info in pages.items():
    if page_info["id"] == current_page:
        page_info["module"].show_page()
        break