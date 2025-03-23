import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def load_css():
    """Load custom CSS for styling the application."""
    st.markdown("""
    <style>
        .main {
            background-color: #e8e8e8;  /* Light grey background */
        }
        .energy-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border-left: 5px solid;
        }
        .solar-card {
            border-left-color: #ffcc00;
        }
        .wind-card {
            border-left-color: #00ccff;
        }
        .hydro-card {
            border-left-color: #0066ff;
        }
        .biomass-card {
            border-left-color: #33cc33;
        }
        .card-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .sidebar .css-1d391kg {
            padding-top: 2rem;
        }
        /* Navigation boxes styling */
        .nav-box-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 10px;
        }
        .stButton > button {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            text-align: left;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
            display: block;
            border: none;
        }
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
    </style>
    """, unsafe_allow_html=True)

def generate_demo_data(energy_type):
    """Generate simulation data for energy production."""
    np.random.seed(42)  # For reproducibility
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    if energy_type == "solar":
        # Solar produces more in summer
        base = np.array([40, 50, 70, 85, 95, 100, 105, 100, 85, 65, 45, 35])
    elif energy_type == "wind":
        # Wind varies seasonally
        base = np.array([90, 85, 80, 70, 60, 55, 60, 70, 85, 95, 100, 95])
    elif energy_type == "hydro":
        # Hydro depends on rainfall/snowmelt
        base = np.array([60, 65, 85, 100, 95, 80, 70, 65, 60, 70, 80, 75])
    else:  # biomass
        # Biomass is relatively constant
        base = np.array([75, 75, 80, 85, 85, 80, 80, 80, 85, 85, 80, 75])
    
    # Add some noise
    data = base + np.random.normal(0, 5, 12)
    
    return pd.DataFrame({
        'Month': months,
        'Energy Output (kWh)': data,
        'Efficiency (%)': data / 1.2
    })

def create_production_chart(data, color):
    """Create a production chart with the given color."""
    fig = px.line(data, x='Month', y='Energy Output (kWh)', markers=True)
    fig.update_traces(line_color=color, line_width=3)
    return fig