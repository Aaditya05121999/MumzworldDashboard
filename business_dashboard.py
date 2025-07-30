import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configure page settings
st.set_page_config(
    page_title="Mumzworld Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Notion-style CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    
    /* Notion-style card design */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .insight-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #4f46e5;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .question-header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        padding: 1rem 1.5rem;
        border-radius: 8px 8px 0 0;
        color: white;
        font-weight: bold;
        margin: 2rem 0 0 0;
    }
    
    .answer-content {
        background: white;
        padding: 1.5rem;
        border-radius: 0 0 8px 8px;
        border: 1px solid #e5e7eb;
        margin: 0 0 2rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .kpi-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 1px solid #e5e7eb;
    }
    
    .sidebar-content {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    /* Mobile optimization */
    @media (max-width: 768px) {
        .stColumns > div {
            min-width: unset !important;
        }
        .metric-card, .insight-card {
            margin: 0.25rem 0;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the dataset"""
    df = pd.read_excel('attached_assets/Planning_Performance_Dataset_1753898833288.xlsx')
    
    # Convert Month to datetime for better analysis
    df['Month_Date'] = pd.to_datetime(df['Month'], format='%b-%Y')
    df['Year'] = df['Month_Date'].dt.year
    df['Month_Num'] = df['Month_Date'].dt.month
    
    # Calculate derived metrics
    df['Marketing_Cost_Per_Order'] = df['Marketing Cost'] / df['Orders']
    df['Revenue_Per_Order'] = df['Revenue'] / df['Orders']
    df['Voucher_Cost_Per_Order'] = df['Voucher Cost'] / df['Orders']
    df['Total_Customers'] = df['New Customers'] + df['Repeat Customers']
    df['Gross_Profit'] = df['Revenue'] * df['Gross Margin %']
    
    return df

def create_notion_card(title, value, subtitle="", color="#4f46e5"):
    """Create a Notion-style metric card"""
    return f"""
    <div style="
        background: linear-gradient(135deg, {color}, {color}dd);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
    ">
        <h3 style="margin: 0; font-size: 1.1rem; opacity: 0.9;">{title}</h3>
        <h1 style="margin: 0.5rem 0; font-size: 2rem; font-weight: bold;">{value}</h1>
        <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{subtitle}</p>
    </div>
    """

def main():
    # Load data
    df = load_data()
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 2.5rem; font-weight: bold; margin: 0;">📊 Mumzworld Business Analytics</h1>
        <p style="font-size: 1.2rem; color: #666; margin: 0.5rem 0;">Graduate Management Trainee Programme Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview KPIs
    st.markdown("## 🎯 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = df['Revenue'].sum()
        st.markdown(create_notion_card("Total Revenue", f"${total_revenue:,.0f}", "Across all markets"), unsafe_allow_html=True)
    
    with col2:
        total_orders = df['Orders'].sum()
        st.markdown(create_notion_card("Total Orders", f"{total_orders:,.0f}", "UAE + KSA combined", "#059669"), unsafe_allow_html=True)
    
    with col3:
        avg_margin = df['Gross Margin %'].mean()
        st.markdown(create_notion_card("Avg Gross Margin", f"{avg_margin:.1%}", "Weighted average", "#dc2626"), unsafe_allow_html=True)
    
    with col4:
        avg_repurchase = df['Repurchase Rate'].mean()
        st.markdown(create_notion_card("Avg Repurchase Rate", f"{avg_repurchase:.1%}", "Customer retention", "#7c3aed"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Question 1: Highest gross margin country-category combination
    st.markdown('<div class="question-header">Q1: Which country-category combination shows the highest gross margin in 2024?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        # Filter for 2024 data
        df_2024 = df[df['Year'] == 2024]
        margin_by_combo = df_2024.groupby(['Country', 'Category'])['Gross Margin %'].mean().reset_index()
        margin_by_combo = margin_by_combo.sort_values('Gross Margin %', ascending=False)
        
        top_combo = margin_by_combo.iloc[0]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div class="insight-card">
                <h3>🏆 Top Performer</h3>
                <h2>{top_combo['Country']} - {top_combo['Category']}</h2>
                <h1 style="color: #059669;">{top_combo['Gross Margin %']:.1%}</h1>
                <p>Highest gross margin combination in 2024</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            fig = px.bar(
                margin_by_combo.head(10),
                x='Gross Margin %',
                y=[f"{row['Country']} - {row['Category']}" for _, row in margin_by_combo.head(10).iterrows()],
                orientation='h',
                title="Top 10 Country-Category Combinations by Gross Margin",
                color='Gross Margin %',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 2: Voucher overspending analysis
    st.markdown('<div class="question-header">Q2: Are we overspending on vouchers in any specific category or market?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        # Calculate voucher cost per order and as % of revenue
        voucher_analysis = df.groupby(['Country', 'Category']).agg({
            'Voucher Cost': 'sum',
            'Revenue': 'sum',
            'Orders': 'sum'
        }).reset_index()
        
        voucher_analysis['Voucher_Per_Order'] = voucher_analysis['Voucher Cost'] / voucher_analysis['Orders']
        voucher_analysis['Voucher_Revenue_Ratio'] = voucher_analysis['Voucher Cost'] / voucher_analysis['Revenue']
        voucher_analysis = voucher_analysis.sort_values('Voucher_Revenue_Ratio', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top voucher spenders by ratio
            fig1 = px.bar(
                voucher_analysis.head(8),
                x='Voucher_Revenue_Ratio',
                y=[f"{row['Country']} - {row['Category']}" for _, row in voucher_analysis.head(8).iterrows()],
                orientation='h',
                title="Voucher Cost as % of Revenue",
                labels={'Voucher_Revenue_Ratio': 'Voucher/Revenue Ratio'},
                color='Voucher_Revenue_Ratio',
                color_continuous_scale='Reds'
            )
            fig1.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Voucher cost per order
            fig2 = px.bar(
                voucher_analysis.head(8),
                x='Voucher_Per_Order',
                y=[f"{row['Country']} - {row['Category']}" for _, row in voucher_analysis.head(8).iterrows()],
                orientation='h',
                title="Voucher Cost per Order",
                labels={'Voucher_Per_Order': 'Voucher Cost per Order ($)'},
                color='Voucher_Per_Order',
                color_continuous_scale='Blues'
            )
            fig2.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig2, use_container_width=True)
        
        # Key insights
        high_voucher = voucher_analysis.iloc[0]
        st.markdown(f"""
        <div class="insight-card">
            <h3>⚠️ Potential Overspending Alert</h3>
            <p><strong>{high_voucher['Country']} - {high_voucher['Category']}</strong> has the highest voucher-to-revenue ratio at <strong>{high_voucher['Voucher_Revenue_Ratio']:.1%}</strong></p>
            <p>This translates to <strong>${high_voucher['Voucher_Per_Order']:.2f}</strong> in vouchers per order</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 3: SLA compliance vs repurchase rate
    st.markdown('<div class="question-header">Q3: What is the relationship between SLA compliance and repurchase rate?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Scatter plot showing relationship
            fig = px.scatter(
                df,
                x='SLA Compliance %',
                y='Repurchase Rate',
                color='Country',
                size='Orders',
                hover_data=['Category', 'Month'],
                title="SLA Compliance vs Repurchase Rate",
                trendline="ols"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Calculate correlation
            correlation = np.corrcoef(df['SLA Compliance %'], df['Repurchase Rate'])[0, 1]
            
            st.markdown(f"""
            <div class="insight-card">
                <h3>📈 Correlation Analysis</h3>
                <h2 style="color: {'#059669' if correlation > 0.5 else '#dc2626' if correlation < -0.5 else '#f59e0b'};">
                    {correlation:.3f}
                </h2>
                <p>Correlation coefficient between SLA compliance and repurchase rate</p>
                <hr>
                <p><strong>Interpretation:</strong></p>
                <p>{'Strong positive' if correlation > 0.5 else 'Moderate positive' if correlation > 0.3 else 'Weak' if correlation > -0.3 else 'Negative'} relationship</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 4: Marketing cost per order by category
    st.markdown('<div class="question-header">Q4: Which categories have the highest marketing cost per order?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        marketing_efficiency = df.groupby(['Category']).agg({
            'Marketing Cost': 'sum',
            'Orders': 'sum',
            'Revenue': 'sum'
        }).reset_index()
        
        marketing_efficiency['Marketing_Per_Order'] = marketing_efficiency['Marketing Cost'] / marketing_efficiency['Orders']
        marketing_efficiency['Marketing_Revenue_Ratio'] = marketing_efficiency['Marketing Cost'] / marketing_efficiency['Revenue']
        marketing_efficiency = marketing_efficiency.sort_values('Marketing_Per_Order', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                marketing_efficiency,
                x='Category',
                y='Marketing_Per_Order',
                title="Marketing Cost per Order by Category",
                color='Marketing_Per_Order',
                color_continuous_scale='Oranges'
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Show efficiency metrics
            st.markdown("### 💰 Marketing Efficiency Rankings")
            for i, row in marketing_efficiency.iterrows():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.5rem; margin: 0.25rem 0; border-radius: 6px; border-left: 3px solid #4f46e5;">
                    <strong>{row['Category']}</strong><br>
                    ${row['Marketing_Per_Order']:.2f} per order ({row['Marketing_Revenue_Ratio']:.1%} of revenue)
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 5: Delivery times and success rate
    st.markdown('<div class="question-header">Q5: Where are delivery times highest and how does it impact success rate?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        delivery_analysis = df.groupby(['Country', 'Category']).agg({
            'Avg Delivery Time (days)': 'mean',
            'Success Rate': 'mean',
            'Orders': 'sum'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Heatmap of delivery times
            delivery_pivot = delivery_analysis.pivot(index='Category', columns='Country', values='Avg Delivery Time (days)')
            fig = px.imshow(
                delivery_pivot,
                title="Average Delivery Time by Country-Category",
                color_continuous_scale='Reds',
                aspect="auto"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Delivery time vs success rate
            fig2 = px.scatter(
                delivery_analysis,
                x='Avg Delivery Time (days)',
                y='Success Rate',
                size='Orders',
                color='Country',
                hover_data=['Category'],
                title="Delivery Time vs Success Rate",
                trendline="ols"
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Insights
        slowest_delivery = delivery_analysis.loc[delivery_analysis['Avg Delivery Time (days)'].idxmax()]
        delivery_success_corr = np.corrcoef(df['Avg Delivery Time (days)'], df['Success Rate'])[0, 1]
        
        st.markdown(f"""
        <div class="insight-card">
            <h3>🚚 Delivery Performance Insights</h3>
            <p><strong>Slowest delivery:</strong> {slowest_delivery['Country']} - {slowest_delivery['Category']} 
            ({slowest_delivery['Avg Delivery Time (days)']:.1f} days)</p>
            <p><strong>Correlation with success rate:</strong> {delivery_success_corr:.3f} 
            ({'Negative impact' if delivery_success_corr < -0.3 else 'Minimal impact' if abs(delivery_success_corr) < 0.3 else 'Positive impact'})</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 6: Effect of 15% shipping cost reduction in KSA
    st.markdown('<div class="question-header">Q6: What would be the effect of a 15% reduction in shipping cost in KSA?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        ksa_data = df[df['Country'] == 'KSA']
        current_shipping = ksa_data['Shipping Cost'].sum()
        reduced_shipping = current_shipping * 0.85
        savings = current_shipping - reduced_shipping
        
        # Calculate impact on gross profit
        current_gross_profit = ksa_data['Gross_Profit'].sum()
        new_gross_profit = current_gross_profit + savings
        profit_increase = (new_gross_profit - current_gross_profit) / current_gross_profit
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(create_notion_card("Current Shipping Cost", f"${current_shipping:,.0f}", "KSA total", "#dc2626"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_notion_card("Potential Savings", f"${savings:,.0f}", "15% reduction", "#059669"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_notion_card("Gross Profit Impact", f"+{profit_increase:.1%}", "Improvement", "#7c3aed"), unsafe_allow_html=True)
        
        # Show impact by category
        ksa_category_impact = ksa_data.groupby('Category').agg({
            'Shipping Cost': 'sum',
            'Revenue': 'sum',
            'Gross_Profit': 'sum'
        }).reset_index()
        
        ksa_category_impact['Shipping_Savings'] = ksa_category_impact['Shipping Cost'] * 0.15
        ksa_category_impact['New_Gross_Profit'] = ksa_category_impact['Gross_Profit'] + ksa_category_impact['Shipping_Savings']
        ksa_category_impact['Profit_Improvement'] = (ksa_category_impact['New_Gross_Profit'] - ksa_category_impact['Gross_Profit']) / ksa_category_impact['Gross_Profit']
        
        fig = px.bar(
            ksa_category_impact,
            x='Category',
            y=['Gross_Profit', 'Shipping_Savings'],
            title="KSA: Current Gross Profit vs Potential Shipping Savings by Category",
            barmode='group'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 7: Strong repurchase behavior at low cost
    st.markdown('<div class="question-header">Q7: Which category shows strong repurchase behavior at low cost?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        # Calculate efficiency metric: repurchase rate vs marketing cost per order
        repurchase_efficiency = df.groupby('Category').agg({
            'Repurchase Rate': 'mean',
            'Marketing_Cost_Per_Order': 'mean',
            'Revenue': 'sum',
            'Orders': 'sum'
        }).reset_index()
        
        # Create efficiency score (high repurchase, low marketing cost)
        repurchase_efficiency['Efficiency_Score'] = repurchase_efficiency['Repurchase Rate'] / repurchase_efficiency['Marketing_Cost_Per_Order']
        repurchase_efficiency = repurchase_efficiency.sort_values('Efficiency_Score', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.scatter(
                repurchase_efficiency,
                x='Marketing_Cost_Per_Order',
                y='Repurchase Rate',
                size='Revenue',
                color='Category',
                title="Repurchase Rate vs Marketing Cost per Order",
                labels={'Marketing_Cost_Per_Order': 'Marketing Cost per Order ($)'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Efficiency Champions")
            for i, row in repurchase_efficiency.head(3).iterrows():
                st.markdown(f"""
                <div class="insight-card">
                    <h4>{row['Category']}</h4>
                    <p><strong>Repurchase Rate:</strong> {row['Repurchase Rate']:.1%}</p>
                    <p><strong>Marketing Cost/Order:</strong> ${row['Marketing_Cost_Per_Order']:.2f}</p>
                    <p><strong>Efficiency Score:</strong> {row['Efficiency_Score']:.3f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 8: Churn rate by country and drivers
    st.markdown('<div class="question-header">Q8: What\'s the churn rate by country and what are the drivers?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        churn_analysis = df.groupby('Country').agg({
            'Customer Churn Rate': 'mean',
            'SLA Compliance %': 'mean',
            'Avg Delivery Time (days)': 'mean',
            'Success Rate': 'mean',
            'Repurchase Rate': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                churn_analysis,
                x='Country',
                y='Customer Churn Rate',
                title="Average Churn Rate by Country",
                color='Customer Churn Rate',
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Correlation analysis for churn drivers
            churn_correlations = pd.Series({
                'SLA Compliance %': np.corrcoef(df['Customer Churn Rate'], df['SLA Compliance %'])[0, 1],
                'Avg Delivery Time (days)': np.corrcoef(df['Customer Churn Rate'], df['Avg Delivery Time (days)'])[0, 1],
                'Success Rate': np.corrcoef(df['Customer Churn Rate'], df['Success Rate'])[0, 1],
                'Voucher_Cost_Per_Order': np.corrcoef(df['Customer Churn Rate'], df['Voucher_Cost_Per_Order'])[0, 1]
            })
            
            fig2 = px.bar(
                x=churn_correlations.values,
                y=churn_correlations.index,
                orientation='h',
                title="Churn Rate Correlation with Key Metrics",
                color=churn_correlations.values,
                color_continuous_scale='RdBu_r'
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Key insights
        highest_churn_country = churn_analysis.loc[churn_analysis['Customer Churn Rate'].idxmax(), 'Country']
        highest_churn_rate = churn_analysis['Customer Churn Rate'].max()
        
        st.markdown(f"""
        <div class="insight-card">
            <h3>📉 Churn Analysis Summary</h3>
            <p><strong>Highest churn rate:</strong> {highest_churn_country} ({highest_churn_rate:.1%})</p>
            <p><strong>Key drivers:</strong> Based on correlations, focus on improving delivery performance and SLA compliance</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 9: New vs repeat customers impact on revenue
    st.markdown('<div class="question-header">Q9: How do new vs repeat customers affect category-level revenue?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        customer_revenue_analysis = df.groupby(['Category']).agg({
            'New Customers': 'sum',
            'Repeat Customers': 'sum',
            'Revenue': 'sum',
            'Orders': 'sum'
        }).reset_index()
        
        customer_revenue_analysis['Total_Customers'] = customer_revenue_analysis['New Customers'] + customer_revenue_analysis['Repeat Customers']
        customer_revenue_analysis['New_Customer_Ratio'] = customer_revenue_analysis['New Customers'] / customer_revenue_analysis['Total_Customers']
        customer_revenue_analysis['Revenue_Per_Customer'] = customer_revenue_analysis['Revenue'] / customer_revenue_analysis['Total_Customers']
        customer_revenue_analysis = customer_revenue_analysis.sort_values('Revenue', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Stacked bar chart of customer composition
            fig = px.bar(
                customer_revenue_analysis,
                x='Category',
                y=['New Customers', 'Repeat Customers'],
                title="Customer Composition by Category",
                color_discrete_map={'New Customers': '#3b82f6', 'Repeat Customers': '#10b981'}
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Revenue per customer analysis
            fig2 = px.scatter(
                customer_revenue_analysis,
                x='New_Customer_Ratio',
                y='Revenue_Per_Customer',
                size='Revenue',
                color='Category',
                title="New Customer Ratio vs Revenue per Customer",
                labels={'New_Customer_Ratio': 'New Customer Ratio', 'Revenue_Per_Customer': 'Revenue per Customer ($)'}
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 10: Margin improvement priorities for 2025
    st.markdown('<div class="question-header">Q10: Where should we prioritize margin improvement actions in 2025?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        # Calculate improvement potential
        margin_improvement = df.groupby(['Country', 'Category']).agg({
            'Revenue': 'sum',
            'Gross Margin %': 'mean',
            'Marketing Cost': 'sum',
            'Voucher Cost': 'sum',
            'Shipping Cost': 'sum'
        }).reset_index()
        
        margin_improvement['Total_Costs'] = margin_improvement['Marketing Cost'] + margin_improvement['Voucher Cost'] + margin_improvement['Shipping Cost']
        margin_improvement['Cost_Revenue_Ratio'] = margin_improvement['Total_Costs'] / margin_improvement['Revenue']
        margin_improvement['Improvement_Potential'] = margin_improvement['Revenue'] * (1 - margin_improvement['Gross Margin %']) * margin_improvement['Cost_Revenue_Ratio']
        margin_improvement = margin_improvement.sort_values('Improvement_Potential', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.scatter(
                margin_improvement.head(10),
                x='Gross Margin %',
                y='Revenue',
                size='Improvement_Potential',
                color='Cost_Revenue_Ratio',
                hover_data=['Country', 'Category'],
                title="Margin Improvement Opportunities (Size = Potential Impact)",
                color_continuous_scale='Reds'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Top 5 Priorities")
            for i, row in margin_improvement.head(5).iterrows():
                priority_score = row['Improvement_Potential'] / margin_improvement['Improvement_Potential'].max() * 100
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #dc2626;">
                    <h4>{row['Country']} - {row['Category']}</h4>
                    <p><strong>Priority Score:</strong> {priority_score:.0f}/100</p>
                    <p><strong>Current Margin:</strong> {row['Gross Margin %']:.1%}</p>
                    <p><strong>Revenue:</strong> ${row['Revenue']:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Question 11: Weighted average gross margin for UAE
    st.markdown('<div class="question-header">Q11: What is the current weighted average gross margin for UAE?</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        uae_data = df[df['Country'] == 'UAE']
        
        # Calculate weighted average margin by revenue
        total_uae_revenue = uae_data['Revenue'].sum()
        weighted_margin = (uae_data['Revenue'] * uae_data['Gross Margin %']).sum() / total_uae_revenue
        
        # By category breakdown
        uae_category_margin = uae_data.groupby('Category').agg({
            'Revenue': 'sum',
            'Gross Margin %': 'mean'
        }).reset_index()
        uae_category_margin['Revenue_Weight'] = uae_category_margin['Revenue'] / total_uae_revenue
        uae_category_margin['Weighted_Contribution'] = uae_category_margin['Revenue_Weight'] * uae_category_margin['Gross Margin %']
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(create_notion_card("UAE Weighted Avg Margin", f"{weighted_margin:.1%}", "Revenue-weighted", "#4f46e5"), unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="insight-card">
                <h3>📊 Calculation Details</h3>
                <p><strong>Total UAE Revenue:</strong> ${total_uae_revenue:,.0f}</p>
                <p><strong>Weighting Method:</strong> Revenue-based</p>
                <p><strong>Result:</strong> {weighted_margin:.3%}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Show contribution by category
            fig = px.pie(
                uae_category_margin,
                values='Revenue',
                names='Category',
                title="UAE Revenue Distribution by Category",
                hover_data=['Gross Margin %']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed breakdown table
        st.markdown("### Category Contribution Analysis")
        uae_category_margin_display = uae_category_margin.copy()
        uae_category_margin_display['Revenue'] = uae_category_margin_display['Revenue'].apply(lambda x: f"${x:,.0f}")
        uae_category_margin_display['Gross Margin %'] = uae_category_margin_display['Gross Margin %'].apply(lambda x: f"{x:.1%}")
        uae_category_margin_display['Revenue_Weight'] = uae_category_margin_display['Revenue_Weight'].apply(lambda x: f"{x:.1%}")
        uae_category_margin_display['Weighted_Contribution'] = uae_category_margin_display['Weighted_Contribution'].apply(lambda x: f"{x:.3%}")
        
        st.dataframe(uae_category_margin_display, use_container_width=True, hide_index=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Questions 12 & 13: Repurchase optimization and margin improvement
    st.markdown('<div class="question-header">Q12-13: Repurchase Rate Optimization & Margin Impact Analysis</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="answer-content">', unsafe_allow_html=True)
        
        # Analyze categories by repurchase rate and margin
        repurchase_margin_analysis = df.groupby('Category').agg({
            'Repurchase Rate': 'mean',
            'Gross Margin %': 'mean',
            'Revenue': 'sum',
            'Orders': 'sum'
        }).reset_index()
        
        repurchase_margin_analysis['Revenue_Share'] = repurchase_margin_analysis['Revenue'] / repurchase_margin_analysis['Revenue'].sum()
        
        st.markdown("### Q12: Categories to Grow for Maximum Repurchase Rate")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Repurchase rate by category
            fig = px.bar(
                repurchase_margin_analysis.sort_values('Repurchase Rate', ascending=True),
                x='Repurchase Rate',
                y='Category',
                orientation='h',
                title="Repurchase Rate by Category",
                color='Repurchase Rate',
                color_continuous_scale='Greens'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Portfolio optimization matrix
            fig2 = px.scatter(
                repurchase_margin_analysis,
                x='Repurchase Rate',
                y='Gross Margin %',
                size='Revenue',
                color='Category',
                title="Repurchase Rate vs Margin (Size = Revenue)",
                labels={'Repurchase Rate': 'Repurchase Rate', 'Gross Margin %': 'Gross Margin %'}
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Recommendations for category mix optimization
        top_repurchase_categories = repurchase_margin_analysis.nlargest(3, 'Repurchase Rate')
        
        st.markdown("### 🎯 Recommended Growth Strategy")
        st.markdown(f"""
        <div class="insight-card">
            <h4>High-Repurchase Categories to Prioritize:</h4>
            <ul>
        """, unsafe_allow_html=True)
        
        for _, cat in top_repurchase_categories.iterrows():
            st.markdown(f"<li><strong>{cat['Category']}</strong>: {cat['Repurchase Rate']:.1%} repurchase rate, {cat['Gross Margin %']:.1%} margin</li>", unsafe_allow_html=True)
        
        st.markdown("</ul></div>", unsafe_allow_html=True)
        
        # Q13: New weighted margin calculation
        st.markdown("### Q13: Optimized Category Mix Impact")
        
        # Simulate increasing share of high-repurchase categories
        optimized_mix = repurchase_margin_analysis.copy()
        
        # Increase share of top 3 repurchase categories by 20% each, decrease others proportionally
        high_repurchase_mask = optimized_mix['Category'].isin(top_repurchase_categories['Category'])
        
        # Current weighted margin
        current_weighted_margin = (optimized_mix['Revenue_Share'] * optimized_mix['Gross Margin %']).sum()
        
        # Simulate optimized mix
        optimized_mix.loc[high_repurchase_mask, 'Revenue_Share'] *= 1.2
        optimized_mix.loc[~high_repurchase_mask, 'Revenue_Share'] *= 0.85
        
        # Normalize to ensure shares sum to 1
        optimized_mix['Revenue_Share'] = optimized_mix['Revenue_Share'] / optimized_mix['Revenue_Share'].sum()
        
        # New weighted margin
        new_weighted_margin = (optimized_mix['Revenue_Share'] * optimized_mix['Gross Margin %']).sum()
        margin_improvement = new_weighted_margin - current_weighted_margin
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(create_notion_card("Current Weighted Margin", f"{current_weighted_margin:.1%}", "Portfolio average", "#dc2626"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_notion_card("Optimized Weighted Margin", f"{new_weighted_margin:.1%}", f"Improvement: +{margin_improvement:.1%}", "#059669"), unsafe_allow_html=True)
        
        # Show the optimization strategy
        comparison_df = pd.DataFrame({
            'Category': optimized_mix['Category'],
            'Current Share': repurchase_margin_analysis['Revenue_Share'],
            'Optimized Share': optimized_mix['Revenue_Share'],
            'Gross Margin %': optimized_mix['Gross Margin %'],
            'Repurchase Rate': optimized_mix['Repurchase Rate']
        })
        comparison_df['Share Change'] = comparison_df['Optimized Share'] - comparison_df['Current Share']
        
        fig = px.bar(
            comparison_df,
            x='Category',
            y=['Current Share', 'Optimized Share'],
            title="Current vs Optimized Category Mix",
            barmode='group'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Strategy recommendations
        target_margin = current_weighted_margin + 0.05  # 5 percentage points higher
        
        st.markdown(f"""
        <div class="insight-card">
            <h3>💡 Strategic Recommendations</h3>
            <p><strong>To achieve {target_margin:.1%} target margin (+5pp):</strong></p>
            <ol>
                <li><strong>Category Mix:</strong> Increase share of high-repurchase categories ({', '.join(top_repurchase_categories['Category'].tolist())})</li>
                <li><strong>AOV Strategy:</strong> Focus on upselling in high-margin categories</li>
                <li><strong>Cost Optimization:</strong> Reduce marketing spend in low-efficiency categories</li>
                <li><strong>Customer Retention:</strong> Leverage strong repurchase behavior for sustainable growth</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>📊 Mumzworld Business Analytics Dashboard</p>
        <p>Built for Graduate Management Trainee Programme Assessment</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()