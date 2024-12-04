import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from reagent_optimizer import ReagentOptimizer
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Reagent Tray Configurator Pro",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
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

def get_reagent_color(reagent_code):
    color_map = {
        'gray': ['KR1E', 'KR1S', 'KR2S', 'KR3E', 'KR3S', 'KR4E', 'KR4S', 'KR5E', 'KR5S', 'KR6E1', 'KR6E2', 'KR6E3', 'KR13E1', 'KR13S', 'KR14E', 'KR14S', 'KR15E', 'KR15S'],
        'violet': ['KR7E1', 'KR7E2', 'KR8E1', 'KR8E2', 'KR19E1', 'KR19E2', 'KR19E3', 'KR20E', 'KR36E1', 'KR36E2', 'KR40E1', 'KR40E2'],
        'green': ['KR9E1', 'KR9E2', 'KR17E1', 'KR17E2', 'KR17E3', 'KR28E1', 'KR28E2', 'KR28E3'],
        'orange': ['KR10E1', 'KR10E2', 'KR10E3', 'KR12E1', 'KR12E2', 'KR12E3', 'KR18E1', 'KR18E2', 'KR22E1', 'KR27E1', 'KR27E2', 'KR42E1', 'KR42E2'],
        'white': ['KR11E', 'KR21E1'],
        'blue': ['KR16E1', 'KR16E2', 'KR16E3', 'KR16E4', 'KR30E1', 'KR30E2', 'KR30E3', 'KR31E1', 'KR31E2', 'KR34E1', 'KR34E2'],
        'red': ['KR29E1', 'KR29E2', 'KR29E3'],
        'yellow': ['KR35E1', 'KR35E2']
    }
    for color, reagents in color_map.items():
        if any(reagent_code.startswith(r) for r in reagents):
            return color
    return 'lightgray'

def create_tray_visualization(config, customer_info):
    locations = config["tray_locations"]
    fig = go.Figure()

    # Create the title with customer information
    title = (f"Reagent Tray Configuration<br>"
             f"Customer: {customer_info['name']} | Unit: {customer_info['unit']} | "
             f"Date: {customer_info['date'].strftime('%Y-%m-%d')}")

    for i, loc in enumerate(locations):
        row = i // 4
        col = i % 4
        color = get_reagent_color(loc['reagent_code']) if loc else 'lightgray'
        opacity = 0.8 if loc else 0.2

        fig.add_trace(go.Scatter(
            x=[col, col+1, col+1, col, col],
            y=[row, row, row+1, row+1, row],
            fill="toself",
            fillcolor=color,
            opacity=opacity,
            line=dict(color="black", width=1),
            mode="lines",
            name=f"LOC-{i+1}",
            text=f"LOC-{i+1}<br>{loc['reagent_code'] if loc else 'Empty'}<br>Tests: {loc['tests_possible'] if loc else 'N/A'}<br>Exp: #{loc['experiment'] if loc else 'N/A'}",
            hoverinfo="text"
        ))

        fig.add_annotation(
            x=(col + col + 1) / 2,
            y=(row + row + 1) / 2,
            text=f"<b>LOC-{i+1}</b><br>{'<b>' + loc['reagent_code'] if loc else 'Empty</b>'}<br>Tests: {loc['tests_possible'] if loc else 'N/A'}<br>Exp: #{loc['experiment'] if loc else 'N/A'}",
            showarrow=False,
            font=dict(color="black", size=14),
            align="center",
            xanchor="center",
            yanchor="middle"
        )

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            y=0.95,
            xanchor="center",
            yanchor="top",
            font=dict(size=16)
        ),
        showlegend=False,
        height=600,
        width=800,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=80, b=20)
    )

    return fig

def display_results(config, selected_experiments, customer_info):
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Tray Configuration")
        fig = create_tray_visualization(config, customer_info)
        st.plotly_chart(fig, use_container_width=True)
        
        if st.button("Download Configuration Plot"):
            fig.write_image("tray_configuration.png")
            st.success("Plot downloaded as 'tray_configuration.png'")

    with col2:
        st.subheader("Results Summary")
        
        # Key metrics in expander
        with st.expander("📊 Key Metrics", expanded=True):
            days_operation = config["overall_days_of_operation"]
            
            # Calculate total tests possible within days of operation
            total_tests = sum(
                min(result["total_tests"], 
                    result["daily_count"] * days_operation)
                for result in config["results"].values()
            )
            
            col1_metric, col2_metric = st.columns(2)
            with col1_metric:
                st.metric("Days of Operation", f"{days_operation:.1f} days")
            with col2_metric:
                st.metric("Total Tests Possible", f"{int(total_tests)}")

        # Results table with adjusted total tests
        results_df = pd.DataFrame([
            {
                "Experiment": f"{result['name']} (#{exp_num})",
                "Daily Tests": result['daily_count'],
                "Total Tests Possible": min(
                    result['total_tests'],
                    int(result['daily_count'] * days_operation)
                ),
                "Days of Operation": result['days_of_operation']
            }
            for exp_num, result in config["results"].items()
        ])
        st.dataframe(results_df, use_container_width=True)

        if st.button("Download Results as CSV"):
            results_df.to_csv("tray_configuration_results.csv", index=False)
            st.success("Results downloaded as 'tray_configuration_results.csv'")


    # Detailed Results in Expandable Sections
    st.subheader("Detailed Results")
    for exp_num, result in config["results"].items():
        with st.expander(f"📋 {result['name']} (#{exp_num}) - {result['total_tests']} total tests"):
            st.markdown(f"**Daily Usage:** {result['daily_count']} tests")
            st.markdown(f"**Days of Operation:** {result['days_of_operation']} days")
            
            for i, set_info in enumerate(result["sets"]):
                st.markdown(f"**{'Primary' if i == 0 else 'Additional'} Set {i+1}:**")
                set_df = pd.DataFrame([
                    {
                        "Reagent": placement["reagent_code"],
                        "Location": f"LOC-{placement['location'] + 1}",
                        "Tests Possible": placement["tests"],
                        "Volume per Test (µL)": placement["volume"]
                    }
                    for placement in set_info["placements"]
                ])
                st.dataframe(set_df, use_container_width=True)
                st.markdown(f"**Tests from this set:** {set_info['tests_per_set']}")
                st.markdown("---")

def reset_app():
    """Clears all session state variables to reset the app."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def main():
    st.title("🧪 Reagent Tray Configurator Pro")
    
    # Initialize session state
    if 'config' not in st.session_state:
        st.session_state.config = None
    if 'selected_experiments' not in st.session_state:
        st.session_state.selected_experiments = []
    if 'daily_counts' not in st.session_state:
        st.session_state.daily_counts = {}

    # Customer Information Section
    st.sidebar.markdown("### 📝 Customer Information")
    customer_name = st.sidebar.text_input("Customer Name", key="customer_name")
    unit_location = st.sidebar.text_input("Unit Location", key="unit_location")
    config_date = st.sidebar.date_input("Configuration Date", datetime.now())

    customer_info = {
        "name": customer_name,
        "unit": unit_location,
        "date": config_date
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
            if not customer_name or not unit_location:
                st.error("Please fill in Customer Name and Unit Location before optimizing.")
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

    # Help and Information
    with st.sidebar.expander("ℹ️ Help & Information"):
        st.markdown("""
        ### How to use

        1. **Customer Information**
           - Enter customer name
           - Specify unit location
           - Set configuration date

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
        """)

    # Add version tracking
    st.sidebar.markdown("""
    <div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: #f0f2f6; padding: 8px; text-align: center; font-size: 12px;'>
    Reagent Tray Configurator Pro v2.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
