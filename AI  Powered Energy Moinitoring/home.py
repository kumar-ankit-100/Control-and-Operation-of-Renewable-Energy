import streamlit as st
import pandas as pd
import plotly.express as px

def show_page():
    st.title("Renewable Energy Solutions")
    st.markdown("### Sustainable power solutions for a greener future")
    
    # Introduction section
    st.markdown("""
    Welcome to our renewable energy platform. We offer cutting-edge solutions in four key renewable energy domains.
    Each solution is designed to maximize efficiency while minimizing environmental impact.
    """)
    
    # Display four energy cards in a 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="energy-card solar-card">
            <div class="card-title">Solar Energy</div>
            <p>Harness the power of the sun with our advanced photovoltaic systems. 
            Our solar solutions provide clean, renewable energy that can be deployed 
            in various scales from residential to industrial applications.</p>
            <p><strong>Efficiency:</strong> Up to 22%</p>
            <p><strong>Lifespan:</strong> 25-30 years</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="energy-card hydro-card">
            <div class="card-title">Hydroelectric Power</div>
            <p>Our micro-hydro solutions harness flowing water from rivers and streams 
            to generate consistent, reliable power with minimal environmental footprint. 
            Perfect for properties with water resources.</p>
            <p><strong>Efficiency:</strong> Up to 90%</p>
            <p><strong>Lifespan:</strong> 50+ years</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="energy-card wind-card">
            <div class="card-title">Wind Energy</div>
            <p>Our wind turbines are designed for maximum energy capture even in 
            moderate wind conditions. Available in various sizes to suit different 
            locations and energy requirements.</p>
            <p><strong>Efficiency:</strong> Up to 45%</p>
            <p><strong>Lifespan:</strong> 20-25 years</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="energy-card biomass-card">
            <div class="card-title">Biomass Energy</div>
            <p>Convert organic waste into valuable energy with our biomass solutions. 
            Our systems are designed to efficiently convert various organic materials 
            into heat and electricity.</p>
            <p><strong>Efficiency:</strong> Up to 85%</p>
            <p><strong>Lifespan:</strong> 15-20 years</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Overall comparison chart
    st.markdown("### Comparative Analysis")
    
    chart_data = pd.DataFrame({
        'Technology': ['Solar', 'Wind', 'Hydro', 'Biomass'],
        'Installation Cost ($/kW)': [1800, 1400, 2500, 3000],
        'Maintenance ($/kW/year)': [20, 40, 15, 70],
        'CO2 Reduction (tons/year/kW)': [0.7, 0.8, 0.9, 0.5]
    })
    
    tab1, tab2, tab3 = st.tabs(["Installation Cost", "Maintenance Cost", "Environmental Impact"])
    
    with tab1:
        fig = px.bar(chart_data, x='Technology', y='Installation Cost ($/kW)', 
                    color='Technology', color_discrete_sequence=['#ffcc00', '#00ccff', '#0066ff', '#33cc33'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.bar(chart_data, x='Technology', y='Maintenance ($/kW/year)', 
                    color='Technology', color_discrete_sequence=['#ffcc00', '#00ccff', '#0066ff', '#33cc33'])
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = px.bar(chart_data, x='Technology', y='CO2 Reduction (tons/year/kW)', 
                    color='Technology', color_discrete_sequence=['#ffcc00', '#00ccff', '#0066ff', '#33cc33'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Navigation buttons to pages
    st.markdown("### Explore Our Solutions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("☀️ Solar Energy", key="home_solar"):
            st.session_state.current_page = "solar"
            st.rerun()
    
    with col2:
        if st.button("🌬️ Wind Energy", key="home_wind"):
            st.session_state.current_page = "wind"
            st.rerun()
    
    with col3:
        if st.button("💧 Hydroelectric", key="home_hydro"):
            st.session_state.current_page = "hydro"
            st.rerun()
    
    with col4:
        if st.button("🌱 Biomass Energy", key="home_biomass"):
            st.session_state.current_page = "biomass"
            st.rerun()