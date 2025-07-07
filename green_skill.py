import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="🏠 Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .energy-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .appliance-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'energy_breakdown' not in st.session_state:
    st.session_state.energy_breakdown = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Smart Energy Consumption Calculator</h1>
    <p>Calculate your home's energy usage in Ahmedabad, Gujarat</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for user info
st.sidebar.header("👤 User Information")
name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age", min_value=1, max_value=100)
city = st.sidebar.text_input("City")
area = st.sidebar.text_input("Area")

st.sidebar.markdown("---")
st.sidebar.info(f"📍 Location: {area}, {city}")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🏠 Property Details")
    
    # Property type selection
    property_type = st.selectbox(
        "Select Property Type",
        ["Flat", "Tenament"],
        help="Choose the type of property you live in"
    )
    
    # BHK selection
    bhk_options = ["1BHK", "2BHK", "3BHK"]
    bhk = st.selectbox(
        "Select Number of BHK",
        bhk_options,
        help="Choose the size of your home"
    )
    
    st.markdown("---")
    
    # Appliances section
    st.header("🔌 Appliances")
    st.write("Select the appliances you have:")
    
    col_ac, col_fr, col_wm = st.columns(3)
    
    with col_ac:
        st.markdown('<div class="appliance-card">', unsafe_allow_html=True)
        st.markdown("❄️ **Air Conditioner**")
        do_ac = st.checkbox("I have AC", key="ac")
        st.markdown("Power: 3 kW")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_fr:
        st.markdown('<div class="appliance-card">', unsafe_allow_html=True)
        st.markdown("🧊 **Refrigerator**")
        do_fr = st.checkbox("I have Fridge", key="fridge")
        st.markdown("Power: 4 kW")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_wm:
        st.markdown('<div class="appliance-card">', unsafe_allow_html=True)
        st.markdown("🧺 **Washing Machine**")
        do_wm = st.checkbox("I have Washing Machine", key="washing")
        st.markdown("Power: 2 kW")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.header("📊 Energy Breakdown")
    
    # Calculate energy based on your original logic
    bhk_num = bhk_options.index(bhk) + 1
    
    # Base energy calculation (lights and fans)
    if bhk_num == 1:
        base_energy = 2 * 0.4 + 2 * 0.8  # 2.4 kW
        lights = 2
        fans = 2
    elif bhk_num == 2:
        base_energy = 3 * 0.4 + 3 * 0.8  # 3.6 kW
        lights = 3
        fans = 3
    else:  # 3BHK
        base_energy = 4 * 0.4 + 4 * 0.8  # 4.8 kW
        lights = 4
        fans = 4
    
    # Appliance energy
    appliance_energy = 0
    if do_ac:
        appliance_energy += 3
    if do_fr:
        appliance_energy += 4
    if do_wm:
        appliance_energy += 2
    
    total_energy = base_energy + appliance_energy
    
    # Store breakdown in session state
    st.session_state.energy_breakdown = {
        'Lights': lights * 0.4,
        'Fans': fans * 0.8,
        'AC': 3 if do_ac else 0,
        'Fridge': 4 if do_fr else 0,
        'Washing Machine': 2 if do_wm else 0
    }
    
    # Display total energy
    st.markdown(f"""
    <div class="energy-card">
        <h2>Total Energy Consumption</h2>
        <h1>{total_energy:.1f} kW</h1>
        <p>Estimated monthly cost: ₹{total_energy * 24 * 30 * 6:.0f}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Energy breakdown chart
    if total_energy > 0:
        st.markdown("### Energy Distribution")
        
        # Create pie chart
        breakdown_data = {k: v for k, v in st.session_state.energy_breakdown.items() if v > 0}
        
        fig = px.pie(
            values=list(breakdown_data.values()),
            names=list(breakdown_data.keys()),
            title="Energy Consumption by Appliance",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(
            font=dict(size=12),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# Bottom section with additional info
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Property Type", property_type)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("BHK", bhk)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Active Appliances", sum([do_ac, do_fr, do_wm]))
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("Daily Cost", f"₹{total_energy * 24 * 6:.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

# Energy saving tips
if total_energy > 0:
    st.markdown("---")
    st.header("💡 Energy Saving Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **💡 Lighting Tips:**
        - Use LED bulbs instead of incandescent
        - Turn off lights when not needed
        - Use natural light during day
        
        **🌀 Fan Tips:**
        - Clean fan blades regularly
        - Use ceiling fans with AC to save energy
        - Optimal fan speed saves electricity
        """)
    
    with tips_col2:
        if do_ac:
            st.markdown("""
            **❄️ AC Tips:**
            - Set temperature to 24°C or higher
            - Use timer function
            - Regular maintenance saves energy
            """)
        
        if do_fr:
            st.markdown("""
            **🧊 Fridge Tips:**
            - Don't overload the fridge
            - Keep it away from heat sources
            - Check door seals regularly
            """)
        
        if do_wm:
            st.markdown("""
            **🧺 Washing Machine Tips:**
            - Use cold water when possible
            - Run full loads only
            - Clean lint filters regularly
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🌱 Made with ❤️ for sustainable living in Ahmedabad | 
    ⚡ Energy consumption calculated based on standard appliance ratings</p>
</div>
""", unsafe_allow_html=True)