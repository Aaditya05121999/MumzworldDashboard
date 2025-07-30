import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
from utils.data_processor import DataProcessor
from utils.insight_generator import InsightGenerator
from utils.chart_generator import ChartGenerator

# Configure page settings for mobile optimization
st.set_page_config(
    page_title="Mobile Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile optimization
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    @media (max-width: 768px) {
        .stColumns > div {
            min-width: unset !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📊 Mobile Data Analyst")
    st.markdown("*Discover insights and trends in your data on the go*")
    
    # Initialize session state
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'processor' not in st.session_state:
        st.session_state.processor = None
    if 'insights' not in st.session_state:
        st.session_state.insights = None

    # Main navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Upload", "📈 Overview", "🔍 Insights", "📊 Charts"])
    
    with tab1:
        upload_section()
    
    with tab2:
        if st.session_state.data is not None:
            overview_section()
        else:
            st.info("👆 Please upload data first to see overview")
    
    with tab3:
        if st.session_state.data is not None:
            insights_section()
        else:
            st.info("👆 Please upload data first to generate insights")
    
    with tab4:
        if st.session_state.data is not None:
            charts_section()
        else:
            st.info("👆 Please upload data first to create charts")

def upload_section():
    st.header("📁 Upload Your Data")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Supported formats: CSV, Excel (.xlsx, .xls)"
    )
    
    if uploaded_file is not None:
        try:
            # Load data based on file type
            if uploaded_file.name.endswith('.csv'):
                data = pd.read_csv(uploaded_file)
            else:
                data = pd.read_excel(uploaded_file)
            
            st.session_state.data = data
            st.session_state.processor = DataProcessor(data)
            st.session_state.insights = None  # Reset insights when new data is loaded
            
            st.success(f"✅ Data loaded successfully! ({len(data)} rows, {len(data.columns)} columns)")
            
            # Quick preview
            with st.expander("📋 Data Preview", expanded=False):
                st.dataframe(data.head(10), use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    # Sample data option
    st.markdown("---")
    st.subheader("🎯 Or try with sample data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📈 Sales Data", use_container_width=True):
            data = generate_sample_sales_data()
            st.session_state.data = data
            st.session_state.processor = DataProcessor(data)
            st.session_state.insights = None
            st.success("✅ Sample sales data loaded!")
    
    with col2:
        if st.button("👥 Customer Data", use_container_width=True):
            data = generate_sample_customer_data()
            st.session_state.data = data
            st.session_state.processor = DataProcessor(data)
            st.session_state.insights = None
            st.success("✅ Sample customer data loaded!")

def overview_section():
    st.header("📈 Data Overview")
    
    data = st.session_state.data
    processor = st.session_state.processor
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rows", f"{len(data):,}")
    with col2:
        st.metric("Columns", len(data.columns))
    with col3:
        st.metric("Missing Values", f"{data.isnull().sum().sum():,}")
    with col4:
        memory_usage = data.memory_usage(deep=True).sum() / 1024**2
        st.metric("Size (MB)", f"{memory_usage:.2f}")
    
    # Data types summary
    with st.expander("📊 Column Information", expanded=False):
        col_info = processor.get_column_info()
        st.dataframe(col_info, use_container_width=True)
    
    # Missing values heatmap
    if data.isnull().sum().sum() > 0:
        with st.expander("🔍 Missing Values Pattern", expanded=False):
            missing_chart = processor.create_missing_values_chart()
            st.plotly_chart(missing_chart, use_container_width=True)
    
    # Statistical summary
    with st.expander("📋 Statistical Summary", expanded=False):
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            st.dataframe(data[numeric_cols].describe(), use_container_width=True)
        else:
            st.info("No numeric columns found for statistical summary")

def insights_section():
    st.header("🔍 Automated Insights")
    
    data = st.session_state.data
    
    # Generate insights button
    if st.button("🚀 Generate Insights", use_container_width=True):
        with st.spinner("Analyzing your data..."):
            insight_gen = InsightGenerator(data)
            insights = insight_gen.generate_all_insights()
            st.session_state.insights = insights
    
    # Display insights if available
    if st.session_state.insights:
        insights = st.session_state.insights
        
        # Key findings
        if 'key_findings' in insights:
            st.subheader("🎯 Key Findings")
            for finding in insights['key_findings']:
                st.markdown(f"• {finding}")
        
        # Correlations
        if 'correlations' in insights and len(insights['correlations']) > 0:
            with st.expander("🔗 Strong Correlations", expanded=False):
                for corr in insights['correlations']:
                    st.markdown(f"• **{corr['var1']}** & **{corr['var2']}**: {corr['correlation']:.3f}")
        
        # Outliers
        if 'outliers' in insights and len(insights['outliers']) > 0:
            with st.expander("⚠️ Potential Outliers", expanded=False):
                for outlier in insights['outliers']:
                    st.markdown(f"• **{outlier['column']}**: {outlier['count']} outliers detected")
        
        # Trends
        if 'trends' in insights and len(insights['trends']) > 0:
            with st.expander("📈 Trend Analysis", expanded=False):
                for trend in insights['trends']:
                    st.markdown(f"• **{trend['column']}**: {trend['description']}")
        
        # Data quality
        if 'data_quality' in insights:
            with st.expander("✅ Data Quality Assessment", expanded=False):
                quality = insights['data_quality']
                st.markdown(f"• **Completeness**: {quality['completeness']:.1f}%")
                st.markdown(f"• **Duplicate Rows**: {quality['duplicates']}")
                if quality['recommendations']:
                    st.markdown("**Recommendations:**")
                    for rec in quality['recommendations']:
                        st.markdown(f"  - {rec}")
    
    else:
        st.info("Click 'Generate Insights' to analyze your data automatically")

def charts_section():
    st.header("📊 Interactive Charts")
    
    data = st.session_state.data
    chart_gen = ChartGenerator(data)
    
    # Chart type selection
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Distribution", "Correlation", "Time Series", "Comparison", "Custom"]
    )
    
    if chart_type == "Distribution":
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Select Column", numeric_cols)
            chart = chart_gen.create_distribution_chart(selected_col)
            st.plotly_chart(chart, use_container_width=True)
            
            # Export button
            export_chart(chart, f"distribution_{selected_col}")
    
    elif chart_type == "Correlation":
        chart = chart_gen.create_correlation_matrix()
        if chart:
            st.plotly_chart(chart, use_container_width=True)
            export_chart(chart, "correlation_matrix")
        else:
            st.warning("Not enough numeric columns for correlation analysis")
    
    elif chart_type == "Time Series":
        date_cols = data.select_dtypes(include=['datetime64', 'object']).columns.tolist()
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if date_cols and numeric_cols:
            col1, col2 = st.columns(2)
            with col1:
                date_col = st.selectbox("Select Date Column", date_cols)
            with col2:
                value_col = st.selectbox("Select Value Column", numeric_cols)
            
            chart = chart_gen.create_time_series_chart(date_col, value_col)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
                export_chart(chart, f"timeseries_{value_col}")
        else:
            st.warning("Need both date and numeric columns for time series")
    
    elif chart_type == "Comparison":
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if categorical_cols and numeric_cols:
            col1, col2 = st.columns(2)
            with col1:
                cat_col = st.selectbox("Select Category Column", categorical_cols)
            with col2:
                num_col = st.selectbox("Select Numeric Column", numeric_cols)
            
            chart = chart_gen.create_comparison_chart(cat_col, num_col)
            st.plotly_chart(chart, use_container_width=True)
            export_chart(chart, f"comparison_{cat_col}_{num_col}")
        else:
            st.warning("Need both categorical and numeric columns for comparison")
    
    elif chart_type == "Custom":
        st.subheader("🎨 Custom Chart Builder")
        
        col1, col2 = st.columns(2)
        with col1:
            x_axis = st.selectbox("X-axis", data.columns.tolist())
        with col2:
            y_axis = st.selectbox("Y-axis", data.columns.tolist())
        
        chart_style = st.selectbox("Chart Style", ["Scatter", "Line", "Bar"])
        
        if st.button("Create Chart", use_container_width=True):
            chart = chart_gen.create_custom_chart(x_axis, y_axis, chart_style.lower())
            st.plotly_chart(chart, use_container_width=True)
            export_chart(chart, f"custom_{x_axis}_{y_axis}")

def export_chart(chart, filename):
    """Export chart functionality"""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download HTML", key=f"html_{filename}"):
            html_string = chart.to_html()
            st.download_button(
                label="Download HTML File",
                data=html_string,
                file_name=f"{filename}.html",
                mime="text/html"
            )
    
    with col2:
        if st.button("📷 Download PNG", key=f"png_{filename}"):
            img_bytes = chart.to_image(format="png", width=800, height=600)
            st.download_button(
                label="Download PNG File",
                data=img_bytes,
                file_name=f"{filename}.png",
                mime="image/png"
            )

def generate_sample_sales_data():
    """Generate sample sales data for demonstration"""
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
    n_days = len(dates)
    
    data = {
        'Date': dates,
        'Sales': np.random.normal(1000, 200, n_days) + np.sin(np.arange(n_days) * 2 * np.pi / 365) * 100,
        'Customers': np.random.poisson(50, n_days),
        'Product_A': np.random.normal(300, 50, n_days),
        'Product_B': np.random.normal(400, 80, n_days),
        'Product_C': np.random.normal(300, 60, n_days),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], n_days),
        'Channel': np.random.choice(['Online', 'Store', 'Phone'], n_days, p=[0.5, 0.3, 0.2])
    }
    
    df = pd.DataFrame(data)
    df['Sales'] = np.maximum(df['Sales'], 100)  # Ensure positive sales
    return df

def generate_sample_customer_data():
    """Generate sample customer data for demonstration"""
    np.random.seed(42)
    n_customers = 1000
    
    data = {
        'Customer_ID': range(1, n_customers + 1),
        'Age': np.random.normal(40, 15, n_customers).astype(int),
        'Income': np.random.normal(50000, 20000, n_customers),
        'Spending_Score': np.random.randint(1, 101, n_customers),
        'Purchase_Frequency': np.random.poisson(5, n_customers),
        'Last_Purchase_Days': np.random.randint(1, 365, n_customers),
        'Gender': np.random.choice(['Male', 'Female'], n_customers),
        'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_customers),
        'Membership': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], n_customers, p=[0.4, 0.3, 0.2, 0.1])
    }
    
    df = pd.DataFrame(data)
    df['Age'] = np.clip(df['Age'], 18, 80)  # Reasonable age range
    df['Income'] = np.maximum(df['Income'], 20000)  # Minimum income
    return df

if __name__ == "__main__":
    main()
