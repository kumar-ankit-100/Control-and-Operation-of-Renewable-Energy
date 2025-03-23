import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pickle
import os
import calendar
from datetime import datetime
import time

# Set page configuration
# st.set_page_config(
#     page_title="Advanced India Solar Power Calculator",
#     page_icon="☀️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Constants - Expanded with Northeast states
STATES_WITH_SUBSIDY = {
    "Andhra Pradesh": {"residential": 40000, "commercial": 30000},
    "Arunachal Pradesh": {"residential": 15000, "commercial": 10000},
    "Assam": {"residential": 18000, "commercial": 12000},
    "Bihar": {"residential": 15000, "commercial": 10000},
    "Chhattisgarh": {"residential": 20000, "commercial": 15000},
    "Gujarat": {"residential": 20000, "commercial": 15000},
    "Haryana": {"residential": 20000, "commercial": 15000},
    "Himachal Pradesh": {"residential": 22000, "commercial": 16000},
    "Jharkhand": {"residential": 15000, "commercial": 10000},
    "Karnataka": {"residential": 25000, "commercial": 20000},
    "Kerala": {"residential": 30000, "commercial": 20000},
    "Madhya Pradesh": {"residential": 20000, "commercial": 15000},
    "Maharashtra": {"residential": 35000, "commercial": 25000},
    "Manipur": {"residential": 18000, "commercial": 12000},
    "Meghalaya": {"residential": 18000, "commercial": 12000},
    "Mizoram": {"residential": 18000, "commercial": 12000},
    "Nagaland": {"residential": 18000, "commercial": 12000},
    "Odisha": {"residential": 20000, "commercial": 15000},
    "Punjab": {"residential": 20000, "commercial": 15000},
    "Rajasthan": {"residential": 30000, "commercial": 20000},
    "Sikkim": {"residential": 18000, "commercial": 12000},
    "Tamil Nadu": {"residential": 40000, "commercial": 30000},
    "Telangana": {"residential": 30000, "commercial": 20000},
    "Tripura": {"residential": 18000, "commercial": 12000},
    "Uttar Pradesh": {"residential": 15000, "commercial": 10000},
    "Uttarakhand": {"residential": 20000, "commercial": 15000},
    "West Bengal": {"residential": 20000, "commercial": 15000},
}

SOLAR_RADIATION = {
    "North India": 5.5,
    "East India": 4.8,
    "West India": 6.0,
    "South India": 5.8,
    "Central India": 5.5,
    "Northeast India": 4.5,
}

# Monthly variation factors (percentage of annual average)
MONTHLY_VARIATION = {
    "North India": [0.8, 0.9, 1.0, 1.1, 1.2, 1.1, 0.9, 0.8, 0.9, 1.0, 1.0, 0.8],
    "East India": [0.8, 0.9, 1.0, 1.1, 1.1, 0.9, 0.8, 0.8, 0.9, 1.0, 1.0, 0.8],
    "West India": [0.9, 1.0, 1.1, 1.2, 1.2, 1.0, 0.8, 0.7, 0.8, 0.9, 0.9, 0.8],
    "South India": [1.0, 1.1, 1.2, 1.2, 1.1, 0.9, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9],
    "Central India": [0.9, 1.0, 1.1, 1.2, 1.2, 1.0, 0.8, 0.7, 0.8, 0.9, 0.9, 0.8],
    "Northeast India": [0.7, 0.8, 0.9, 1.0, 1.0, 0.8, 0.7, 0.7, 0.8, 0.9, 0.8, 0.7],
}

