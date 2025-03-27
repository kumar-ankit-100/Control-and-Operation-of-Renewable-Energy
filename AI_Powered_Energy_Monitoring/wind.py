import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pickle
import os
from plotly.subplots import make_subplots

# Set page configuration
# st.set_page_config(
#     page_title="Wind Turbine Efficiency Monitor",
#     page_icon="🌬️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

st.markdown("""
<style>
    /* Main background color - light blue */
    .stApp {
        background-color: #e6f2ff;  /* Light blue background */
    }

    /* Make sure content areas have appropriate contrast */
    .main .block-container {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f0f7ff;
        border-right: 1px solid #b8d8ff;
    }

    /* Set all text to black by default */
    * {
        color: black;
    }

    /* Headers with black text */
    h1, h2, h3, p, span, div, .main-header, .subheader {
        color: black;
    }

    /* Ensure sidebar text is black */
    [data-testid="stSidebar"] * {
        color: black;
    }

    /* Exception for status indicators */
    .good-efficiency {color: green; font-weight: bold;}
    .moderate-efficiency {color: orange; font-weight: bold;}
    .poor-efficiency {color: red; font-weight: bold;}

    /* Metric cards with better contrast */
    .metric-card {
        background-color: white;
        border: 1px solid #d1e3ff;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }

    /* Panel styling */
    .panel-table {
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 10px;
        margin-bottom: 10px;
    }

    /* Status tables - preserve special backgrounds but with black text */
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
        text-align: center;
        margin-bottom: 20px;
    }

    .subheader {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .panel-group-header {
        background-color: #0c3866;
        color: white !important; /* Force white text on dark background */
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
        background-color: white;
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

    /* Chart area */
    [data-testid="stPlotlyChart"] {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Data tables */
    .stDataFrame {
        background-color: white;
        border-radius: 5px;
        padding: 5px;
    }

    /* Buttons with better visibility */
    .stButton > button {
        border: 1px solid #0c3866;
        color: black;
        background-color: white;
    }

    .stButton > button:hover {
        background-color: #0c3866;
        color: white !important; /* Force white text on hover */
    }

    /* Make sure labels and values in metrics are black */
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        color: black !important;
    }

    /* Fix for selectbox - ensure text is visible */
    [data-testid="stSelectbox"] {
        color: black !important;
    }
    
    /* Fix selectbox dropdown background color */
    [data-testid="stSelectbox"] > div > div {
        background-color: white !important;
    }
    
    /* Fix for selectbox option text */
    .st-bj, .st-bk, .st-bl, .st-al, .st-am, .st-an {
        color: black !important;
    }
    
    /* Dropdown container and options */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] ul,
    div[data-baseweb="select"] li,
    div[data-baseweb="popover"] div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background-color: white !important;
        color: black !important;
    }
    
    /* Ensure that dropdown options are visible */
    li[role="option"] {
        background-color: white !important;
        color: black !important;
    }
    
    /* Dropdown hover state */
    li[role="option"]:hover {
        background-color: #f0f7ff !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions for efficiency classification
def calculate_efficiency(active_power, theoretical_power):
    """Calculate efficiency as ratio of actual power to theoretical power"""
    if theoretical_power <= 0:
        return 0
    return min(active_power / theoretical_power, 1)

def classify_efficiency(efficiency):
    if efficiency >= 0.75:
        return "Good", "green"
    elif efficiency >= 0.5:
        return "Moderate", "yellow"
    else:
        return "Poor", "red"

def create_simulated_data():
    """Create simulated data based on Kaggle Wind Turbine dataset structure"""
    # Generate timestamps for last 48 hours with 10-minute intervals
    end_time = pd.Timestamp.now().floor('10min')
    start_time = end_time - pd.Timedelta(days=2)
    timestamps = pd.date_range(start=start_time, end=end_time, freq='10min')
    
    # Generate data with realistic patterns
    n = len(timestamps)
    
    # Simulate daily patterns with some randomness
    hour_of_day = np.array([t.hour + t.minute/60 for t in timestamps])
    
    # Wind speed with daily pattern (stronger during day)
    wind_speed = 5 + 3 * np.sin(np.pi * hour_of_day / 12) + np.random.normal(0, 1, n)
    wind_speed = np.maximum(0.5, wind_speed)
    
    # Wind direction changes slowly over time
    wind_direction = np.cumsum(np.random.normal(0, 5, n)) % 360
    
    # Temperature with daily cycle
    ambient_temp = 15 + 5 * np.sin(np.pi * (hour_of_day - 2) / 12) + np.random.normal(0, 1, n)
    
    # Calculate theoretical power based on wind speed (simplified cube law)
    # P = 0.5 * air_density * swept_area * Cp * wind_speed^3
    theoretical_power = 0.5 * 1.225 * 8000 * 0.45 * wind_speed**3
    theoretical_power = np.minimum(theoretical_power, 2000)  # Cap at 2000 kW
    
    # Active power with some efficiency losses
    active_power = theoretical_power * (0.7 + 0.2 * np.random.random(n))
    active_power = np.maximum(0, active_power)
    
    # Nacelle angle tries to follow wind direction with some lag
    nacelle_angle = np.roll(wind_direction, 3)
    
    # Simulate rotor RPM based on wind speed
    rotor_rpm = 5 + wind_speed * 2 + np.random.normal(0, 1, n)
    
    # Create dataframe
    data = pd.DataFrame({
        'Date_Time': timestamps,
        'ActivePower_kW': active_power,
        'AmbientTemperature_°C': ambient_temp,
        'WindDirection_°': wind_direction,
        'WindSpeed_m/s': wind_speed,
        'NacellePosition_°': nacelle_angle,
        'RotorRPM': rotor_rpm,
        'TheoreticalPower_kW': theoretical_power
    })
    
    return data

def load_dataset():
    """Load the Kaggle Wind Turbine dataset"""
    try:
        # Check if file exists in current directory
        if os.path.exists("Turbine_Data.csv"):
            data = pd.read_csv("Turbine_Data.csv")
            # Ensure Date_Time column exists and is properly formatted
            if 'Date_Time' not in data.columns:
                st.sidebar.warning("Turbine_Data.csv found.")
                data = create_simulated_data()
            st.sidebar.success("Successfully loaded Turbine_Data.csv")
        else:
            st.sidebar.warning("Turbine_Data.csv not found. Using simulated data for demonstration.")
            # Create simulated data similar to Kaggle dataset format
            data = create_simulated_data()
        return data
    except Exception as e:
        st.sidebar.error(f"Error loading dataset: {e}")
        return create_simulated_data()

def load_trained_model():
    try:
        # Try loading pickle model - adjust path as needed
        if os.path.exists("wind_energy_model.pkl"):
            with open("wind_energy_model.pkl", "rb") as f:
                model = pickle.load(f)
            st.sidebar.success("Successfully loaded pickle model.")
        else:
            st.sidebar.warning("No model file found. Using dummy model for demo purposes.")
            # Create a dummy model for demonstration
            model = DummyModel()
        return model
    except Exception as e:
        st.sidebar.error(f"Error loading model: {e}")
        return DummyModel()

# Dummy model for demonstration purposes if real model isn't available
class DummyModel:
    def predict(self, X):
        # Simulate predictions based on input features
        # For simplicity, we'll use wind speed as main predictor
        wind_speed = X[:, 3]  # Assuming wind speed is at index 3
        predictions = []
        
        for ws in wind_speed:
            if ws > 8:  # Strong wind
                pred = 2  # Good efficiency
            elif ws > 4:  # Moderate wind
                pred = 1  # Moderate efficiency
            else:  # Low wind
                pred = 0  # Poor efficiency
            predictions.append(pred)
            
        return np.array(predictions)
    
    def predict_proba(self, X):
        # For visualization purposes, we'll simulate probabilities
        n_samples = X.shape[0]
        wind_speed = X[:, 3]  # Assuming wind speed is at index 3
        
        probas = np.zeros((n_samples, 3))
        for i, ws in enumerate(wind_speed):
            if ws > 8:  # Strong wind
                probas[i] = [0.1, 0.2, 0.7]  # Likely good
            elif ws > 4:  # Moderate wind
                probas[i] = [0.2, 0.6, 0.2]  # Likely moderate
            else:  # Low wind
                probas[i] = [0.7, 0.2, 0.1]  # Likely poor
                
        return probas

# Function to get real-time data from the dataset
def get_real_time_data(dataset, turbine_id, simulated_time=None):
    # In production, you would query your actual turbine data source
    # For demonstration, we'll sample from our loaded dataset
    
    if simulated_time is None:
        # Use the current time for simulation
        simulated_time = datetime.now()
    
    # Find the closest timestamp in the dataset
    # In real implementation, you would query the latest data point
    if isinstance(dataset, pd.DataFrame) and 'Date_Time' in dataset.columns and not dataset.empty:
        dataset['Date_Time'] = pd.to_datetime(dataset['Date_Time'])
        
        # For simulation, we'll pick a random row or one close to our simulated time
        if isinstance(simulated_time, int):
            # If simulated_time is an index, use that row
            idx = simulated_time % len(dataset)
            row = dataset.iloc[idx].copy()
        else:
            # Try to find the closest timestamp
            simulated_time_str = pd.Timestamp(simulated_time)
            idx = abs(dataset['Date_Time'] - simulated_time_str).idxmin()
            row = dataset.iloc[idx].copy()
    else:
        # Create a fallback row if dataset doesn't have expected structure
        row = pd.Series({
            'Date_Time': simulated_time,
            'ActivePower_kW': np.random.uniform(100, 1500),
            'AmbientTemperature_°C': np.random.uniform(10, 25),
            'WindDirection_°': np.random.uniform(0, 360),
            'WindSpeed_m/s': np.random.uniform(2, 15),
            'NacellePosition_°': np.random.uniform(0, 360),
            'RotorRPM': np.random.uniform(5, 20),
            'TheoreticalPower_kW': np.random.uniform(200, 2000)
        })
    
    # Calculate theoretical power if not present
    if 'TheoreticalPower_kW' not in row:
        # Simplified theoretical power calculation
        wind_speed = row['WindSpeed_m/s']
        row['TheoreticalPower_kW'] = min(0.5 * 1.225 * 8000 * 0.45 * wind_speed**3, 2000)
    
    # Calculate yaw error (difference between wind direction and nacelle position)
    yaw_error = min(abs(row['WindDirection_°'] - row['NacellePosition_°']), 
                   abs(360 - abs(row['WindDirection_°'] - row['NacellePosition_°'])))
    
    # Create features for model input
    features = np.array([
        [row['ActivePower_kW'], row['AmbientTemperature_°C'], 
         row['WindDirection_°'], row['WindSpeed_m/s'], 
         row['NacellePosition_°'], row['RotorRPM'], yaw_error]
    ])
    
    # Calculate efficiency
    efficiency = calculate_efficiency(row['ActivePower_kW'], row['TheoreticalPower_kW'])
    
    return {
        "timestamp": row['Date_Time'] if isinstance(row['Date_Time'], str) else row['Date_Time'].strftime("%Y-%m-%d %H:%M:%S"),
        "active_power": row['ActivePower_kW'],
        "theoretical_power": row['TheoreticalPower_kW'],
        "wind_speed": row['WindSpeed_m/s'],
        "wind_direction": row['WindDirection_°'],
        "ambient_temp": row['AmbientTemperature_°C'],
        "rotor_rpm": row['RotorRPM'],
        "nacelle_position": row['NacellePosition_°'],
        "yaw_error": yaw_error,
        "efficiency": efficiency,
        "features": features
    }

# Initialize session state for storing historical data
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "timestamp", "active_power", "theoretical_power", "wind_speed", "wind_direction", 
        "ambient_temp", "rotor_rpm", "nacelle_position", "yaw_error", "efficiency", "status"
    ])

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

def show_page():
    # Page header
    st.markdown('<div class="main-header">🌬️ Wind Turbine Efficiency Monitor</div>', unsafe_allow_html=True)
    
    # Load dataset
    dataset = load_dataset()
    
    # Sidebar controls
    st.sidebar.title("Control Panel")
    
    # Load model
    model = load_trained_model()
    
    # Turbine selection
    turbine_id = st.sidebar.selectbox(
        "Select Wind Turbine:",
        ["Turbine-01", "Turbine-02", "Turbine-03", "Turbine-04", "Turbine-05"]
    )
    
    # Refresh rate control
    refresh_interval = st.sidebar.slider(
        "Data Refresh Interval (seconds)",
        min_value=1,
        max_value=60,
        value=5
    )
    
    # Data simulation speed
    simulation_speed = st.sidebar.slider(
        "Simulation Speed",
        min_value=1,
        max_value=20,
        value=5,
        help="Higher values will simulate faster time progression"
    )
    
    # Dataset info - safely display info about dataset
    if isinstance(dataset, pd.DataFrame) and not dataset.empty and 'Date_Time' in dataset.columns:
        st.sidebar.subheader("Dataset Information")
        st.sidebar.info(f"Dataset size: {len(dataset)} records\nTime range: {dataset['Date_Time'].min()} to {dataset['Date_Time'].max()}")
    
    # Monitoring controls
    col1, col2 = st.columns(2)
    
    with col1:
        start_monitoring = st.button("Start Monitoring", use_container_width=True)
    
    with col2:
        stop_monitoring = st.button("Stop Monitoring", use_container_width=True)
    
    # Create placeholder for metrics and charts
    metrics_section = st.container()
    chart_section = st.container()
    history_section = st.container()
    
    # Main monitoring loop
    monitoring_placeholder = st.empty()
    
    if start_monitoring:
        st.session_state.monitoring = True
    
    if stop_monitoring:
        st.session_state.monitoring = False
    
    if st.session_state.get('monitoring', False):
        with monitoring_placeholder.container():
            # For simulation, use index to step through dataset or generate simulated data
            if isinstance(dataset, pd.DataFrame) and not dataset.empty and 'Date_Time' in dataset.columns:
                # Increment the index for simulation
                st.session_state.current_index += simulation_speed
                
                # Get real-time data from dataset
                data = get_real_time_data(dataset, turbine_id, st.session_state.current_index)
            else:
                # Get simulated data if no dataset
                data = get_real_time_data(dataset, turbine_id)
            
            # Predict efficiency using the model
            try:
                predicted_category = model.predict(data["features"])[0]
                if hasattr(model, 'predict_proba'):
                    probs = model.predict_proba(data["features"])[0]
                    # Convert classification to efficiency score
                    predicted_efficiency = (probs[1] * 0.5) + (probs[2] * 1.0) if len(probs) == 3 else 0.5
                else:
                    # Map categories 0, 1, 2 to efficiency values
                    efficiency_map = {0: 0.3, 1: 0.6, 2: 0.85}
                    predicted_efficiency = efficiency_map.get(predicted_category, 0.5)
            except Exception as e:
                # Use calculated efficiency if model fails
                predicted_efficiency = data["efficiency"]
            
            # Combine calculated and predicted efficiency
            # For a real system, you might use only the prediction or a weighted average
            final_efficiency = (data["efficiency"] + predicted_efficiency) / 2
            
            # Classify efficiency
            status, color = classify_efficiency(final_efficiency)
            
            # Add to history
            new_row = {
                "timestamp": data["timestamp"],
                "active_power": data["active_power"],
                "theoretical_power": data["theoretical_power"],
                "wind_speed": data["wind_speed"],
                "wind_direction": data["wind_direction"],
                "ambient_temp": data["ambient_temp"],
                "rotor_rpm": data["rotor_rpm"],
                "nacelle_position": data["nacelle_position"],
                "yaw_error": data["yaw_error"],
                "efficiency": final_efficiency,
                "status": status
            }
            
            st.session_state.history = pd.concat([
                st.session_state.history,
                pd.DataFrame([new_row])
            ], ignore_index=True).tail(100)  # Keep last 100 records
            
            # Display real-time metrics
            with metrics_section:
                st.subheader(f"Current Metrics for {turbine_id}")
                
                m1, m2, m3, m4 = st.columns(4)
                
                with m1:
                    # Calculate delta only if history has more than 1 row
                    wind_speed_delta = data['wind_speed'] - st.session_state.history['wind_speed'].iloc[-2] if len(st.session_state.history) > 1 else 0
                    st.metric("Wind Speed", f"{data['wind_speed']:.1f} m/s", f"{wind_speed_delta:.1f} m/s")
                    st.metric("Wind Direction", f"{data['wind_direction']:.1f}°")
                
                with m2:
                    power_delta = data['active_power'] - st.session_state.history['active_power'].iloc[-2] if len(st.session_state.history) > 1 else 0
                    st.metric("Active Power", f"{data['active_power']:.1f} kW", f"{power_delta:.1f} kW")
                    st.metric("Theoretical Power", f"{data['theoretical_power']:.1f} kW")
                
                with m3:
                    st.metric("Ambient Temp", f"{data['ambient_temp']:.1f} °C")
                    st.metric("Rotor RPM", f"{data['rotor_rpm']:.1f}")
                
                with m4:
                    efficiency_delta = final_efficiency - st.session_state.history['efficiency'].iloc[-2] if len(st.session_state.history) > 1 else 0
                    st.metric("Efficiency", f"{final_efficiency:.2f}", f"{efficiency_delta:.2f}")
                    
                    if status == "Good":
                        st.markdown(f"<div class='metric-card' style='background-color:rgba(0,128,0,0.2)'><h3 style='color:green'>STATUS: GOOD</h3></div>", unsafe_allow_html=True)
                    elif status == "Moderate":
                        st.markdown(f"<div class='metric-card' style='background-color:rgba(255,165,0,0.2)'><h3 style='color:orange'>STATUS: MODERATE</h3></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='metric-card' style='background-color:rgba(255,0,0,0.2)'><h3 style='color:red'>STATUS: POOR</h3></div>", unsafe_allow_html=True)
            
            # Display charts
            with chart_section:
                if not st.session_state.history.empty and len(st.session_state.history) > 1:
                    chart_cols = st.columns(2)
                    
                    with chart_cols[0]:
                        st.subheader("Efficiency Over Time")
                        history_df = st.session_state.history.copy()
                        history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                        
                        # Create color-mapped efficiency chart
                        fig = px.line(
                            history_df, 
                            x='timestamp', 
                            y='efficiency',
                            title="Turbine Efficiency Trend",
                            labels={"timestamp": "Time", "efficiency": "Efficiency"}
                        )
                        
                        # Add color-coded background regions
                        fig.add_shape(
                            type="rect",
                            x0=history_df['timestamp'].min(),
                            x1=history_df['timestamp'].max(),
                            y0=0,
                            y1=0.5,
                            fillcolor="rgba(255,0,0,0.1)",
                            line=dict(width=0),
                            layer="below"
                        )
                        fig.add_shape(
                            type="rect",
                            x0=history_df['timestamp'].min(),
                            x1=history_df['timestamp'].max(),
                            y0=0.5,
                            y1=0.75,
                            fillcolor="rgba(255,165,0,0.1)",
                            line=dict(width=0),
                            layer="below"
                        )
                        fig.add_shape(
                            type="rect",
                            x0=history_df['timestamp'].min(),
                            x1=history_df['timestamp'].max(),
                            y0=0.75,
                            y1=1.0,
                            fillcolor="rgba(0,128,0,0.1)",
                            line=dict(width=0),
                            layer="below"
                        )
                        
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with chart_cols[1]:
                        st.subheader("Power Output vs Wind Speed")
                        fig = px.scatter(
                            history_df,
                            x="wind_speed",
                            y="active_power",
                            color="efficiency",
                            size="rotor_rpm",
                            color_continuous_scale=["red", "yellow", "green"],
                            title="Power Output vs Wind Speed",
                            labels={
                                "wind_speed": "Wind Speed (m/s)",
                                "active_power": "Active Power (kW)",
                                "efficiency": "Efficiency"
                            }
                        )
                        
                        # Add theoretical power curve
                        wind_speeds = np.linspace(0, max(history_df["wind_speed"]) * 1.1, 100)
                        theoretical_powers = [min(0.5 * 1.225 * 8000 * 0.45 * ws**3, 2000) for ws in wind_speeds]
                        
                        fig.add_trace(
                            go.Scatter(
                                x=wind_speeds,
                                y=theoretical_powers,
                                mode='lines',
                                line=dict(color='rgba(0,0,0,0.7)', dash='dash'),
                                name='Theoretical Power'
                            )
                        )
                        
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                
                    # Additional charts
                    chart_cols2 = st.columns(2)
                    
                    with chart_cols2[0]:
                        st.subheader("Power and Wind Speed Over Time")
                        
                        # Create figure with secondary y-axis
                        fig = make_subplots(specs=[[{"secondary_y": True}]])
                        
                        # Add traces
                        fig.add_trace(
                            go.Scatter(
                                x=history_df['timestamp'],
                                y=history_df['active_power'],
                                name="Active Power (kW)",
                                line=dict(color="blue")
                            ),
                            secondary_y=False,
                        )
                        
                        fig.add_trace(
                            go.Scatter(
                                x=history_df['timestamp'],
                                y=history_df['wind_speed'],
                                name="Wind Speed (m/s)",
                                line=dict(color="green")
                            ),
                            secondary_y=True,
                        )
                        
                        # Set x-axis title
                        fig.update_xaxes(title_text="Time")
                        
                        # Set y-axes titles
                        fig.update_yaxes(title_text="Active Power (kW)", secondary_y=False)
                        fig.update_yaxes(title_text="Wind Speed (m/s)", secondary_y=True)
                        
                        fig.update_layout(
                            title="Power Output and Wind Speed Over Time",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with chart_cols2[1]:
                        st.subheader("Yaw Error Analysis")
                        
                        fig = px.scatter(
                            history_df,
                            x="yaw_error",
                            y="efficiency",
                            color="wind_speed",
                            size="active_power",
                            color_continuous_scale="Viridis",
                            title="Impact of Yaw Error on Efficiency",
                            labels={
                                "yaw_error": "Yaw Error (degrees)",
                                "efficiency": "Efficiency",
                                "wind_speed": "Wind Speed (m/s)",
                                "active_power": "Active Power (kW)"
                            }
                        )
                        
                        # Add trend line
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
            
            # Historical data table
            with history_section:
                st.subheader(f"Historical Data - {turbine_id}")
                
                # Format the dataframe for display
                display_df = st.session_state.history.copy()
                display_df['time'] = pd.to_datetime(display_df['timestamp']).dt.time
                
                # Prepare data for display
                cols_to_display = ['time', 'wind_speed', 'active_power', 'theoretical_power', 
                                  'efficiency', 'yaw_error', 'status']
                
                # Convert the dataframe to a format that can be displayed
                display_data = display_df[cols_to_display].rename(
                    columns={
                        'time': 'Time', 
                        'wind_speed': 'Wind Speed (m/s)', 
                        'active_power': 'Active Power (kW)',
                        'theoretical_power': 'Theoretical (kW)',
                        'efficiency': 'Efficiency',
                        'yaw_error': 'Yaw Error (°)',
                        'status': 'Status'
                    }
                )
                
                # Display the dataframe
                st.dataframe(
                    display_data.style.format({
                        'Wind Speed (m/s)': '{:.1f}',
                        'Active Power (kW)': '{:.1f}',
                        'Theoretical (kW)': '{:.1f}',
                        'Efficiency': '{:.3f}',
                        'Yaw Error (°)': '{:.1f}'
                    }),
                    use_container_width=True,
                    height=300
                )
            
            # Sleep to simulate refresh interval
            time.sleep(refresh_interval)
            
            # Trigger rerun to refresh data
            st.rerun()
    else:
        st.info("Click 'Start Monitoring' to begin real-time data collection and prediction.")

if __name__ == "__main__":
    show_page()
