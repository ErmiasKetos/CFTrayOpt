import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from reagent_optimizer import ReagentOptimizer
from datetime import datetime
from collections import defaultdict
import importlib
import gspread
from google.oauth2.service_account import Credentials
import os

# Set page config
st.set_page_config(
    page_title="Reagent Tray Configurator Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS (unchanged)
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
    }
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stExpander {
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    .info-box {
        background-color: #e1f5fe;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .header-box {
        background-color: #f1f8e9;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Function to check for required modules
def check_required_modules():
    required_modules = ['gspread', 'google.oauth2']
    missing_modules = []
    for module in required_modules:
        if importlib.util.find_spec(module) is None:
            missing_modules.append(module)
    return missing_modules

# Function to initialize Google Sheets connection
def init_google_sheets():
    missing_modules = check_required_modules()
    if missing_modules:
        st.error(f"The following required modules are missing: {', '.join(missing_modules)}")
        st.info("Please install the missing modules using the following command:")
        st.code("pip install gspread google-auth")
        return None

    try:
        import gspread
        from google.oauth2.service_account import Credentials

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file('path/to/your/credentials.json', scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key('17w0SV6waugh6oc0hrGS7i2FcOFC3jnvc').worksheet('KCFtray2024')
        return sheet
    except Exception as e:
        st.error(f"Error initializing Google Sheets: {str(e)}")
        return None

# Function to update KCFtray2024.csv
def update_kcf_summary(data):
    sheet = init_google_sheets()
    if sheet:
        try:
            sheet.append_row(data)
            return True
        except Exception as e:
            st.error(f"Error updating KCF summary: {str(e)}")
    return False

# Function to check if KCFtray2024.csv exists and is up-to-date
def check_kcf_summary():
    sheet = init_google_sheets()
    if sheet:
        try:
            values = sheet.get_all_values()
            if len(values) > 1:  # Assuming the first row is headers
                return True
        except Exception as e:
            st.error(f"Error accessing KCFtray2024.csv: {str(e)}")
    return False

# Rest of the functions remain unchanged
# ... (keep all other functions as they were)

def display_results(config, selected_experiments, customer_info):
    # Display results here... (This function was not provided in the original code)
    pass

def reset_app():
    # Reset app state here... (This function was not provided in the original code)
    pass

def main():
    st.title("🧪 Reagent Tray Configurator")
    
    # Initialize session state
    if 'config' not in st.session_state:
        st.session_state.config = None
    if 'selected_experiments' not in st.session_state:
        st.session_state.selected_experiments = []
    if 'daily_counts' not in st.session_state:
        st.session_state.daily_counts = {}

    # Check for required modules
    missing_modules = check_required_modules()
    if missing_modules:
        st.warning("Google Sheets integration is not available. Some features will be limited.")
        st.info("To enable full functionality, please install the required modules:")
        st.code("pip install gspread google-auth")
    else:
        # Check KCFtray2024.csv status
        if not check_kcf_summary():
            st.warning("KCFtray2024.csv is not accessible. Some features will be limited.")

    # Customer Information Section
    st.sidebar.markdown("### 📝 Customer Information")
    customer_name = st.sidebar.text_input("Customer Name", key="customer_name")
    unit_location = st.sidebar.text_input("Unit Location", key="unit_location")
    config_date = st.sidebar.date_input("Configuration Date", datetime.now())
    operator_name = st.sidebar.text_input("Operator Name", key="operator_name")

    customer_info = {
        "name": customer_name,
        "unit": unit_location,
        "date": config_date,
        "operator": operator_name
    }

    # Reset Button
    if st.sidebar.button("🔄 Reset All", key="reset_button"):
        reset_app()
        st.rerun()

    optimizer = ReagentOptimizer()
    experiments = optimizer.get_available_experiments()

    # Experiment Selection Section
    st.sidebar.markdown("### 1️⃣ Select Experiments")
    
    # Group experiments by type
    exp_types = {
        "LR": [exp for exp in experiments if "(LR)" in exp["name"]],
        "HR": [exp for exp in experiments if "(HR)" in exp["name"]],
        "Other": [exp for exp in experiments if "(LR)" not in exp["name"] and "(HR)" not in exp["name"]]
    }

    selected_experiments = []
    
    # Create tabs for experiment types
    tab_lr, tab_hr, tab_other = st.sidebar.tabs(["Low Range", "High Range", "Other"])
    
    with tab_lr:
        for exp in exp_types["LR"]:
            if st.checkbox(f"{exp['id']}: {exp['name']}", key=f"exp_{exp['id']}"):
                selected_experiments.append(exp['id'])
    
    with tab_hr:
        for exp in exp_types["HR"]:
            if st.checkbox(f"{exp['id']}: {exp['name']}", key=f"exp_{exp['id']}_hr"):
                selected_experiments.append(exp['id'])
    
    with tab_other:
        for exp in exp_types["Other"]:
            if st.checkbox(f"{exp['id']}: {exp['name']}", key=f"exp_{exp['id']}_other"):
                selected_experiments.append(exp['id'])

    # Manual Input Option
    st.sidebar.markdown("---")
    st.sidebar.markdown("Or enter experiment numbers manually:")
    manual_input = st.sidebar.text_input(
        "Experiment numbers (comma-separated)", 
        placeholder="e.g., 1, 16, 29"
    )

    if manual_input:
        selected_experiments = [int(num.strip()) for num in manual_input.split(',') if num.strip()]

    # Show current locations status
    if selected_experiments:
        total_locations_needed = sum(len(optimizer.experiment_data[exp]["reagents"]) 
                                   for exp in selected_experiments)
        st.sidebar.markdown(f"""
        <div style='padding: 10px; background-color: #e1f5fe; border-radius: 5px;'>
            <strong>Initial Locations Required:</strong> {total_locations_needed}
            <br><small>Additional sets will be added to optimize days of operation</small>
        </div>
        """, unsafe_allow_html=True)

        # Daily Count Input
        st.sidebar.markdown("### 2️⃣ Enter Daily Test Counts")
        daily_counts = {}
        
        for exp_id in selected_experiments:
            exp_name = next(exp['name'] for exp in experiments if exp['id'] == exp_id)
            count = st.sidebar.number_input(
                f"#{exp_id}: {exp_name}",
                min_value=1,
                value=st.session_state.daily_counts.get(exp_id, 1),
                key=f"daily_count_{exp_id}"
            )
            daily_counts[exp_id] = count
            st.session_state.daily_counts = daily_counts

        # Information about current selection
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Current Selection")
        st.sidebar.markdown(f"**Total experiments:** {len(selected_experiments)}")
        st.sidebar.markdown(f"**Total daily tests:** {sum(daily_counts.values())}")

        optimize_button = st.sidebar.button("3️⃣ Optimize Configuration", key="optimize_button")

        if optimize_button:
            if not customer_name or not unit_location or not operator_name:
                st.error("Please fill in Customer Name, Unit Location, and Operator Name before optimizing.")
            else:
                try:
                    with st.spinner("Optimizing tray configuration..."):
                        config = optimizer.optimize_tray_configuration(selected_experiments, daily_counts)
                    st.session_state.config = config
                    st.session_state.selected_experiments = selected_experiments
                    
                    # Show optimization summary
                    used_locations = len([loc for loc in config["tray_locations"] if loc is not None])
                    st.success(f"""
                    Configuration optimized successfully:
                    - All {used_locations} locations utilized
                    - Optimized for maximum days of operation
                    - Multiple sets added where beneficial
                    """)
                    
                except ValueError as e:
                    st.error(str(e))
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    if st.session_state.config is not None:
        display_results(st.session_state.config, st.session_state.selected_experiments, customer_info)

        # QC Questionnaire
        st.subheader("QC Questionnaire")
        qc1 = st.checkbox("1. Sealed + Zip Locked fluid tray is placed inside designated box with designated Styrofoam packaging material on all 6 sides of the tray?")
        qc2 = st.checkbox("2. Box is sealed with tape, 'Fragile' and 'This way up' stickers?")
        qc3 = st.checkbox("3. Box is carried to FedEx by KETOS for 2-day Air or Ground shipping only?")

        # Tracking Number Input
        tracking_number = st.text_input("Tracking Number")

        # Ship Button
        if st.button("Mark as Shipped"):
            if qc1 and qc2 and qc3 and tracking_number:
                # Prepare data for KCF summary
                kcf_data = [
                    customer_info['operator'],
                    datetime.now().strftime("%m/%d/%Y %H:%M"),
                    customer_info['name'],
                    customer_info['unit'],
                    len(selected_experiments),
                    tracking_number,
                    "Yes" if qc1 else "No",
                    "Yes" if qc2 else "No",
                    "Yes" if qc3 else "No"
                ]
                
                if not missing_modules:
                    # Update KCFtray2024.csv
                    if update_kcf_summary(kcf_data):
                        st.success("Tray marked as shipped and KCF summary updated successfully!")
                    else:
                        st.error("Failed to update KCF summary. Please try again or contact support.")
                else:
                    st.warning("KCF summary could not be updated due to missing modules.")
                    st.info("Tray information:")
                    st.json(kcf_data)
            else:
                st.error("Please complete all QC checks and provide a tracking number before shipping.")

    # Help and Information
    with st.sidebar.expander("ℹ️ Help & Information"):
        st.markdown("""
        ### How to use

        1. **Customer Information**
           - Enter customer name
           - Specify unit location
           - Set configuration date
           - Enter operator name

        2. **Select Experiments**
           - Choose from Low Range, High Range, or Other tabs
           - Or enter experiment numbers manually
           - View experiments by category

        3. **Daily Test Counts**
           - Enter the number of daily tests needed for each selected experiment
           - Numbers must be greater than 0

        4. **Optimization**
           - Click 'Optimize Configuration' to generate the optimal tray layout
           - System will maximize days of operation based on daily usage

        5. **Results**
           - View the tray visualization
           - Check detailed metrics and summaries
           - Download configuration plot and results

        6. **QC and Shipping**
           - Complete the QC questionnaire
           - Enter the tracking number
           - Mark the tray as shipped to update the KCF summary
        """)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #666;'>
    <small>Version 2.1 | Last Updated: 2024-03</small>
    </div>
    """, unsafe_allow_html=True)

    # Main page information (when no configuration is shown)
    if st.session_state.config is None:
        st.markdown("""
        <div class='header-box'>
        <h2>Welcome to the Reagent Tray Configurator! 👋</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='info-box'>
        <h3>🎯 Key Features</h3>
        
        - Optimized tray configuration based on daily usage
        - Smart allocation of high-capacity locations
        - Detailed analysis of operational duration
        - Downloadable reports and visualizations
        - Easy experiment selection by category
        - QC checklist and shipping integration
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='warning-box'>
        <h3>⚠️ Important Notes</h3>
        
        - High-volume reagents are automatically prioritized for 270mL locations
        - The system optimizes for maximum days of operation
        - Configuration considers both volume requirements and daily usage patterns
        - Total reagents must not exceed 16 locations
        - Complete all QC checks before marking a tray as shipped
        </div>
        """, unsafe_allow_html=True)

    # Add version tracking
    st.sidebar.markdown("""
    <div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: #f0f2f6; padding: 8px; text-align: center; font-size: 12px;'>
    Reagent Tray Configurator v2.1
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