ELECTRICITY_RATES = {
    "Andhra Pradesh": {"residential": 8.50, "commercial": 10.50},
    "Arunachal Pradesh": {"residential": 7.00, "commercial": 9.00},
    "Assam": {"residential": 7.20, "commercial": 9.20},
    "Bihar": {"residential": 6.80, "commercial": 8.80},
    "Chhattisgarh": {"residential": 7.50, "commercial": 9.50},
    "Gujarat": {"residential": 7.80, "commercial": 9.80},
    "Haryana": {"residential": 7.50, "commercial": 9.50},
    "Himachal Pradesh": {"residential": 6.20, "commercial": 8.20},
    "Jharkhand": {"residential": 6.50, "commercial": 8.50},
    "Karnataka": {"residential": 8.20, "commercial": 10.20},
    "Kerala": {"residential": 7.90, "commercial": 9.90},
    "Madhya Pradesh": {"residential": 7.30, "commercial": 9.30},
    "Maharashtra": {"residential": 9.50, "commercial": 11.50},
    "Manipur": {"residential": 7.00, "commercial": 9.00},
    "Meghalaya": {"residential": 6.80, "commercial": 8.80},
    "Mizoram": {"residential": 6.90, "commercial": 8.90},
    "Nagaland": {"residential": 7.00, "commercial": 9.00},
    "Odisha": {"residential": 7.20, "commercial": 9.20},
    "Punjab": {"residential": 7.50, "commercial": 9.50},
    "Rajasthan": {"residential": 8.00, "commercial": 10.00},
    "Sikkim": {"residential": 6.50, "commercial": 8.50},
    "Tamil Nadu": {"residential": 8.50, "commercial": 10.50},
    "Telangana": {"residential": 8.20, "commercial": 10.20},
    "Tripura": {"residential": 6.90, "commercial": 8.90},
    "Uttar Pradesh": {"residential": 7.00, "commercial": 9.00},
    "Uttarakhand": {"residential": 6.80, "commercial": 8.80},
    "West Bengal": {"residential": 7.50, "commercial": 9.50},
}

NET_METERING_RATES = {
    "Andhra Pradesh": {"residential": 6.00, "commercial": 5.00},
    "Arunachal Pradesh": {"residential": 5.00, "commercial": 4.00},
    "Assam": {"residential": 5.20, "commercial": 4.20},
    "Bihar": {"residential": 4.80, "commercial": 3.80},
    "Chhattisgarh": {"residential": 5.30, "commercial": 4.30},
    "Gujarat": {"residential": 5.50, "commercial": 4.50},
    "Haryana": {"residential": 5.30, "commercial": 4.30},
    "Himachal Pradesh": {"residential": 4.50, "commercial": 3.50},
    "Jharkhand": {"residential": 4.70, "commercial": 3.70},
    "Karnataka": {"residential": 5.80, "commercial": 4.80},
    "Kerala": {"residential": 5.70, "commercial": 4.70},
    "Madhya Pradesh": {"residential": 5.20, "commercial": 4.20},
    "Maharashtra": {"residential": 6.50, "commercial": 5.50},
    "Manipur": {"residential": 5.00, "commercial": 4.00},
    "Meghalaya": {"residential": 4.80, "commercial": 3.80},
    "Mizoram": {"residential": 4.90, "commercial": 3.90},
    "Nagaland": {"residential": 5.00, "commercial": 4.00},
    "Odisha": {"residential": 5.10, "commercial": 4.10},
    "Punjab": {"residential": 5.30, "commercial": 4.30},
    "Rajasthan": {"residential": 5.70, "commercial": 4.70},
    "Sikkim": {"residential": 4.70, "commercial": 3.70},
    "Tamil Nadu": {"residential": 6.20, "commercial": 5.20},
    "Telangana": {"residential": 5.90, "commercial": 4.90},
    "Tripura": {"residential": 4.90, "commercial": 3.90},
    "Uttar Pradesh": {"residential": 5.00, "commercial": 4.00},
    "Uttarakhand": {"residential": 4.80, "commercial": 3.80},
    "West Bengal": {"residential": 5.20, "commercial": 4.20},
}

PANEL_EFFICIENCY = {
    "Monocrystalline": 0.20,
    "Polycrystalline": 0.17,
    "Thin Film": 0.12,
    "Bifacial": 0.22,
    "PERC": 0.21,
    "HJT": 0.23,
}

PANEL_COST_PER_KW = {
    "Monocrystalline": 45000,
    "Polycrystalline": 40000,
    "Thin Film": 35000,
    "Bifacial": 50000,
    "PERC": 47000,
    "HJT": 55000,
}

