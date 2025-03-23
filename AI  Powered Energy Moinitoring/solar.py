import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import joblib
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Set page configuration
st.set_page_config(
    page_title="Solar Panel Efficiency Monitor",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .good-efficiency {color: green; font-weight: bold;}
    .moderate-efficiency {color: orange; font-weight: bold;}
    .poor-efficiency {color: red; font-weight: bold;}
    .stHeader {background-color: #0c3866 !important;}
    .stSidebar {background-color: #f0f2f6;}
    .metric-card {
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    .panel-table {
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 10px;
        margin-bottom: 10px;
    }
    .good-table {
        background-color: rgba(0, 128, 0, 0.1);
        border: 1px solid green;
    }
    .moderate-table {
        background-color: rgba(255, 165, 0, 0.1);
        border: 1px solid orange;
    }
    .poor-table {
        background-color: rgba(255, 0, 0, 0.1);
        border: 1px solid red;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0c3866;
        text-align: center;
        margin-bottom: 20px;
    }
    .subheader {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0c3866;
        margin-bottom: 10px;
    }
    .panel-group-header {
        background-color: #0c3866;
        color: white;
        padding: 5px 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .summary-card {
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    .group-summary-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .alert-card {
        background-color: #ffe6e6;
        border-left: 5px solid #ff0000;
        padding: 10px;
        margin: 10px 0;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions for efficiency classification
def classify_efficiency(efficiency):
    if efficiency >= 0.75:
        return "Good", "green"
    elif efficiency >= 0.5:
        return "Moderate", "yellow"
    else:
        return "Poor", "red"

def load_trained_model():
    try:
        # Try loading different model formats - adjust paths as needed
        if os.path.exists("solar_panel_efficiency_model.h5"):
            model = load_model("solar_panel_efficiency_model.h5")
            st.sidebar.success("Successfully loaded TensorFlow model.")
        elif os.path.exists("solar_panel_efficiency_model.joblib"):
            model = joblib.load("solar_panel_efficiency_model.joblib")
            st.sidebar.success("Successfully loaded joblib model.")
        elif os.path.exists("solar_panel_efficiency_model.pkl"):
            with open("solar_panel_efficiency_model.pkl", "rb") as f:
                model = pickle.load(f)
            st.sidebar.success("Successfully loaded pickle model.")
        else:
            st.sidebar.error("No model file found. Using dummy model for demo purposes.")
            # Create a dummy model for demonstration
            model = DummyModel()  # Defined below
        return model
    except Exception as e:
        st.sidebar.error(f"Error loading model: {e}")
        return DummyModel()  # Fallback to dummy model

# Dummy model for demonstration purposes if real model isn't available
class DummyModel:
    def predict(self, X):
        # Simulate predictions based on time of day for demo purposes
        hour = datetime.now().hour
        # Solar panels work better during daylight (simplified)
        if 10 <= hour <= 16:  # Peak sunlight hours
            return np.random.uniform(0.7, 0.95, (X.shape[0], 1))
        elif 7 <= hour < 10 or 16 < hour <= 19:  # Partial sunlight
            return np.random.uniform(0.45, 0.75, (X.shape[0], 1))
        else:  # Low/no sunlight
            return np.random.uniform(0.1, 0.45, (X.shape[0], 1))




# def get_real_time_data(panel_id, group_id):
#     # In production, this would connect to your IoT devices, APIs, or databases
#     # For demonstration, we'll generate simulated data
#     now = datetime.now()
    
#     # Add some variability based on panel and group ID
#     panel_num = int(panel_id.split('-')[1])
#     group_factor = ord(group_id) - ord('A') + 1
    
#     # Base values influenced by time of day
#     base_irradiance = max(0, 1000 * np.sin(np.pi * (now.hour + now.minute/60) / 12))
#     base_temperature = 25 + 10 * np.sin(np.pi * (now.hour + now.minute/60) / 12)
    
#     # Add variability based on panel and group
#     irradiance = base_irradiance * (0.9 + 0.2 * (panel_num % 3) / 10) * (0.95 + group_factor/20) + np.random.normal(0, 50)
#     temperature = base_temperature * (0.95 + 0.1 * (panel_num % 5) / 10) + np.random.normal(0, 2)
#     voltage = 48 * (0.98 + 0.04 * (group_factor % 3) / 10) + np.random.normal(0, 1)
#     current = max(0, 10 * np.sin(np.pi * (now.hour + now.minute/60) / 12) * (0.9 + 0.2 * panel_num / 10)) + np.random.normal(0, 0.5)
#     power = voltage * current
    
#     # Create features for model input
#     features = np.array([
#         [irradiance, temperature, voltage, current, power, 
#          now.hour, now.minute, now.weekday()]
#     ])
    
#     return {
#         "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
#         "panel_id": panel_id,
#         "group_id": group_id,
#         "irradiance": irradiance,  # W/m²
#         "temperature": temperature,  # °C
#         "voltage": voltage,  # V
#         "current": current,  # A
#         "power": power,  # W
#         "features": features
#     }

def get_real_time_data(panel_id, group_id):
    """
    Generate realistic solar panel data similar to real-world patterns.
    This function creates data points that follow typical solar panel behavior
    with appropriate distribution of efficiencies.
    """
    now = datetime.now()
    
    # Extract panel and group information for variation
    panel_num = int(panel_id.split('-')[1])
    group_factor = ord(group_id) - ord('A') + 1
    
    # Panel-specific base efficiency factor (0.65-0.95)
    # Deterministically assign efficiency tiers to ensure distribution across good/moderate/poor
    if panel_num % 5 == 0:  # 20% poor panels
        base_efficiency_factor = np.random.uniform(0.40, 0.49)
        panel_health = "poor"
    elif panel_num % 5 == 1:  # 20% moderate panels
        base_efficiency_factor = np.random.uniform(0.55, 0.74)
        panel_health = "moderate"
    else:  # 60% good panels
        base_efficiency_factor = np.random.uniform(0.75, 0.95)
        panel_health = "good"
    
    # Time of day factor - solar panels produce more during midday
    hour = now.hour + now.minute/60
    time_factor = max(0, np.sin(np.pi * (hour - 6) / 12)) if 6 <= hour <= 18 else 0
    
    # Weather variability (cloud cover effect) - simplified simulation
    # Use panel_id hash to create consistent weather patterns within groups
    panel_hash = hash(panel_id) % 100
    group_hash = hash(group_id) % 100
    weather_variability = 0.7 + 0.3 * np.sin(np.pi * (panel_hash / 100))
    
    # Calculate realistic values based on these factors
    max_irradiance = 1000  # W/m²
    irradiance = max_irradiance * time_factor * weather_variability
    
    # Temperature follows daily patterns and affects efficiency
    ambient_temp = 20 + 15 * time_factor  # Base ambient temperature
    panel_temp = ambient_temp + 10 * time_factor  # Panels get hotter with more sun
    
    # Add some age/dust/degradation effects based on panel number
    age_factor = 1.0 - (panel_num % 100) / 1000  # 0-10% degradation
    
    # Maintenance cycle effects - panels in different groups have different maintenance schedules
    maintenance_factor = 0.95 + 0.05 * np.sin(np.pi * (group_factor / 5))
    
    # Calculate electrical parameters
    voltage = 45 + 5 * time_factor * base_efficiency_factor * age_factor
    current = 8 * irradiance / max_irradiance * base_efficiency_factor * age_factor * maintenance_factor
    power = voltage * current
    
    # Add small random noise to all measurements
    irradiance *= np.random.uniform(0.98, 1.02)
    panel_temp *= np.random.uniform(0.99, 1.01)
    voltage *= np.random.uniform(0.99, 1.01)
    current *= np.random.uniform(0.99, 1.01)
    power = voltage * current  # Recalculate after adding noise
    
    # Create a more accurate efficiency prediction
    # This combines all the factors that influence real panel efficiency
    predicted_efficiency = (
        base_efficiency_factor * 
        age_factor * 
        maintenance_factor * 
        (1 - 0.005 * max(0, panel_temp - 25))  # Temperature coefficient
    )
    
    # Add noise to efficiency but keep within realistic bounds
    efficiency_with_noise = min(0.98, max(0.1, predicted_efficiency * np.random.uniform(0.97, 1.03)))
    
    # Create features for model input (keeping the same structure as the original code)
    features = np.array([
        [irradiance, panel_temp, voltage, current, power, 
         now.hour, now.minute, now.weekday()]
    ])
    
    return {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "panel_id": panel_id,
        "group_id": group_id,
        "irradiance": irradiance,
        "temperature": panel_temp,
        "voltage": voltage,
        "current": current,
        "power": power,
        "efficiency": efficiency_with_noise,
        "status": classify_efficiency(efficiency_with_noise)[0],  # Add status directly
        "features": features
    }

# Function to generate panel IDs for a group
def generate_panel_ids(group_id, num_panels=100):
    return [f"{group_id}-{i+1:03d}" for i in range(num_panels)]

# Initialize session state for storing data
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "timestamp", "panel_id", "group_id", "irradiance", "temperature", "voltage", 
        "current", "power", "efficiency", "status"
    ])

if 'group_summary' not in st.session_state:
    st.session_state.group_summary = pd.DataFrame(columns=[
        "group_id", "total_panels", "good_panels", "moderate_panels", "poor_panels", 
        "avg_efficiency", "total_power"
    ])

if 'alerts' not in st.session_state:
    st.session_state.alerts = []

def update_group_summaries(history_df):
    # Filter to get only the latest record for each panel
    if history_df.empty:
        return pd.DataFrame(columns=[
            "group_id", "total_panels", "good_panels", "moderate_panels", "poor_panels", 
            "avg_efficiency", "total_power"
        ])
    
    latest_records = history_df.sort_values("timestamp").groupby("panel_id").last().reset_index()
    
    # Group by group_id and calculate summaries
    group_summary = latest_records.groupby("group_id").agg(
        total_panels=("panel_id", "count"),
        good_panels=("status", lambda x: (x == "Good").sum()),
        moderate_panels=("status", lambda x: (x == "Moderate").sum()),
        poor_panels=("status", lambda x: (x == "Poor").sum()),
        avg_efficiency=("efficiency", "mean"),
        total_power=("power", "sum")
    ).reset_index()
    
    return group_summary

def show_page():
    # Page header
    st.markdown('<div class="main-header">☀️ Solar Panel Efficiency Monitor</div>', unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.title("Control Panel")
    
    # Load model
    model = load_trained_model()
    
    # Define panel groups
    panel_groups = ["A", "B", "C", "D", "E"]
    
    # Group selection
    selected_group = st.sidebar.selectbox(
        "Select Panel Group:",
        panel_groups,
        index=0
    )
    
    # Panel selection (filtered by group)
    panel_ids = generate_panel_ids(selected_group, num_panels=100)
    selected_panel = st.sidebar.selectbox(
        "Select Individual Panel:",
        panel_ids,
        index=0
    )
    
    # Advanced settings
    st.sidebar.markdown("---")
    st.sidebar.subheader("Advanced Settings")
    
    # Refresh rate control
    refresh_interval = st.sidebar.slider(
        "Data Refresh Interval (seconds)",
        min_value=1,
        max_value=60,
        value=5
    )
    
    # Alert thresholds
    efficiency_alert_threshold = st.sidebar.slider(
        "Efficiency Alert Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.4,
        step=0.05
    )
    
    temperature_alert_threshold = st.sidebar.slider(
        "Temperature Alert Threshold (°C)",
        min_value=30,
        max_value=80,
        value=50,
        step=5
    )
    
    # Show/hide sections
    show_alerts = st.sidebar.checkbox("Show Alerts Section", value=True)
    show_category_tables = st.sidebar.checkbox("Show Categorized Panels", value=True)
    
    # Export data option
    if st.sidebar.button("Export Historical Data"):
        # In a real application, this would save data to a file
        st.sidebar.success("Data exported successfully!")
    
    # Monitoring controls
    col1, col2 = st.columns(2)
    
    with col1:
        start_monitoring = st.button("Start Monitoring", use_container_width=True)
    
    with col2:
        stop_monitoring = st.button("Stop Monitoring", use_container_width=True)
    
    # Create placeholder for different sections
    summary_section = st.container()
    alerts_section = st.container() if show_alerts else None
    metrics_section = st.container()
    chart_section = st.container()
    panel_tables_section = st.container() if show_category_tables else None
    history_section = st.container()
    
    # Main monitoring loop
    monitoring_placeholder = st.empty()
    
    if start_monitoring:
        st.session_state.monitoring = True
    
    if stop_monitoring:
        st.session_state.monitoring = False
        
    # if st.session_state.get('monitoring', False):
    #     with monitoring_placeholder.container():
    #         # Simulate getting data from all panels in all groups (for summary)
    #         all_panel_data = []
            
    #         # For demo, we'll simulate data for a subset of panels from each group
    #         for group_id in panel_groups:
    #             # Simulate data for 10 random panels from each group for efficiency
    #             sample_panels = [f"{group_id}-{np.random.randint(1, 101):03d}" for _ in range(10)]
    #             for panel_id in sample_panels:
    #                 panel_data = get_real_time_data(panel_id, group_id)
                    
    #                 # Predict efficiency using the model
    #                 try:
    #                     predicted_efficiency = model.predict(panel_data["features"])[0][0]
    #                 except:
    #                     # Fallback in case of prediction error
    #                     hour = datetime.now().hour
    #                     if 10 <= hour <= 16:
    #                         predicted_efficiency = np.random.uniform(0.7, 0.95)
    #                     elif 7 <= hour < 10 or 16 < hour <= 19:
    #                         predicted_efficiency = np.random.uniform(0.45, 0.75)
    #                     else:
    #                         predicted_efficiency = np.random.uniform(0.1, 0.45)
                    
    #                 # Classify efficiency
    #                 status, color = classify_efficiency(predicted_efficiency)
                    
    #                 # Add to data collection
    #                 panel_data["efficiency"] = predicted_efficiency
    #                 panel_data["status"] = status
    #                 all_panel_data.append(panel_data)
                    
    #                 # Check for alerts
    #                 if predicted_efficiency < efficiency_alert_threshold:
    #                     alert = f"Low efficiency alert: Panel {panel_id} at {predicted_efficiency:.2f}"
    #                     if alert not in st.session_state.alerts:
    #                         st.session_state.alerts.append(alert)
                    
    #                 if panel_data["temperature"] > temperature_alert_threshold:
    #                     alert = f"High temperature alert: Panel {panel_id} at {panel_data['temperature']:.1f}°C"
    #                     if alert not in st.session_state.alerts:
    #                         st.session_state.alerts.append(alert)
    if st.session_state.get('monitoring', False):
        with monitoring_placeholder.container():
            # Simulate getting data from all panels in all groups (for summary)
            all_panel_data = []
            
            # For demo, we'll simulate data for ALL panels in the selected group and a subset from others
            for group_id in panel_groups:
                # For the selected group, get data for all 100 panels
                if group_id == selected_group:
                    sample_panels = generate_panel_ids(group_id, num_panels=100)
                else:
                    # For other groups, just get a sample of 10 panels for efficiency
                    sample_panels = [f"{group_id}-{np.random.randint(1, 101):03d}" for _ in range(10)]
                
                for panel_id in sample_panels:
                    panel_data = get_real_time_data(panel_id, group_id)
                    
                    # Predict efficiency using the model
                    try:
                        predicted_efficiency = model.predict(panel_data["features"])[0][0]
                    except:
                        # Fallback in case of prediction error
                        # Use the panel_id to create consistent variation in efficiencies
                        panel_num = int(panel_id.split('-')[1])
                        # Assign poor efficiency (20% of panels)
                        if panel_num % 5 == 0:
                            predicted_efficiency = np.random.uniform(0.3, 0.45)
                        # Assign moderate efficiency (30% of panels)
                        elif panel_num % 3 == 0:
                            predicted_efficiency = np.random.uniform(0.5, 0.7)
                        # Assign good efficiency (50% of panels)
                        else:
                            predicted_efficiency = np.random.uniform(0.75, 0.9)
                    
                    # Classify efficiency
                    status, color = classify_efficiency(predicted_efficiency)
                    
                    # Add to data collection
                    panel_data["efficiency"] = predicted_efficiency
                    panel_data["status"] = status
                    all_panel_data.append(panel_data)
                    
                    # Check for alerts
                    if predicted_efficiency < efficiency_alert_threshold:
                        alert = f"Low efficiency alert: Panel {panel_id} at {predicted_efficiency:.2f}"
                        if alert not in st.session_state.alerts:
                            st.session_state.alerts.append(alert)
                    
                    if panel_data["temperature"] > temperature_alert_threshold:
                        alert = f"High temperature alert: Panel {panel_id} at {panel_data['temperature']:.1f}°C"
                        if alert not in st.session_state.alerts:
                            st.session_state.alerts.append(alert)        
            # Update history with new data
            new_rows = []
            for data in all_panel_data:
                new_row = {
                    "timestamp": data["timestamp"],
                    "panel_id": data["panel_id"],
                    "group_id": data["group_id"],
                    "irradiance": data["irradiance"],
                    "temperature": data["temperature"],
                    "voltage": data["voltage"],
                    "current": data["current"],
                    "power": data["power"],
                    "efficiency": data["efficiency"],
                    "status": data["status"]
                }
                new_rows.append(new_row)
            
            st.session_state.history = pd.concat([
                st.session_state.history,
                pd.DataFrame(new_rows)
            ], ignore_index=True).tail(1000)  # Keep last 1000 records
            
            # Update group summaries
            st.session_state.group_summary = update_group_summaries(st.session_state.history)
            
            # Get data for selected panel (for detailed view)
            selected_panel_data = next((data for data in all_panel_data if data["panel_id"] == selected_panel), None)
            if not selected_panel_data:
                # If selected panel not in sample, generate it specifically
                selected_panel_data = get_real_time_data(selected_panel, selected_group)
                try:
                    selected_panel_data["efficiency"] = model.predict(selected_panel_data["features"])[0][0]
                except:
                    # Fallback
                    selected_panel_data["efficiency"] = np.random.uniform(0.4, 0.9)
                selected_panel_data["status"], _ = classify_efficiency(selected_panel_data["efficiency"])
            
            # Display overall system summary
            with summary_section:
                st.markdown('<div class="subheader">System Overview</div>', unsafe_allow_html=True)
                
                # Overall metrics
                if not st.session_state.group_summary.empty:
                    total_panels = st.session_state.group_summary["total_panels"].sum()
                    total_good = st.session_state.group_summary["good_panels"].sum()
                    total_moderate = st.session_state.group_summary["moderate_panels"].sum()
                    total_poor = st.session_state.group_summary["poor_panels"].sum()
                    avg_system_efficiency = st.session_state.group_summary["avg_efficiency"].mean()
                    total_system_power = st.session_state.group_summary["total_power"].sum()
                    
                    # System summary cards
                    st.markdown(f"""
                    <div class="group-summary-card">
                        <h3>System Health Summary</h3>
                        <div style="display: flex; flex-wrap: wrap; justify-content: space-between;">
                            <div style="flex: 0 0 16%; text-align: center;">
                                <div style="font-size: 2rem; font-weight: bold; color: #0c3866;">{total_panels}</div>
                                <div>Total Panels</div>
                            </div>
                            <div style="flex: 0 0 16%; text-align: center;">
                                <div style="font-size: 2rem; font-weight: bold; color: green;">{total_good}</div>
                                <div>Good Panels</div>
                            </div>
                            <div style="flex: 0 0 16%; text-align: center;">
                                <div style="font-size: 2rem; font-weight: bold; color: orange;">{total_moderate}</div>
                                <div>Moderate Panels</div>
                            </div>
                            <div style="flex: 0 0 16%; text-align: center;">
                                <div style="font-size: 2rem; font-weight: bold; color: red;">{total_poor}</div>
                                <div>Poor Panels</div>
                            </div>
                            <div style="flex: 0 0 16%; text-align: center;">
                                <div style="font-size: 2rem; font-weight: bold; color: #0c3866;">{avg_system_efficiency:.2f}</div>
                                <div>Avg Efficiency</div>
                            </div>
                            <div style="flex: 0 0 16%; text-align: center;">
                                <div style="font-size: 2rem; font-weight: bold; color: #0c3866;">{total_system_power:.1f} W</div>
                                <div>Total Power</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Group summary cards
                    st.markdown('<h4>Panel Group Summary</h4>', unsafe_allow_html=True)
                    group_cols = st.columns(len(panel_groups))
                    
                    for i, group_id in enumerate(panel_groups):
                        group_data = st.session_state.group_summary[st.session_state.group_summary["group_id"] == group_id]
                        
                        if not group_data.empty:
                            good_percent = group_data["good_panels"].iloc[0] / group_data["total_panels"].iloc[0] * 100
                            moderate_percent = group_data["moderate_panels"].iloc[0] / group_data["total_panels"].iloc[0] * 100
                            poor_percent = group_data["poor_panels"].iloc[0] / group_data["total_panels"].iloc[0] * 100
                            
                            with group_cols[i]:
                                st.markdown(f"""
                                <div class="summary-card">
                                    <h4>Group {group_id}</h4>
                                    <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                                        <div style="width: 100px; height: 100px; border-radius: 50%; background: conic-gradient(
                                            green 0% {good_percent}%, 
                                            orange {good_percent}% {good_percent + moderate_percent}%, 
                                            red {good_percent + moderate_percent}% 100%
                                        );"></div>
                                    </div>
                                    <div>Efficiency: {group_data["avg_efficiency"].iloc[0]:.2f}</div>
                                    <div>Power: {group_data["total_power"].iloc[0]:.1f} W</div>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.info("Waiting for data to calculate system summary...")
            
            # Display alerts if enabled
            if show_alerts and alerts_section:
                with alerts_section:
                    st.markdown('<div class="subheader">System Alerts</div>', unsafe_allow_html=True)
                    
                    # Keep only the 10 most recent alerts
                    st.session_state.alerts = st.session_state.alerts[-10:]
                    
                    if st.session_state.alerts:
                        for alert in reversed(st.session_state.alerts):
                            st.markdown(f"""
                            <div class="alert-card">
                                <strong>{alert.split(':')[0]}:</strong> {alert.split(':', 1)[1]}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("No active alerts - All systems normal")
            
            # Display real-time metrics for selected panel
            with metrics_section:
                st.markdown(f'<div class="panel-group-header">Panel Details - {selected_panel} (Group {selected_group})</div>', unsafe_allow_html=True)
                
                m1, m2, m3, m4, m5 = st.columns(5)
                
                with m1:
                    st.metric("Temperature", f"{selected_panel_data['temperature']:.1f} °C", 
                              f"{np.random.uniform(-1, 1):.1f} °C")
                
                with m2:
                    st.metric("Irradiance", f"{selected_panel_data['irradiance']:.1f} W/m²", 
                              f"{np.random.uniform(-50, 50):.1f} W/m²")
                
                with m3:
                    st.metric("Power Output", f"{selected_panel_data['power']:.1f} W", 
                              f"{np.random.uniform(-10, 10):.1f} W")
                
                with m4:
                    st.metric("Predicted Efficiency", f"{selected_panel_data['efficiency']:.2f}", 
                              f"{np.random.uniform(-0.05, 0.05):.2f}")
                
                with m5:
                    status = selected_panel_data["status"]
                    if status == "Good":
                        st.markdown(f"<div class='metric-card' style='background-color:rgba(0,128,0,0.2)'><h3 style='color:green'>STATUS: GOOD</h3></div>", unsafe_allow_html=True)
                    elif status == "Moderate":
                        st.markdown(f"<div class='metric-card' style='background-color:rgba(255,165,0,0.2)'><h3 style='color:orange'>STATUS: MODERATE</h3></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='metric-card' style='background-color:rgba(255,0,0,0.2)'><h3 style='color:red'>STATUS: POOR</h3></div>", unsafe_allow_html=True)
            
            # Display charts for selected panel
            with chart_section:
                if not st.session_state.history.empty:
                    # Filter history for selected panel
                    panel_history = st.session_state.history[st.session_state.history["panel_id"] == selected_panel].copy()
                    panel_history['timestamp'] = pd.to_datetime(panel_history['timestamp'])
                    
                    # Only proceed if we have data for this panel
                    if not panel_history.empty:
                        chart_cols = st.columns(2)
                        
                        with chart_cols[0]:
                            st.subheader("Efficiency Over Time")
                            
                            # Create color-mapped efficiency chart
                            fig = px.line(
                                panel_history, 
                                x='timestamp', 
                                y='efficiency',
                                title=f"Panel {selected_panel} Efficiency Trend",
                                labels={"timestamp": "Time", "efficiency": "Efficiency"}
                            )
                            
                            # Add color-coded background regions
                            fig.add_shape(
                                type="rect",
                                x0=panel_history['timestamp'].min(),
                                x1=panel_history['timestamp'].max(),
                                y0=0,
                                y1=0.5,
                                fillcolor="rgba(255,0,0,0.1)",
                                line=dict(width=0),
                                layer="below"
                            )
                            fig.add_shape(
                                type="rect",
                                x0=panel_history['timestamp'].min(),
                                x1=panel_history['timestamp'].max(),
                                y0=0.5,
                                y1=0.75,
                                fillcolor="rgba(255,165,0,0.1)",
                                line=dict(width=0),
                                layer="below"
                            )
                            fig.add_shape(
                                type="rect",
                                x0=panel_history['timestamp'].min(),
                                x1=panel_history['timestamp'].max(),
                                y0=0.75,
                                y1=1.0,
                                fillcolor="rgba(0,128,0,0.1)",
                                line=dict(width=0),
                                layer="below"
                            )
                            
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with chart_cols[1]:
                            st.subheader("Power vs Environmental Factors")
                            
                            # Create scatterplot
                            fig = px.scatter(
                                panel_history,
                                x="temperature",
                                y="power",
                                color="efficiency",
                                size="irradiance",
                                color_continuous_scale=["red", "yellow", "green"],
                                title=f"Panel {selected_panel} Performance Factors",
                                labels={
                                    "temperature": "Temperature (°C)",
                                    "power": "Power Output (W)",
                                    "efficiency": "Efficiency"
                                }
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Additional chart for group comparison
                    group_data = st.session_state.history[st.session_state.history["group_id"] == selected_group].copy()
                    if not group_data.empty:
                        # Get the latest data point for each panel in the group
                        latest_group_data = group_data.sort_values("timestamp").groupby("panel_id").last().reset_index()
                        
                        # Create a box plot comparing panels within the group
                        fig = px.box(
                            latest_group_data,
                            y="efficiency",
                            title=f"Efficiency Distribution - Group {selected_group}",
                            labels={"efficiency": "Efficiency"},
                            height=300
                        )
                        
                        # Add a scatter plot on top of the box plot
                        fig.add_trace(
                            go.Scatter(
                                x=[0] * len(latest_group_data),
                                y=latest_group_data["efficiency"],
                                mode="markers",
                                marker=dict(
                                    color=latest_group_data["efficiency"],
                                    colorscale=["red", "yellow", "green"],
                                    size=8,
                                    opacity=0.7
                                ),
                                name="Panels"
                            )
                        )
                        
                        # Add a marker for the selected panel
                        selected_efficiency = latest_group_data[latest_group_data["panel_id"] == selected_panel]["efficiency"].values
                        if len(selected_efficiency) > 0:
                            fig.add_trace(
                                go.Scatter(
                                    x=[0],
                                    y=[selected_efficiency[0]],
                                    mode="markers",
                                    marker=dict(
                                        color="black",
                                        symbol="star",
                                        size=15,
                                        line=dict(width=2, color="white")
                                    ),
                                    name=f"Selected Panel ({selected_panel})"
                                )
                            )
                        
                        fig.update_layout(showlegend=True)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Display histogram of panel efficiencies by group
                    if len(st.session_state.history["group_id"].unique()) > 1:
                        # Get the latest data point for each panel
                        latest_data = st.session_state.history.sort_values("timestamp").groupby("panel_id").last().reset_index()
                        
                        # Create a histogram comparing groups
                        fig = px.histogram(
                            latest_data,
                            x="efficiency",
                            color="group_id",
                            barmode="overlay",
                            marginal="box",
                            title="Efficiency Distribution by Group",
                            labels={"efficiency": "Efficiency", "group_id": "Group"},
                            height=400,
                            opacity=0.7
                        )
                        fig.update_layout(
                            xaxis_title="Efficiency",
                            yaxis_title="Count",
                            legend_title="Panel Group"
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            # Display categorized panel tables if enabled
            if show_category_tables and panel_tables_section:
                with panel_tables_section:
                    st.markdown(f'<div class="panel-group-header">Categorized Panels - Group {selected_group}</div>', unsafe_allow_html=True)
                    
                    # Filter to get only the latest record for each panel in the selected group
                    if not st.session_state.history.empty:
                        group_history = st.session_state.history[st.session_state.history["group_id"] == selected_group].copy()
                        if not group_history.empty:
                            latest_group_data = group_history.sort_values("timestamp").groupby("panel_id").last().reset_index()
                            
                            # Split into good, moderate, and poor panels
                            good_panels = latest_group_data[latest_group_data["status"] == "Good"].sort_values("efficiency", ascending=False)
                            moderate_panels = latest_group_data[latest_group_data["status"] == "Moderate"].sort_values("efficiency", ascending=False)
                            poor_panels = latest_group_data[latest_group_data["status"] == "Poor"].sort_values("efficiency", ascending=False)
                            
                            # Display in three columns
                            panel_cat_cols = st.columns(3)
                            
                            with panel_cat_cols[0]:
                                st.markdown(f"""
                                <div class="panel-table good-table">
                                    <h4 style="color: green; text-align: center;">Good Panels ({len(good_panels)})</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if not good_panels.empty:
                                    # Format for display
                                    display_df = good_panels[["panel_id", "efficiency", "power", "temperature"]].copy()
                                    display_df.columns = ["Panel ID", "Efficiency", "Power (W)", "Temp (°C)"]
                                    display_df = display_df.round({"Efficiency": 3, "Power (W)": 1, "Temp (°C)": 1})
                                    
                                    # Highlight the selected panel
                                    def highlight_selected(s):
                                        return ['background-color: rgba(0,128,0,0.3)' if s["Panel ID"] == selected_panel else '' for _ in s]
                                    
                                    st.dataframe(
                                        display_df.style.apply(highlight_selected, axis=1),
                                        height=300,
                                        use_container_width=True
                                    )
                                else:
                                    st.info("No panels with good efficiency")
                            
                            with panel_cat_cols[1]:
                                st.markdown(f"""
                                <div class="panel-table moderate-table">
                                    <h4 style="color: orange; text-align: center;">Moderate Panels ({len(moderate_panels)})</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if not moderate_panels.empty:
                                    # Format for display
                                    display_df = moderate_panels[["panel_id", "efficiency", "power", "temperature"]].copy()
                                    display_df.columns = ["Panel ID", "Efficiency", "Power (W)", "Temp (°C)"]
                                    display_df = display_df.round({"Efficiency": 3, "Power (W)": 1, "Temp (°C)": 1})
                                    
                                    # Highlight the selected panel
                                    def highlight_selected(s):
                                        return ['background-color: rgba(255,165,0,0.3)' if s["Panel ID"] == selected_panel else '' for _ in s]
                                    
                                    st.dataframe(
                                        display_df.style.apply(highlight_selected, axis=1),
                                        height=300,
                                        use_container_width=True
                                    )
                                else:
                                    st.info("No panels with moderate efficiency")
                            
                            with panel_cat_cols[2]:
                                st.markdown(f"""
                                <div class="panel-table poor-table">
                                    <h4 style="color: red; text-align: center;">Poor Panels ({len(poor_panels)})</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if not poor_panels.empty:
                                    # Format for display
                                    display_df = poor_panels[["panel_id", "efficiency", "power", "temperature"]].copy()
                                    display_df.columns = ["Panel ID", "Efficiency", "Power (W)", "Temp (°C)"]
                                    display_df = display_df.round({"Efficiency": 3, "Power (W)": 1, "Temp (°C)": 1})
                                    
                                    # Highlight the selected panel
                                    def highlight_selected(s):
                                        return ['background-color: rgba(255,0,0,0.3)' if s["Panel ID"] == selected_panel else '' for _ in s]
                                    
                                    st.dataframe(
                                        display_df.style.apply(highlight_selected, axis=1),
                                        height=300,
                                        use_container_width=True
                                    )
                                else:
                                    st.info("No panels with poor efficiency")
                        else:
                            st.info(f"No data available for Group {selected_group} yet")
            
            # Historical data table for selected panel
            with history_section:
                st.markdown(f'<div class="panel-group-header">Historical Data - {selected_panel}</div>', unsafe_allow_html=True)
                
                # Filter history for the selected panel
                panel_history = st.session_state.history[st.session_state.history["panel_id"] == selected_panel].copy()
                
                if not panel_history.empty:
                    # Format the dataframe for display
                    display_df = panel_history.copy()
                    display_df['time'] = pd.to_datetime(display_df['timestamp']).dt.time
                    display_df['status_colored'] = display_df['status'].apply(
                        lambda x: f"{x}" if x == "Good" 
                        else (f"{x}" if x == "Moderate" 
                              else f"{x}")
                    )
                    
                    cols_to_display = ['time', 'irradiance', 'temperature', 'power', 'efficiency', 'status_colored']
                    st.dataframe(
                        display_df[cols_to_display].rename(
                            columns={'time': 'Time', 'irradiance': 'Irradiance (W/m²)', 
                                    'temperature': 'Temp (°C)', 'power': 'Power (W)', 
                                    'efficiency': 'Efficiency', 'status_colored': 'Status'}
                        ).style.format({
                            'Irradiance (W/m²)': '{:.1f}',
                            'Temp (°C)': '{:.1f}',
                            'Power (W)': '{:.1f}',
                            'Efficiency': '{:.3f}'
                        }), 
                        use_container_width=True,
                        height=300
                    )
                else:
                    st.info(f"No historical data available for Panel {selected_panel} yet")
            
            # Sleep to simulate refresh interval
            time.sleep(refresh_interval)
            
            # Trigger rerun to refresh data
            st.rerun()
    else:
        st.info("Click 'Start Monitoring' to begin real-time data collection and analysis.")

if __name__ == "__main__":
    show_page()