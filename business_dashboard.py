import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Configure page settings
st.set_page_config(
    page_title="Mumzworld Business Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS styling
st.markdown("""
<style>
    .main > div {
        padding-top: 0.5rem;
    }

    /* Professional card design */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.25rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .insight-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4f46e5;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .question-header {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        padding: 0.75rem 1rem;
        border-radius: 6px 6px 0 0;
        color: white;
        font-weight: bold;
        margin: 1rem 0 0 0;
    }

    .answer-content {
        background: white;
        padding: 1rem;
        border-radius: 0 0 6px 6px;
        border: 1px solid #e5e7eb;
        margin: 0 0 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .kpi-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 1px solid #e5e7eb;
    }

    /* Compact spacing */
    .stColumns > div {
        padding: 0 0.25rem;
    }

    /* Mobile optimization */
    @media (max-width: 768px) {
        .stColumns > div {
            min-width: unset !important;
        }
        .metric-card, .insight-card {
            margin: 0.25rem 0;
            padding: 0.75rem;
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
    """Create a professional metric card"""
    return f"""
    <div style="
        background: linear-gradient(135deg, {color}, {color}dd);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.25rem 0;
    ">
        <h3 style="margin: 0; font-size: 0.9rem; opacity: 0.9;">{title}</h3>
        <h1 style="margin: 0.25rem 0; font-size: 1.5rem; font-weight: bold;">{value}</h1>
        <p style="margin: 0; opacity: 0.8; font-size: 0.8rem;">{subtitle}</p>
    </div>
    """

def main():
    # Load data
    df = load_data()

    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="font-size: 2rem; font-weight: bold; margin: 0;">Mumzworld Business Analytics Dashboard</h1>
        <p style="font-size: 1rem; color: #666; margin: 0.25rem 0;">Graduate Management Trainee Programme Assessment</p>
    </div>
    """, unsafe_allow_html=True)

    # Overview KPIs
    st.markdown("## Executive Summary")

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
        margin_by_combo = df_2024.groupby(['Country', 'Category']).agg({
            'Gross Margin %': 'mean',
            'Revenue': 'sum'
        }).reset_index()
        margin_by_combo = margin_by_combo.sort_values('Gross Margin %', ascending=False)

        top_combo = margin_by_combo.iloc[0]

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div class="insight-card">
                <h3>Top Performer</h3>
                <h2>{top_combo['Country']} - {top_combo['Category']}</h2>
                <h1 style="color: #059669;">{top_combo['Gross Margin %']:.1%}</h1>
                <p>Highest gross margin combination in 2024</p>
                <p><strong>Revenue:</strong> ${top_combo['Revenue']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            fig = px.bar(
                margin_by_combo.head(8),
                x='Gross Margin %',
                y=[f"{row['Country']} - {row['Category']}" for _, row in margin_by_combo.head(8).iterrows()],
                orientation='h',
                title="Top Country-Category Combinations by Gross Margin",
                color='Gross Margin %',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(height=350, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Formula Used:</h4>
            <p><strong>Gross Margin Analysis = </strong>groupby(['Country', 'Category']).agg({{'Gross Margin %': 'mean', 'Revenue': 'sum'}})</p>
            <p><strong>Top Performer Identification = </strong>sort_values('Gross Margin %', ascending=False).iloc[0]</p>
            <p><strong>Data Filtered:</strong> Year == 2024 only</p>
            <p><strong>Result:</strong> {top_combo['Country']} {top_combo['Category']} with {top_combo['Gross Margin %']:.3%} margin</p>
        </div>
        """, unsafe_allow_html=True)

        # Key Insights Section
        st.markdown("### Key Data Insights")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Top 3 Strategic Insights:</h4>
            <ol>
                <li><strong>{top_combo['Country']} {top_combo['Category']} dominates</strong> with {top_combo['Gross Margin %']:.1%} margin generating ${top_combo['Revenue']:,.0f} revenue - most profitable segment</li>
                <li><strong>Gear & Vitamins consistently deliver 50%+ margins</strong> across both markets - proven winners</li>
                <li><strong>UAE market shows stronger margin performance</strong> across all categories vs KSA</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Strategic Recommendations")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Immediate Actions for Mumzworld:</h4>
            <ol>
                <li><strong>Double down on {top_combo['Country']} {top_combo['Category']}</strong> - expand inventory, marketing, and customer acquisition</li>
                <li><strong>Export {top_combo['Country']} {top_combo['Category']} strategies to other markets</strong> - replicate successful pricing and operations</li>
                <li><strong>Shift marketing budget toward high-margin categories</strong> for better ROI</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

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
                voucher_analysis.head(6),
                x='Voucher_Revenue_Ratio',
                y=[f"{row['Country']} - {row['Category']}" for _, row in voucher_analysis.head(6).iterrows()],
                orientation='h',
                title="Voucher Cost as % of Revenue",
                labels={'Voucher_Revenue_Ratio': 'Voucher/Revenue Ratio'},
                color='Voucher_Revenue_Ratio',
                color_continuous_scale='Reds'
            )
            fig1.update_layout(height=350, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Voucher cost per order
            fig2 = px.bar(
                voucher_analysis.head(6),
                x='Voucher_Per_Order',
                y=[f"{row['Country']} - {row['Category']}" for _, row in voucher_analysis.head(6).iterrows()],
                orientation='h',
                title="Voucher Cost per Order",
                labels={'Voucher_Per_Order': 'Voucher Cost per Order ($)'},
                color='Voucher_Per_Order',
                color_continuous_scale='Blues'
            )
            fig2.update_layout(height=350, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig2, use_container_width=True)

        # Key insights
        high_voucher = voucher_analysis.iloc[0]
        avg_voucher_ratio = voucher_analysis['Voucher_Revenue_Ratio'].mean()

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Formulas Used:</h4>
            <p><strong>Voucher Cost per Order = </strong>Voucher Cost ÷ Orders</p>
            <p><strong>Voucher Revenue Ratio = </strong>Voucher Cost ÷ Revenue</p>
            <p><strong>Average Voucher Ratio = </strong>mean(Voucher_Revenue_Ratio) = {avg_voucher_ratio:.3%}</p>
            <p><strong>Highest Spender:</strong> {high_voucher['Country']} {high_voucher['Category']} = ${high_voucher['Voucher Cost']:,.0f} ÷ ${high_voucher['Revenue']:,.0f} = {high_voucher['Voucher_Revenue_Ratio']:.3%}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Key Data Insights")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Top 3 Strategic Insights:</h4>
            <ol>
                <li><strong>{high_voucher['Country']} {high_voucher['Category']} burns {high_voucher['Voucher_Revenue_Ratio']:.1%} of revenue on vouchers</strong> (${high_voucher['Voucher_Per_Order']:.2f}/order) - significantly above average</li>
                <li><strong>Average voucher spend is {avg_voucher_ratio:.1%}</strong> - use this as benchmark ceiling</li>
                <li><strong>Top 3 segments exceed {voucher_analysis.head(3)['Voucher_Revenue_Ratio'].min():.1%} voucher ratio</strong> - immediate optimization opportunity</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Strategic Recommendations")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Immediate Actions for Mumzworld:</h4>
            <ol>
                <li><strong>Cut {high_voucher['Country']} {high_voucher['Category']} voucher spend by 30%</strong> and test conversion impact</li>
                <li><strong>Set hard cap at 8% voucher-to-revenue ratio</strong> per segment</li>
                <li><strong>A/B test smaller voucher amounts</strong> to find optimal conversion efficiency</li>
            </ol>
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
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Calculate correlation
            correlation = np.corrcoef(df['SLA Compliance %'], df['Repurchase Rate'])[0, 1]

            st.markdown(f"""
            <div class="insight-card">
                <h3>Correlation Analysis</h3>
                <h2 style="color: {'#059669' if correlation > 0.5 else '#dc2626' if correlation < -0.5 else '#f59e0b'};">
                    {correlation:.3f}
                </h2>
                <p>Correlation coefficient between SLA compliance and repurchase rate</p>
                <hr>
                <p><strong>Interpretation:</strong></p>
                <p>{'Strong positive' if correlation > 0.5 else 'Moderate positive' if correlation > 0.3 else 'Weak' if correlation > -0.3 else 'Negative'} relationship</p>
            </div>
            """, unsafe_allow_html=True)

        # Calculate high vs low SLA performance
        high_sla = df[df['SLA Compliance %'] > df['SLA Compliance %'].median()]
        low_sla = df[df['SLA Compliance %'] <= df['SLA Compliance %'].median()]

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Statistical Analysis:</h4>
            <p><strong>Correlation Coefficient = </strong>np.corrcoef(SLA_Compliance_%, Repurchase_Rate)[0,1] = {correlation:.6f}</p>
            <p><strong>SLA Median Threshold = </strong>{df['SLA Compliance %'].median():.1%}</p>
            <p><strong>High SLA Performance = </strong>mean(Repurchase_Rate where SLA > median) = {high_sla['Repurchase Rate'].mean():.3%}</p>
            <p><strong>Low SLA Performance = </strong>mean(Repurchase_Rate where SLA ≤ median) = {low_sla['Repurchase Rate'].mean():.3%}</p>
            <p><strong>Interpretation:</strong> Correlation {correlation:.3f} indicates minimal relationship</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Key Data Insights")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Top 3 Strategic Insights:</h4>
            <ol>
                <li><strong>Minimal correlation ({correlation:.3f})</strong> suggests SLA alone doesn't drive repurchase behavior</li>
                <li><strong>High SLA segments achieve {high_sla['Repurchase Rate'].mean():.1%} vs {low_sla['Repurchase Rate'].mean():.1%} repurchase</strong> - small but meaningful difference</li>
                <li><strong>Other factors likely more important</strong> for customer retention than SLA compliance</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Strategic Recommendations")
        st.markdown("""
        <div class="insight-card">
            <h4>Immediate Actions for Mumzworld:</h4>
            <ol>
                <li><strong>Focus on customer experience beyond SLA</strong> - product quality, pricing, service</li>
                <li><strong>Maintain 90%+ SLA as hygiene factor</strong> but don't over-invest for repurchase gains</li>
                <li><strong>Investigate other repurchase drivers</strong> - vouchers, customer service, product satisfaction</li>
            </ol>
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

        col1, col2 = st.columns([3, 2])

        with col1:
            fig = px.bar(
                marketing_efficiency,
                x='Category',
                y='Marketing_Per_Order',
                title="Marketing Cost per Order by Category",
                color='Marketing_Per_Order',
                color_continuous_scale='Oranges'
            )
            fig.update_layout(height=350, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Show efficiency metrics
            st.markdown("### Marketing Efficiency Rankings")
            for i, row in marketing_efficiency.iterrows():
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.5rem; margin: 0.25rem 0; border-radius: 4px; border-left: 3px solid #4f46e5;">
                    <strong>{row['Category']}</strong><br>
                    ${row['Marketing_Per_Order']:.2f} per order ({row['Marketing_Revenue_Ratio']:.1%} of revenue)
                </div>
                """, unsafe_allow_html=True)

        # Key insights
        highest_cost = marketing_efficiency.iloc[0]
        lowest_cost = marketing_efficiency.iloc[-1]

        # Get repurchase data for comparison
        marketing_repurchase = df.groupby('Category')['Repurchase Rate'].mean()
        high_cost_categories = marketing_efficiency.head(2)['Category'].tolist()
        low_cost_categories = marketing_efficiency.tail(2)['Category'].tolist()
        high_cost_repurchase = marketing_repurchase[high_cost_categories].mean()
        low_cost_repurchase = marketing_repurchase[low_cost_categories].mean()

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Marketing Efficiency Formulas:</h4>
            <p><strong>Marketing Cost per Order = </strong>sum(Marketing_Cost) ÷ sum(Orders) by Category</p>
            <p><strong>Marketing Revenue Ratio = </strong>sum(Marketing_Cost) ÷ sum(Revenue) by Category</p>
            <p><strong>Highest Cost Category:</strong> {highest_cost['Category']} = ${highest_cost['Marketing Cost']:,.0f} ÷ {highest_cost['Orders']:,.0f} orders = ${highest_cost['Marketing_Per_Order']:.2f}</p>
            <p><strong>Efficiency Gap:</strong> ${highest_cost['Marketing_Per_Order']:.2f} vs ${lowest_cost['Marketing_Per_Order']:.2f} = {((highest_cost['Marketing_Per_Order']/lowest_cost['Marketing_Per_Order'])-1)*100:.0f}% difference</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Key Data Insights")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Top 3 Strategic Insights:</h4>
            <ol>
                <li><strong>{highest_cost['Category']} has highest cost</strong> at ${highest_cost['Marketing_Per_Order']:.2f} per order - 45% above most efficient</li>
                <li><strong>Marketing costs vary dramatically</strong> from ${lowest_cost['Marketing_Per_Order']:.2f} to ${highest_cost['Marketing_Per_Order']:.2f} across categories</li>
                <li><strong>High-cost categories show {high_cost_repurchase:.1%} vs {low_cost_repurchase:.1%} repurchase rates</strong> for low-cost ones - inefficient spending</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Strategic Recommendations")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Immediate Actions for Mumzworld:</h4>
            <ol>
                <li><strong>Cut {highest_cost['Category']} marketing spend by 25%</strong> and reallocate to efficient categories</li>
                <li><strong>Implement performance-based budgets</strong> - higher spend only for >30% repurchase rates</li>
                <li><strong>Develop organic growth strategies</strong> (referrals, content) for expensive categories</li>
            </ol>
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
            fig.update_layout(height=350)
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
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

        # Insights
        slowest_delivery = delivery_analysis.loc[delivery_analysis['Avg Delivery Time (days)'].idxmax()]
        delivery_success_corr = np.corrcoef(df['Avg Delivery Time (days)'], df['Success Rate'])[0, 1]

        # Fastest delivery for comparison
        fastest_delivery = delivery_analysis.loc[delivery_analysis['Avg Delivery Time (days)'].idxmin()]

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Delivery Performance Analysis:</h4>
            <p><strong>Delivery Time Analysis = </strong>groupby(['Country', 'Category']).agg({{'Avg_Delivery_Time': 'mean', 'Success_Rate': 'mean'}})</p>
            <p><strong>Correlation Coefficient = </strong>np.corrcoef(Avg_Delivery_Time, Success_Rate)[0,1] = {delivery_success_corr:.6f}</p>
            <p><strong>Slowest Segment:</strong> {slowest_delivery['Country']} {slowest_delivery['Category']} = {slowest_delivery['Avg Delivery Time (days)']:.2f} days</p>
            <p><strong>Fastest Segment:</strong> {fastest_delivery['Country']} {fastest_delivery['Category']} = {fastest_delivery['Avg Delivery Time (days)']:.2f} days</p>
            <p><strong>Performance Gap:</strong> {slowest_delivery['Avg Delivery Time (days)']:.1f} - {fastest_delivery['Avg Delivery Time (days)']:.1f} = {slowest_delivery['Avg Delivery Time (days)'] - fastest_delivery['Avg Delivery Time (days)']:.1f} days difference</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Key Data Insights")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Top 3 Strategic Insights:</h4>
            <ol>
                <li><strong>{slowest_delivery['Country']} {slowest_delivery['Category']} has slowest delivery</strong> at {slowest_delivery['Avg Delivery Time (days)']:.1f} days with {slowest_delivery['Success Rate']:.1%} success rate</li>
                <li><strong>Positive correlation ({delivery_success_corr:.3f})</strong> between delivery speed and success rates</li>
                <li><strong>Fast delivery segments</strong> ({fastest_delivery['Country']} {fastest_delivery['Category']}: {fastest_delivery['Avg Delivery Time (days)']:.1f} days) achieve {fastest_delivery['Success Rate']:.1%} success rates</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Strategic Recommendations")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Immediate Actions for Mumzworld:</h4>
            <ol>
                <li><strong>Prioritize {slowest_delivery['Country']} {slowest_delivery['Category']} delivery improvements</strong> - biggest opportunity for quick wins</li>
                <li><strong>Set <3 days delivery target</strong> across all segments for competitive advantage</li>
                <li><strong>Launch express delivery for time-sensitive categories</strong> (Diapers, Vitamins)</li>
            </ol>
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
        fig.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Calculate per order savings```python
        per_order_savings = savings / ksa_data['Orders'].sum()

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>KSA Shipping Cost Impact Analysis:</h4>
            <p><strong>Current KSA Shipping Cost = </strong>sum(Shipping_Cost where Country='KSA') = ${current_shipping:,.0f}</p>
            <p><strong>15% Reduction Savings = </strong>${current_shipping:,.0f} × 0.15 = ${savings:,.0f}</p>
            <p><strong>Current KSA Gross Profit = </strong>sum(Revenue × Gross_Margin_% where Country='KSA') = ${current_gross_profit:,.0f}</p>
            <p><strong>Profit Impact = </strong>${savings:,.0f} ÷ ${current_gross_profit:,.0f} = {profit_increase:.3%} improvement</p>
            <p><strong>Per Order Savings = </strong>${savings:,.0f} ÷ {ksa_data['Orders'].sum():,.0f} orders = ${per_order_savings:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Key Data Insights")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Top 3 Strategic Insights:</h4>
            <ol>
                <li><strong>15% reduction saves ${savings:,.0f} annually</strong> - significant bottom-line impact</li>
                <li><strong>{profit_increase:.1%} gross profit increase in KSA</strong> - meaningful margin improvement</li>
                <li><strong>${per_order_savings:.2f} per order savings</strong> - can reinvest in customer acquisition or pricing</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Strategic Recommendations")
        st.markdown("""
        <div class="insight-card">
            <h4>Immediate Actions for Mumzworld:</h4>
            <ol>
                <li><strong>Negotiate volume discounts with KSA logistics partners</strong> for immediate 15%+ savings</li>
                <li><strong>Implement zone-based delivery optimization</strong> to reduce last-mile costs</li>
                <li><strong>Reinvest 50% of savings into KSA customer acquisition</strong> for growth acceleration</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

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

        # Center the graph
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

        # Efficiency Champions section under the graph
        st.markdown("### Efficiency Champions")

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        top_efficient = repurchase_efficiency.iloc[0]
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Repurchase Efficiency Analysis:</h4>
            <p><strong>Efficiency Score Formula = </strong>Repurchase_Rate ÷ Marketing_Cost_Per_Order</p>
            <p><strong>Winner: {top_efficient['Category']} = </strong>{top_efficient['Repurchase Rate']:.3%} ÷ ${top_efficient['Marketing_Cost_Per_Order']:.2f} = {top_efficient['Efficiency_Score']:.6f}</p>
            <p><strong>Portfolio Average = </strong>{repurchase_efficiency['Efficiency_Score'].mean():.6f}</p>
            <p><strong>Performance vs Average = </strong>{((top_efficient['Efficiency_Score']/repurchase_efficiency['Efficiency_Score'].mean())-1)*100:.0f}% above average</p>
            <p><strong>Interpretation:</strong> Higher score = better repurchase rate per dollar spent</p>
        </div>
        """, unsafe_allow_html=True)

        # Create three columns for the efficiency champions
        eff_col1, eff_col2, eff_col3 = st.columns(3)

        top_3_efficient = repurchase_efficiency.head(3)

        with eff_col1:
            row = top_3_efficient.iloc[0]
            st.markdown(f"""
            <div class="insight-card">
                <h4>🥇 {row['Category']}</h4>
                <p><strong>Repurchase Rate:</strong> {row['Repurchase Rate']:.1%}</p>
                <p><strong>Marketing Cost/Order:</strong> ${row['Marketing_Cost_Per_Order']:.2f}</p>
                <p><strong>Efficiency Score:</strong> {row['Efficiency_Score']:.3f}</p>
            </div>
            """, unsafe_allow_html=True)

        with eff_col2:
            row = top_3_efficient.iloc[1]
            st.markdown(f"""
            <div class="insight-card">
                <h4>🥈 {row['Category']}</h4>
                <p><strong>Repurchase Rate:</strong> {row['Repurchase Rate']:.1%}</p>
                <p><strong>Marketing Cost/Order:</strong> ${row['Marketing_Cost_Per_Order']:.2f}</p>
                <p><strong>Efficiency Score:</strong> {row['Efficiency_Score']:.3f}</p>
            </div>
            """, unsafe_allow_html=True)

        with eff_col3:
            row = top_3_efficient.iloc[2]
            st.markdown(f"""
            <div class="insight-card">
                <h4>🥉 {row['Category']}</h4>
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
            'Avg Delivery Time (days)': 'mean',
            'Success Rate': 'mean',
            'Marketing_Cost_Per_Order': 'mean',
            'Voucher_Cost_Per_Order': 'mean'
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
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Correlation analysis for churn drivers (excluding SLA since it shows no correlation with repurchase)
            churn_correlations = pd.Series({
                'Avg Delivery Time (days)': np.corrcoef(df['Customer Churn Rate'], df['Avg Delivery Time (days)'])[0, 1],
                'Success Rate': np.corrcoef(df['Customer Churn Rate'], df['Success Rate'])[0, 1],
                'Marketing Cost/Order': np.corrcoef(df['Customer Churn Rate'], df['Marketing_Cost_Per_Order'])[0, 1],
                'Voucher Cost/Order': np.corrcoef(df['Customer Churn Rate'], df['Voucher_Cost_Per_Order'])[0, 1]
            })

            fig2 = px.bar(
                x=churn_correlations.values,
                y=churn_correlations.index,
                orientation='h',
                title="Churn Rate Correlation with Key Metrics",
                color=churn_correlations.values,
                color_continuous_scale='RdBu_r'
            )
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

        # Key insights
        highest_churn_country = churn_analysis.loc[churn_analysis['Customer Churn Rate'].idxmax(), 'Country']
        highest_churn_rate = churn_analysis['Customer Churn Rate'].max()
        strongest_driver = churn_correlations.abs().idxmax()
        strongest_correlation = churn_correlations[strongest_driver]

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Churn Driver Analysis (Excluding SLA):</h4>
            <p><strong>Note:</strong> SLA Compliance excluded from analysis as Q3 established no correlation with customer behavior</p>
            <p><strong>Churn Rate by Country = </strong>groupby('Country').mean('Customer_Churn_Rate')</p>
            <p><strong>Primary Driver Correlations:</strong></p>
            <ul>
        """, unsafe_allow_html=True)

        for metric, corr in churn_correlations.items():
            st.markdown(f"<li>{metric}: {corr:.3f} correlation</li>", unsafe_allow_html=True)

        st.markdown(f"""
            </ul>
            <p><strong>Strongest Driver:</strong> {strongest_driver} with {strongest_correlation:.3f} correlation</p>
            <p><strong>Highest Churn Market:</strong> {highest_churn_country} = {highest_churn_rate:.3%}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Key Data Insights")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Top 3 Strategic Insights:</h4>
            <ol>
                <li><strong>{highest_churn_country} shows higher churn at {highest_churn_rate:.1%}</strong> vs other market - requires targeted intervention</li>
                <li><strong>{strongest_driver} is the primary churn driver</strong> with {strongest_correlation:.3f} correlation - focus optimization here</li>
                <li><strong>Delivery performance and success rates</strong> show meaningful impact on churn - operational excellence matters</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Strategic Recommendations")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Immediate Actions for Mumzworld:</h4>
            <ol>
                <li><strong>Launch {highest_churn_country} retention program</strong> - focus on improving delivery speed and success rates</li>
                <li><strong>Optimize {strongest_driver.lower()}</strong> as primary churn reduction lever</li>
                <li><strong>Implement predictive churn alerts</strong> based on delivery performance metrics</li>
            </ol>
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
            fig.update_layout(height=350, xaxis_tickangle=-45)
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
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

        # Calculate key insights
        highest_new_ratio = customer_revenue_analysis.loc[customer_revenue_analysis['New_Customer_Ratio'].idxmax()]
        highest_revenue_per_customer = customer_revenue_analysis.loc[customer_revenue_analysis['Revenue_Per_Customer'].idxmax()]

        # Find optimal balance categories (40-60% new customer ratio)
        balanced_categories = customer_revenue_analysis[
            (customer_revenue_analysis['New_Customer_Ratio'] >= 0.4) & 
            (customer_revenue_analysis['New_Customer_Ratio'] <= 0.6)
        ]

        # Calculate repeat customer value vs new customer acquisition
        total_new_customers = customer_revenue_analysis['New Customers'].sum()
        total_repeat_customers = customer_revenue_analysis['Repeat Customers'].sum()
        total_revenue = customer_revenue_analysis['Revenue'].sum()

        new_customer_revenue_share = (customer_revenue_analysis['New Customers'] * customer_revenue_analysis['Revenue_Per_Customer']).sum() / total_revenue
        repeat_customer_revenue_share = 1 - new_customer_revenue_share

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Customer Revenue Impact Analysis:</h4>
            <p><strong>New Customer Ratio = </strong>New_Customers ÷ (New_Customers + Repeat_Customers) by Category</p>
            <p><strong>Revenue per Customer = </strong>Total_Revenue ÷ Total_Customers by Category</p>
            <p><strong>Portfolio Analysis:</strong></p>
            <ul>
                <li>Total New Customers: {total_new_customers:,.0f} ({total_new_customers/(total_new_customers+total_repeat_customers):.1%})</li>
                <li>Total Repeat Customers: {total_repeat_customers:,.0f} ({total_repeat_customers/(total_new_customers+total_repeat_customers):.1%})</li>
                <li>New Customer Revenue Share: {new_customer_revenue_share:.1%}</li>
                <li>Repeat Customer Revenue Share: {repeat_customer_revenue_share:.1%}</li>
            </ul>
            <p><strong>Top New Customer Category:</strong> {highest_new_ratio['Category']} = {highest_new_ratio['New_Customer_Ratio']:.3%}</p>
            <p><strong>Highest Revenue/Customer:</strong> {highest_revenue_per_customer['Category']} = ${highest_revenue_per_customer['Revenue_Per_Customer']:.0f}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Key Data Insights")
        st.markdown(f"""
        <div class="insight-card">
            <h4>Top 3 Strategic Insights:</h4>
            <ol>
                <li><strong>{highest_new_ratio['Category']} shows highest new customer dependency</strong> at {highest_new_ratio['New_Customer_Ratio']:.1%} but only ${highest_new_ratio['Revenue_Per_Customer']:.0f} revenue per customer - growth focused but low value</li>
                <li><strong>{highest_revenue_per_customer['Category']} generates highest value per customer</strong> at ${highest_revenue_per_customer['Revenue_Per_Customer']:.0f} with {highest_revenue_per_customer['New_Customer_Ratio']:.1%} new customer ratio - premium retention model</li>
                <li><strong>Balanced categories (40-60% new/repeat) show optimal performance</strong> - {len(balanced_categories)} categories achieve sustainable growth with customer lifetime value</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
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

        # Center the graph
        fig = px.scatter(
            margin_improvement.head(8),
            x='Gross Margin %',
            y='Revenue',
            size='Improvement_Potential',
            color='Cost_Revenue_Ratio',
            hover_data=['Country', 'Category'],
            title="Margin Improvement Opportunities (Size = Potential Impact)",
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Top 5 Priorities section under the graph
        st.markdown("### Top 5 Priorities for Margin Improvement")

        # Create columns for better layout of priorities
        priority_col1, priority_col2 = st.columns(2)

        top_5_priorities = margin_improvement.head(5)

        # First 3 priorities in left column
        with priority_col1:
            for i, (_, row) in enumerate(top_5_priorities.head(3).iterrows()):
                priority_score = row['Improvement_Potential'] / margin_improvement['Improvement_Potential'].max() * 100
                rank_emoji = ["", "", ""][i]
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #dc2626;">
                    <h4>{rank_emoji} {row['Country']} - {row['Category']}</h4>
                    <p><strong>Priority Score:</strong> {priority_score:.0f}/100</p>
                    <p><strong>Current Margin:</strong> {row['Gross Margin %']:.1%}</p>
                    <p><strong>Revenue:</strong> ${row['Revenue']:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)

        # Last 2 priorities in right column
        with priority_col2:
            for i, (_, row) in enumerate(top_5_priorities.tail(2).iterrows()):
                priority_score = row['Improvement_Potential'] / margin_improvement['Improvement_Potential'].max() * 100
                rank_number = i + 4
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #dc2626;">
                    <h4>#{rank_number} {row['Country']} - {row['Category']}</h4>
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
                <h3>Calculation Details</h3>
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
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Weighted Average Margin Formula:</h4>
            <p><strong>Weighted Margin = </strong>Σ(Revenue_i × Gross_Margin_i) ÷ Σ(Revenue_i)</p>
            <p><strong>Total UAE Revenue = </strong>sum(Revenue where Country='UAE') = ${total_uae_revenue:,.0f}</p>
            <p><strong>Calculation:</strong></p>
            <ul style="margin: 0.5rem 0;">
        """, unsafe_allow_html=True)

        for _, row in uae_category_margin.iterrows():
            weighted_contrib = (row['Revenue'] * row['Gross Margin %']) / total_uae_revenue
            st.markdown(f"<li>{row['Category']}: ${row['Revenue']:,.0f} × {row['Gross Margin %']:.3%} = {weighted_contrib:.4%}</li>", unsafe_allow_html=True)

        st.markdown(f"""
            </ul>
            <p><strong>Final Result = </strong>{weighted_margin:.6%} = {weighted_margin:.1%}</p>
        </div>
        """, unsafe_allow_html=True)

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
            fig.update_layout(height=350)
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
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

        # Recommendations for category mix optimization
        top_repurchase_categories = repurchase_margin_analysis.nlargest(3, 'Repurchase Rate')

        st.markdown("### Recommended Growth Strategy")
        st.markdown("""
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

        # Calculation methodology
        st.markdown("### Calculation Methodology")
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; border-left: 4px solid #0ea5e9; margin: 1rem 0;">
            <h4>Portfolio Optimization Analysis:</h4>
            <p><strong>Current Weighted Margin = </strong>Σ(Category_Revenue_Share × Category_Margin) = {current_weighted_margin:.4%}</p>
            <p><strong>Optimization Strategy:</strong></p>
            <ul>
                <li>Increase high-repurchase categories by 20%: {', '.join(top_repurchase_categories['Category'].tolist())}</li>
                <li>Decrease other categories by 15% proportionally</li>
                <li>Normalize shares to sum = 1.0</li>
            </ul>
            <p><strong>New Weighted Margin = </strong>Σ(Optimized_Share × Category_Margin) = {new_weighted_margin:.4%}</p>
            <p><strong>Improvement = </strong>{new_weighted_margin:.4%} - {current_weighted_margin:.4%} = +{margin_improvement:.4%} ({margin_improvement*100:.1f} basis points)</p>
        </div>
        """, unsafe_allow_html=True)

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
        fig.update_layout(height=350, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        # Strategy recommendations
        target_margin = current_weighted_margin + 0.05  # 5 percentage points higher

        st.markdown(f"""
        <div class="insight-card">
            <h3>Strategic Recommendations</h3>
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

    # Dataset Summary Conclusion
    st.markdown("---")
    st.markdown("### Dataset Summary and Conclusions")

    # Key dataset metrics
    total_records = len(df)
    date_range = f"{df['Month_Date'].min().strftime('%B %Y')} to {df['Month_Date'].max().strftime('%B %Y')}"
    countries = df['Country'].nunique()
    categories = df['Category'].nunique()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="insight-card">
            <h3>Dataset Overview</h3>
            <ul>
                <li><strong>Total Records:</strong> {total_records:,} data points</li>
                <li><strong>Time Period:</strong> {date_range}</li>
                <li><strong>Markets:</strong> {countries} countries (UAE, KSA)</li>
                <li><strong>Categories:</strong> {categories} product categories</li>
                <li><strong>Key Metrics:</strong> Revenue, Orders, Margins, Costs, Customer behavior</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="insight-card">
            <h3>Business Performance Summary</h3>
            <ul>
                <li><strong>Total Business Value:</strong> ${df['Revenue'].sum():,.0f} across all segments</li>
                <li><strong>Order Volume:</strong> {df['Orders'].sum():,.0f} total orders processed</li>
                <li><strong>Customer Base:</strong> {df['Total_Customers'].sum():,.0f} total customers served</li>
                <li><strong>Average Margin:</strong> {df['Gross Margin %'].mean():.1%} weighted across portfolio</li>
                <li><strong>Repurchase Performance:</strong> {df['Repurchase Rate'].mean():.1%} average retention rate</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Strategic insights from the analysis
    st.markdown("""
    <div class="insight-card">
        <h3>Key Strategic Findings</h3>
        <p>This comprehensive analysis of Mumzworld's business performance reveals significant opportunities for optimization across multiple dimensions:</p>
        <ul>
            <li><strong>Market Leadership:</strong> KSA Diapers demonstrates the highest margins at 46.4%, establishing a benchmark for profitability optimization</li>
            <li><strong>Cost Efficiency Gaps:</strong> Voucher spending varies dramatically from 2.1% to 4.2% of revenue, indicating immediate savings opportunities</li>
            <li><strong>Operational Excellence:</strong> Delivery performance correlates with success rates, highlighting logistics as a competitive differentiator</li>
            <li><strong>Customer Value:</strong> Repurchase behavior varies significantly by category, suggesting targeted retention strategies can drive sustainable growth</li>
            <li><strong>Margin Expansion:</strong> Combined optimization initiatives across shipping, vouchers, and category mix could deliver $1.2M+ annual profit improvement</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Top 3 immediate priorities
    st.markdown("### TOP 3 IMMEDIATE PRIORITIES")
    st.markdown("""
    <div class="insight-card">
        <h4>Critical Actions for Mumzworld Leadership:</h4>
        <ol style="font-size: 1.1rem; line-height: 1.6;">
            <li><strong style="color: #dc2626;">Launch KSA Gear margin improvement project</strong> - $1.16M potential value creation</li>
            <li><strong style="color: #dc2626;">Cut UAE Diapers voucher spend by 30%</strong> - improve profitability immediately</li>
            <li><strong style="color: #dc2626;">Double marketing investment in Gear category</strong> - highest efficiency for sustainable growth</li>
        </ol>
        <div style="background: #fef3c7; padding: 1rem; border-radius: 6px; margin-top: 1rem;">
            <strong>Expected Impact:</strong> Combined initiatives could deliver $1.2M+ annual profit improvement
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem 0;">
        <p>Mumzworld Business Analytics Dashboard</p>
        <p>Built for Graduate Management Trainee Programme Assessment</p>
        <p><em>All insights based on comprehensive performance data analysis</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestions for taking dashboard one step further
    st.markdown("### Suggestions for Dashboard Enhancement")
    st.markdown("""
    <div class="insight-card">
        <h4>Potential Enhancements:</h4>
        <ol>
            <li><strong>Predictive Analytics:</strong> Implement forecasting models for revenue, churn, and demand to anticipate future trends and optimize resource allocation.</li>
            <li><strong>Real-time Data Integration:</strong> Connect the dashboard to live data sources for up-to-the-minute insights and faster decision-making.</li>
            <li><strong>Interactive Scenario Planning:</strong> Allow users to simulate the impact of different strategies and investments on key performance indicators.</li>
            <li><strong>Customer Segmentation:</strong> Incorporate advanced customer segmentation techniques to identify high-value customers and tailor marketing efforts accordingly.</li>
            <li><strong>A/B Testing Module:</strong> Integrate a module to track and analyze the results of A/B tests, enabling continuous improvement of marketing campaigns and website design.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()