BATTERY_TYPES = {
    "Lithium-Ion": {"cost_per_kwh": 10000, "life_cycles": 4000, "efficiency": 0.95},
    "Lead-Acid": {"cost_per_kwh": 6000, "life_cycles": 1500, "efficiency": 0.80},
    "Flow": {"cost_per_kwh": 15000, "life_cycles": 10000, "efficiency": 0.85},
}

INVERTER_TYPES = {
    "String Inverter": {"cost_per_kw": 7000, "efficiency": 0.96, "life_years": 10},
    "Microinverter": {"cost_per_kw": 12000, "efficiency": 0.98, "life_years": 15},
    "Hybrid Inverter": {"cost_per_kw": 15000, "efficiency": 0.97, "life_years": 12},
}

REGION_MAPPING = {
    "Andhra Pradesh": "South India",
    "Arunachal Pradesh": "Northeast India",
    "Assam": "Northeast India",
    "Bihar": "East India",
    "Chhattisgarh": "Central India",
    "Gujarat": "West India",
    "Haryana": "North India",
    "Himachal Pradesh": "North India",
    "Jharkhand": "East India",
    "Karnataka": "South India",
    "Kerala": "South India",
    "Madhya Pradesh": "Central India",
    "Maharashtra": "West India",
    "Manipur": "Northeast India",
    "Meghalaya": "Northeast India",
    "Mizoram": "Northeast India",
    "Nagaland": "Northeast India",
    "Odisha": "East India",
    "Punjab": "North India",
    "Rajasthan": "North India",
    "Sikkim": "Northeast India",
    "Tamil Nadu": "South India",
    "Telangana": "South India",
    "Tripura": "Northeast India",
    "Uttar Pradesh": "North India",
    "Uttarakhand": "North India",
    "West Bengal": "East India",
}

# Custom CSS for better UI
st.markdown("""
<style>
    body {
        background: linear-gradient(to bottom, #e0f7fa, #ffffff);
        font-family: 'Arial', sans-serif;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0c3866;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0c3866;
        margin-bottom: 10px;
    }
    .section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .warning-box {
        background-color: #fff8e1;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stProgress > div > div > div {
        background-color: #4CAF50;
    }
    .recommendation {
        background-color: #f1f8e9;
        padding: 15px;
        border-radius: 5px;
        margin-top: 5px;
        border-left: 5px solid #8bc34a;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .animated-button {
        background-color: #ffcc00;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.3s;
    }
    .animated-button:hover {
        background-color: #ff9900;
        transform: scale(1.05);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #ffcc00, #ff9900);
    }
    .stButton>button {
        background-color: #ffcc00;
        color: #ffffff;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff9900;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize ML models
def initialize_ml_models():
    try:
        # Create models directory if it doesn't exist
        os.makedirs("models", exist_ok=True)
        
        # Generation model
        if not os.path.exists("models/solar_generation_model.pkl"):
            generation_model = RandomForestRegressor(n_estimators=100, random_state=42)
            # Create synthetic training data
            X = np.random.rand(1000, 6)  # [capacity, radiation, temp, angle, age, efficiency]
            y = X[:, 0] * 5.0 * X[:, 1] * (1 - 0.005 * X[:, 3]) * (1 - 0.005 * (X[:, 2] - 25)) * (1 - 0.01 * X[:, 4]) * (X[:, 5] * 5)
            generation_model.fit(X, y)
            with open("models/solar_generation_model.pkl", "wb") as f:
                pickle.dump(generation_model, f)
        else:
            with open("models/solar_generation_model.pkl", "rb") as f:
                generation_model = pickle.load(f)
        
        # Recommendation model - a simple clustering model
        if not os.path.exists("models/recommendation_model.pkl"):
            recommendation_model = KMeans(n_clusters=5, random_state=42)
            # Create synthetic user profiles
            profiles = np.random.rand(200, 5)  # [consumption, budget, area, electricity_rate, radiation]
            recommendation_model.fit(profiles)
            with open("models/recommendation_model.pkl", "wb") as f:
                pickle.dump(recommendation_model, f)
        else:
            with open("models/recommendation_model.pkl", "rb") as f:
                recommendation_model = pickle.load(f)
        
        # ROI prediction model
        if not os.path.exists("models/roi_prediction_model.pkl"):
            roi_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            # Create synthetic data
            X = np.random.rand(1000, 7)  # [capacity, cost, savings, radiation, temp, lifespan, maintenance]
            y = (X[:, 2] * X[:, 4] * 365 * X[:, 5]) / (X[:, 1] + X[:, 6] * X[:, 5]) * 100
            roi_model.fit(X, y)
            with open("models/roi_prediction_model.pkl", "wb") as f:
                pickle.dump(roi_model, f)
        else:
            with open("models/roi_prediction_model.pkl", "rb") as f:
                roi_model = pickle.load(f)
        
        # Initialize scalers
        gen_scaler = StandardScaler()
        gen_scaler.fit(np.random.rand(100, 6))
        
        rec_scaler = StandardScaler()
        rec_scaler.fit(np.random.rand(100, 5))
        
        roi_scaler = StandardScaler()
        roi_scaler.fit(np.random.rand(100, 7))
        
        return generation_model, recommendation_model, roi_model, gen_scaler, rec_scaler, roi_scaler
    
    except Exception as e:
        st.error(f"Error initializing ML models: {e}")
        return None, None, None, None, None, None

# Calculate monthly solar generation with seasonal variation
def calculate_monthly_generation(annual_generation, region):
    monthly_factors = MONTHLY_VARIATION[region]
    monthly_generation = []
    
    for factor in monthly_factors:
        monthly_gen = (annual_generation / 12) * factor
        monthly_generation.append(monthly_gen)
    
    return monthly_generation

# Calculate recommended system size based on consumption
def calculate_recommended_system(monthly_consumption, roof_area, budget, panel_efficiency, panel_cost_per_kw):
    # Estimate kWh per kW per day (assume 4 peak sun hours on average)
    daily_kwh_per_kw = 4 * panel_efficiency / 0.17  # Normalized to polycrystalline
    
    # Calculate system size based on consumption
    required_system_kw = (monthly_consumption / 30) / daily_kwh_per_kw
    
    # Calculate system size based on roof area (assume 10 sq.m per kW)
    roof_area_system_kw = roof_area / 10
    
    # Calculate system size based on budget
    budget_system_kw = budget / panel_cost_per_kw
    
    # Return the minimum of the three constraints
    return min(required_system_kw, roof_area_system_kw, budget_system_kw)

# Generate recommendations based on user inputs and clustering model
def generate_recommendations(recommendation_model, rec_scaler, user_type, state, monthly_consumption, budget, roof_area):
    try:
        # Prepare user profile for clustering
        electricity_rate = ELECTRICITY_RATES[state][user_type]
        region = REGION_MAPPING[state]
        radiation = SOLAR_RADIATION[region]
        
        user_profile = np.array([[monthly_consumption, budget, roof_area, electricity_rate, radiation]])
        user_profile_scaled = rec_scaler.transform(user_profile)
        
        # Predict cluster
        cluster = recommendation_model.predict(user_profile_scaled)[0]
        
        # Generate recommendations based on cluster
        if cluster == 0:  # Low consumption, low budget
            panel_recommendation = "Polycrystalline"
            battery_recommendation = "No battery storage recommended for your budget"
            inverter_recommendation = "String Inverter"
            financing_recommendation = "Consider government subsidies and low-interest solar loans"
        elif cluster == 1:  # High consumption, high budget
            panel_recommendation = "Monocrystalline or PERC"
            battery_recommendation = "Lithium-Ion battery storage recommended"
            inverter_recommendation = "Hybrid Inverter"
            financing_recommendation = "Consider power purchase agreement (PPA) or solar lease"
        elif cluster == 2:  # Medium consumption, medium budget
            panel_recommendation = "Monocrystalline"
            battery_recommendation = "Small Lithium-Ion battery for critical loads"
            inverter_recommendation = "String Inverter"
            financing_recommendation = "Explore solar loans with extended payment terms"
        elif cluster == 3:  # Low consumption, high budget
            panel_recommendation = "HJT or Bifacial"
            battery_recommendation = "Lithium-Ion battery for energy independence"
            inverter_recommendation = "Microinverter"
            financing_recommendation = "Consider outright purchase for maximum long-term savings"
        else:  # High consumption, low budget
            panel_recommendation = "Polycrystalline"
            battery_recommendation = "Consider Lead-Acid battery as a lower-cost option"
            inverter_recommendation = "String Inverter"
            financing_recommendation = "Start with a smaller system and expand later"
            
        return {
            "panel": panel_recommendation,
            "battery": battery_recommendation,
            "inverter": inverter_recommendation,
            "financing": financing_recommendation,
            "cluster": cluster,
        }
    
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return None

# Calculate CO2 emissions reduction
def calculate_co2_reduction(annual_generation):
    # Average CO2 emissions factor for Indian grid electricity (kg CO2 per kWh)
    co2_factor = 0.82
    return annual_generation * co2_factor

# Perform detailed financial calculations
def calculate_financials(system_capacity, panel_type, include_battery, battery_type, battery_capacity, 
                         inverter_type, state, user_type, region, lifespan, annual_generation):
    try:
        # Calculate system costs
        panel_cost = system_capacity * PANEL_COST_PER_KW[panel_type]
        inverter_cost = system_capacity * INVERTER_TYPES[inverter_type]["cost_per_kw"]
        
        # Installation cost (estimated at 20% of panel cost)
        installation_cost = panel_cost * 0.2
        
        # Battery cost if applicable
        battery_cost = 0
        if include_battery:
            battery_cost = battery_capacity * BATTERY_TYPES[battery_type]["cost_per_kwh"]
            
        # Calculate total cost
        total_cost = panel_cost + inverter_cost + installation_cost + battery_cost
        
        # Apply subsidy
        subsidy = STATES_WITH_SUBSIDY[state][user_type]
        net_cost = total_cost - subsidy
        
        # Calculate annual savings
        electricity_rate = ELECTRICITY_RATES[state][user_type]
        annual_savings = annual_generation * electricity_rate
        
        # Calculate maintenance costs (estimated at 1% of total cost per year)
        annual_maintenance = total_cost * 0.01
        
        # Calculate inverter replacement cost
        inverter_life = INVERTER_TYPES[inverter_type]["life_years"]
        inverter_replacements = max(0, int(lifespan / inverter_life) - 1)
        inverter_replacement_cost = inverter_replacements * inverter_cost
        
        # Calculate battery replacement cost if applicable
        battery_replacement_cost = 0
        if include_battery:
            battery_life_years = (BATTERY_TYPES[battery_type]["life_cycles"] * 0.8) / 365  # Assuming 1 cycle per day
            battery_replacements = max(0, int(lifespan / battery_life_years) - 1)
            battery_replacement_cost = battery_replacements * battery_cost
            
        # Calculate total lifetime cost
        lifetime_maintenance = annual_maintenance * lifespan
        lifetime_cost = net_cost + lifetime_maintenance + inverter_replacement_cost + battery_replacement_cost
        
        # Calculate total lifetime savings
        # Assuming 0.5% panel degradation per year
        total_lifetime_generation = 0
        for year in range(lifespan):
            degradation_factor = 1 - (0.005 * year)
            total_lifetime_generation += annual_generation * degradation_factor
            
        total_lifetime_savings = total_lifetime_generation * electricity_rate
        
        # Calculate ROI, NPV, and payback period
        roi = ((total_lifetime_savings - lifetime_cost) / lifetime_cost) * 100
        
        # NPV calculation (simplified, assuming 7% discount rate)
        discount_rate = 0.07
        npv = -net_cost
        for year in range(1, lifespan + 1):
            degradation_factor = 1 - (0.005 * (year - 1))
            annual_saving = annual_generation * degradation_factor * electricity_rate
            annual_cost = annual_maintenance
            
            # Add inverter replacement cost if applicable
            if year % inverter_life == 0 and year != lifespan:
                annual_cost += inverter_cost
                
            # Add battery replacement cost if applicable
            if include_battery and year % int(battery_life_years) == 0 and year != lifespan:
                annual_cost += battery_cost
                
            net_cash_flow = annual_saving - annual_cost
            npv += net_cash_flow / ((1 + discount_rate) ** year)
            
        # Calculate simple payback period
        simple_payback = net_cost / (annual_savings - annual_maintenance)
        
        # Calculate discounted payback period (more accurate)
        discounted_payback = 0
        cumulative_savings = 0
        for year in range(1, lifespan + 1):
            degradation_factor = 1 - (0.005 * (year - 1))
            annual_saving = annual_generation * degradation_factor * electricity_rate
            annual_cost = annual_maintenance
            net_cash_flow = annual_saving - annual_cost
            discounted_cash_flow = net_cash_flow / ((1 + discount_rate) ** year)
            cumulative_savings += discounted_cash_flow
            
            if cumulative_savings >= net_cost and discounted_payback == 0:
                # Interpolate for more accurate result
                previous_savings = cumulative_savings - discounted_cash_flow
                fraction = (net_cost - previous_savings) / discounted_cash_flow
                discounted_payback = year - 1 + fraction
        
        return {
            "panel_cost": panel_cost,
            "inverter_cost": inverter_cost,
            "installation_cost": installation_cost,
            "battery_cost": battery_cost,
            "total_cost": total_cost,
            "subsidy": subsidy,
            "net_cost": net_cost,
            "annual_savings": annual_savings,
            "annual_maintenance": annual_maintenance,
            "lifetime_maintenance": lifetime_maintenance,
            "inverter_replacement_cost": inverter_replacement_cost,
            "battery_replacement_cost": battery_replacement_cost,
            "lifetime_cost": lifetime_cost,
            "total_lifetime_generation": total_lifetime_generation,
            "total_lifetime_savings": total_lifetime_savings,
            "roi": roi,
            "npv": npv,
            "simple_payback": simple_payback,
            "discounted_payback": discounted_payback,
        }
    
    except Exception as e:
        st.error(f"Error calculating financials: {e}")
        return None

# Perform calculations
def perform_calculations(user_type, state, monthly_consumption, monthly_bill, roof_area, system_capacity, 
                         budget, lifespan, panel_type, roof_angle, include_battery, battery_type, battery_capacity,
                         inverter_type, generation_model, gen_scaler, roi_model, roi_scaler):
    
    if generation_model is None or gen_scaler is None:
        st.error("ML models not initialized. Please restart the application.")
        return None
    
    try:
        # Get region
        region = REGION_MAPPING[state]
        
        # Get radiation
        avg_radiation = SOLAR_RADIATION[region]
        
        # Estimate average temperature
        avg_temp = 25  # Simplified assumption
        
        # Get panel efficiency
        panel_efficiency = PANEL_EFFICIENCY[panel_type]
        
        # Prepare input data for the generation model
        system_age = 0  # New system
        
        input_data = np.array([[system_capacity, avg_radiation, avg_temp, roof_angle, system_age, panel_efficiency]])
        input_data_scaled = gen_scaler.transform(input_data)
        
        # Predict annual generation
        annual_generation = generation_model.predict(input_data_scaled)[0]
        
        # Calculate monthly generation with seasonal variation
        monthly_generation = calculate_monthly_generation(annual_generation, region)
        
        # Calculate savings
        electricity_rate = ELECTRICITY_RATES[state][user_type]
        monthly_savings = [gen * electricity_rate / 1000 for gen in monthly_generation]
        
        # Calculate net metering income
        net_metering_rate = NET_METERING_RATES[state][user_type]
        net_metering_income = annual_generation * net_metering_rate / 12
        
        # Calculate financials
        financials = calculate_financials(
            system_capacity, panel_type, include_battery, battery_type, battery_capacity,
            inverter_type, state, user_type, region, lifespan, annual_generation
        )
        
        # Calculate CO2 reduction
        co2_reduction = calculate_co2_reduction(annual_generation)
        
        # Calculate trees equivalent (average tree absorbs 21 kg CO2 per year)
        trees_equivalent = co2_reduction / 21
        
        # Calculate export vs. self-consumption (assume 70% self-consumption)
        self_consumption_ratio = 0.7
        self_consumption = annual_generation * self_consumption_ratio
        export_to_grid = annual_generation * (1 - self_consumption_ratio)
        
        # Calculate grid dependency reduction
        grid_dependency_reduction = (self_consumption / (monthly_consumption * 12)) * 100
        
        # Calculate energy security metrics
        if include_battery:
            # Calculate days of autonomy
            daily_consumption = monthly_consumption / 30
            days_of_autonomy = (battery_capacity * BATTERY_TYPES[battery_type]["efficiency"]) / daily_consumption
            
            # Calculate resilience score (0-10)
            resilience_score = min(10, days_of_autonomy * 2)
        else:
            days_of_autonomy = 0
            resilience_score = 0
        
        # Prepare results
        results = {
            "annual_generation": annual_generation,
            "monthly_generation": monthly_generation,
            "monthly_savings": monthly_savings,
            "net_metering_income": net_metering_income,
            "financials": financials,
            "co2_reduction": co2_reduction,
            "trees_equivalent": trees_equivalent,
            "self_consumption": self_consumption,
            "export_to_grid": export_to_grid,
            "grid_dependency_reduction": grid_dependency_reduction,
            "days_of_autonomy": days_of_autonomy,
            "resilience_score": resilience_score,
        }
        
        return results
    
    except Exception as e:
        st.error(f"Error in perform_calculations: {e}")
        return None

# Create system size recommendation
def get_system_size_recommendation(monthly_consumption, roof_area, budget, panel_type):
    panel_cost_per_kw = PANEL_COST_PER_KW[panel_type]
    panel_efficiency = PANEL_EFFICIENCY[panel_type]
    return calculate_recommended_system(monthly_consumption, roof_area, budget, panel_efficiency, panel_cost_per_kw)

# Main application
def show_page():
    st.markdown("<h1 class='main-header'>Advanced India Solar Power Calculator</h1>", unsafe_allow_html=True)
    
    # Initialize models
    generation_model, recommendation_model, roi_model, gen_scaler, rec_scaler, roi_scaler = initialize_ml_models()
    
    # Sidebar inputs
    st.sidebar.header("User Inputs")
    user_type = st.sidebar.selectbox("Installation Type", ["residential", "commercial"])
    state = st.sidebar.selectbox("State", sorted(ELECTRICITY_RATES.keys()))
    monthly_consumption = st.sidebar.number_input("Monthly Electricity Consumption (kWh)", min_value=0.0, value=300.0)
    monthly_bill = st.sidebar.number_input("Monthly Electricity Bill (₹)", min_value=0.0, value=2400.0)
    roof_area = st.sidebar.number_input("Available Roof Area (sq.m)", min_value=0.0, value=50.0)
    system_capacity = st.sidebar.number_input("System Capacity (kW)", min_value=0.0, value=5.0)
    budget = st.sidebar.number_input("Budget (₹)", min_value=0.0, value=200000.0)
    lifespan = st.sidebar.number_input("Expected System Lifespan (years)", min_value=1, value=25)
    panel_type = st.sidebar.selectbox("Panel Type", list(PANEL_EFFICIENCY.keys()))
    roof_angle = st.sidebar.number_input("Roof Angle (degrees)", min_value=0.0, value=30.0)
    include_battery = st.sidebar.checkbox("Include Battery Storage", value=False)
    battery_type = st.sidebar.selectbox("Battery Type", list(BATTERY_TYPES.keys())) if include_battery else None
    battery_capacity = st.sidebar.number_input("Battery Capacity (kWh)", min_value=0.0, value=10.0) if include_battery else 0.0
    inverter_type = st.sidebar.selectbox("Inverter Type", list(INVERTER_TYPES.keys()))
    
    # Perform calculations
    if st.sidebar.button("Calculate"):
        results = perform_calculations(user_type, state, monthly_consumption, monthly_bill, roof_area, system_capacity, 
                                       budget, lifespan, panel_type, roof_angle, include_battery, battery_type, battery_capacity,
                                       inverter_type, generation_model, gen_scaler, roi_model, roi_scaler)
        if results:
            st.markdown("<h2 class='sub-header'>Calculation Results</h2>", unsafe_allow_html=True)
            st.write(f"**Annual Generation:** {results['annual_generation']:.2f} kWh")
            
            # Display monthly generation as a bar chart
            monthly_gen_df = pd.DataFrame({
                "Month": calendar.month_name[1:],
                "Generation (kWh)": results['monthly_generation']
            })
            fig = px.bar(monthly_gen_df, x="Month", y="Generation (kWh)", title="Monthly Solar Generation")
            st.plotly_chart(fig)
            
            st.write(f"**Monthly Savings:** ₹{sum(results['monthly_savings']):.2f}")
            st.write(f"**Net Metering Income:** ₹{results['net_metering_income']:.2f}")
            st.write(f"**CO2 Reduction:** {results['co2_reduction']:.2f} kg")
            st.write(f"**Equivalent Trees Planted:** {results['trees_equivalent']:.2f}")
            st.write(f"**Self-Consumption:** {results['self_consumption']:.2f} kWh")
            st.write(f"**Export to Grid:** {results['export_to_grid']:.2f} kWh")
            st.write(f"**Grid Dependency Reduction:** {results['grid_dependency_reduction']:.2f}%")
            st.write(f"**Days of Autonomy:** {results['days_of_autonomy']:.2f}")
            st.write(f"**Resilience Score:** {results['resilience_score']:.2f}")
            
            # Display financials
            st.markdown("<h2 class='sub-header'>Financial Analysis</h2>", unsafe_allow_html=True)
            st.write(f"**Panel Cost:** ₹{results['financials']['panel_cost']:.2f}")
            st.write(f"**Inverter Cost:** ₹{results['financials']['inverter_cost']:.2f}")
            st.write(f"**Installation Cost:** ₹{results['financials']['installation_cost']:.2f}")
            st.write(f"**Battery Cost:** ₹{results['financials']['battery_cost']:.2f}")
            st.write(f"**Total Cost:** ₹{results['financials']['total_cost']:.2f}")
            st.write(f"**Subsidy:** ₹{results['financials']['subsidy']:.2f}")
            st.write(f"**Net Cost:** ₹{results['financials']['net_cost']:.2f}")
            st.write(f"**Annual Savings:** ₹{results['financials']['annual_savings']:.2f}")
            st.write(f"**Annual Maintenance:** ₹{results['financials']['annual_maintenance']:.2f}")
            st.write(f"**Lifetime Maintenance:** ₹{results['financials']['lifetime_maintenance']:.2f}")
            st.write(f"**Inverter Replacement Cost:** ₹{results['financials']['inverter_replacement_cost']:.2f}")
            st.write(f"**Battery Replacement Cost:** ₹{results['financials']['battery_replacement_cost']:.2f}")
            st.write(f"**Lifetime Cost:** ₹{results['financials']['lifetime_cost']:.2f}")
            st.write(f"**Total Lifetime Generation:** {results['financials']['total_lifetime_generation']:.2f} kWh")
            st.write(f"**Total Lifetime Savings:** ₹{results['financials']['total_lifetime_savings']:.2f}")
            st.write(f"**ROI:** {results['financials']['roi']:.2f}%")
            st.write(f"**NPV:** ₹{results['financials']['npv']:.2f}")
            st.write(f"**Simple Payback:** {results['financials']['simple_payback']:.2f} years")
            st.write(f"**Discounted Payback:** {results['financials']['discounted_payback']:.2f} years")
    
    # Generate recommendations
    if st.sidebar.button("Generate Recommendations"):
        recommendations = generate_recommendations(recommendation_model, rec_scaler, user_type, state, monthly_consumption, budget, roof_area)
        if recommendations:
            st.markdown("<h2 class='sub-header'>System Recommendations</h2>", unsafe_allow_html=True)
            st.write(f"**Recommended Panel Type:** {recommendations['panel']}")
            st.write(f"**Recommended Battery:** {recommendations['battery']}")
            st.write(f"**Recommended Inverter:** {recommendations['inverter']}")
            st.write(f"**Financing Recommendation:** {recommendations['financing']}")
            st.write(f"**User Profile Cluster:** {recommendations['cluster']}")

if __name__ == "__main__":
    show_page()