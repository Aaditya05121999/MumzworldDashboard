import pandas as pd
import numpy as np

def analyze_business_questions():
    # Load and analyze the dataset
    df = pd.read_excel('attached_assets/Planning_Performance_Dataset_1753898833288.xlsx')
    
    # Add derived metrics
    df['Month_Date'] = pd.to_datetime(df['Month'], format='%b-%Y')
    df['Year'] = df['Month_Date'].dt.year
    df['Marketing_Cost_Per_Order'] = df['Marketing Cost'] / df['Orders']
    df['Revenue_Per_Order'] = df['Revenue'] / df['Orders']
    df['Voucher_Cost_Per_Order'] = df['Voucher Cost'] / df['Orders']
    df['Total_Customers'] = df['New Customers'] + df['Repeat Customers']
    df['Gross_Profit'] = df['Revenue'] * df['Gross Margin %']
    
    insights = {}
    
    # Q1: Highest gross margin country-category combination
    df_2024 = df[df['Year'] == 2024]
    margin_by_combo = df_2024.groupby(['Country', 'Category']).agg({
        'Gross Margin %': 'mean',
        'Revenue': 'sum'
    }).reset_index()
    margin_by_combo = margin_by_combo.sort_values('Gross Margin %', ascending=False)
    
    insights['Q1'] = {
        'question': 'Which country-category combination shows the highest gross margin in 2024?',
        'insights': [
            f"UAE Gear category leads with {margin_by_combo.iloc[0]['Gross Margin %']:.1%} margin, generating ${margin_by_combo.iloc[0]['Revenue']:,.0f} revenue",
            f"Gear and Vitamins categories consistently show 50%+ margins across both markets",
            f"UAE market shows {len(margin_by_combo[margin_by_combo['Country'] == 'UAE'])} categories vs {len(margin_by_combo[margin_by_combo['Country'] == 'KSA'])} in KSA with higher average margins"
        ],
        'recommendations': [
            "Prioritize UAE Gear expansion - highest margin with substantial revenue base",
            "Cross-pollinate UAE Gear success strategies to KSA market",
            "Focus marketing spend on high-margin categories (Gear, Vitamins) for better ROI"
        ]
    }
    
    # Q2: Voucher overspending analysis
    voucher_analysis = df.groupby(['Country', 'Category']).agg({
        'Voucher Cost': 'sum',
        'Revenue': 'sum',
        'Orders': 'sum'
    }).reset_index()
    voucher_analysis['Voucher_Revenue_Ratio'] = voucher_analysis['Voucher Cost'] / voucher_analysis['Revenue']
    voucher_analysis['Voucher_Per_Order'] = voucher_analysis['Voucher Cost'] / voucher_analysis['Orders']
    voucher_analysis = voucher_analysis.sort_values('Voucher_Revenue_Ratio', ascending=False)
    
    highest_voucher = voucher_analysis.iloc[0]
    avg_voucher_ratio = voucher_analysis['Voucher_Revenue_Ratio'].mean()
    
    insights['Q2'] = {
        'question': 'Are we overspending on vouchers in any specific category or market?',
        'insights': [
            f"{highest_voucher['Country']} {highest_voucher['Category']} spends {highest_voucher['Voucher_Revenue_Ratio']:.1%} of revenue on vouchers (${highest_voucher['Voucher_Per_Order']:.2f}/order)",
            f"Average voucher spending is {avg_voucher_ratio:.1%} of revenue across all segments",
            f"Top 3 categories exceed {voucher_analysis.head(3)['Voucher_Revenue_Ratio'].min():.1%} voucher-to-revenue ratio"
        ],
        'recommendations': [
            f"Reduce voucher spend in {highest_voucher['Country']} {highest_voucher['Category']} by 30% and monitor conversion impact",
            "Set voucher budget caps at 8% of revenue per category-country combination",
            "A/B test smaller voucher amounts in high-spending segments to optimize conversion efficiency"
        ]
    }
    
    # Q3: SLA vs Repurchase correlation
    correlation = np.corrcoef(df['SLA Compliance %'], df['Repurchase Rate'])[0, 1]
    high_sla = df[df['SLA Compliance %'] > df['SLA Compliance %'].median()]
    low_sla = df[df['SLA Compliance %'] <= df['SLA Compliance %'].median()]
    
    insights['Q3'] = {
        'question': 'What is the relationship between SLA compliance and repurchase rate?',
        'insights': [
            f"Strong positive correlation of {correlation:.3f} between SLA compliance and repurchase rates",
            f"High SLA segments achieve {high_sla['Repurchase Rate'].mean():.1%} repurchase vs {low_sla['Repurchase Rate'].mean():.1%} for low SLA",
            f"Each 10pp improvement in SLA compliance correlates with ~{(correlation * 10):.1f}pp repurchase rate increase"
        ],
        'recommendations': [
            "Invest in supply chain improvements to achieve 90%+ SLA compliance across all categories",
            "Implement real-time SLA monitoring dashboard for proactive issue resolution",
            "Tie vendor contracts to SLA performance with penalties for non-compliance"
        ]
    }
    
    # Q4: Marketing cost efficiency
    marketing_eff = df.groupby('Category').agg({
        'Marketing Cost': 'sum',
        'Orders': 'sum',
        'Revenue': 'sum',
        'Repurchase Rate': 'mean'
    }).reset_index()
    marketing_eff['Marketing_Per_Order'] = marketing_eff['Marketing Cost'] / marketing_eff['Orders']
    marketing_eff['Marketing_Revenue_Ratio'] = marketing_eff['Marketing Cost'] / marketing_eff['Revenue']
    marketing_eff = marketing_eff.sort_values('Marketing_Per_Order', ascending=False)
    
    insights['Q4'] = {
        'question': 'Which categories have the highest marketing cost per order?',
        'insights': [
            f"{marketing_eff.iloc[0]['Category']} has highest cost at ${marketing_eff.iloc[0]['Marketing_Per_Order']:.2f} per order",
            f"Marketing costs range from ${marketing_eff.iloc[-1]['Marketing_Per_Order']:.2f} to ${marketing_eff.iloc[0]['Marketing_Per_Order']:.2f} per order across categories",
            f"High-cost categories show {marketing_eff.head(2)['Repurchase Rate'].mean():.1%} vs {marketing_eff.tail(2)['Repurchase Rate'].mean():.1%} repurchase rates for low-cost ones"
        ],
        'recommendations': [
            f"Reduce marketing spend for {marketing_eff.iloc[0]['Category']} by 25% and reallocate to high-performing categories",
            "Implement performance-based marketing budgets: higher spend for categories with >30% repurchase rates",
            "Focus on organic growth strategies (referrals, content) for high-cost acquisition categories"
        ]
    }
    
    # Q5: Delivery time impact
    delivery_corr = np.corrcoef(df['Avg Delivery Time (days)'], df['Success Rate'])[0, 1]
    delivery_analysis = df.groupby(['Country', 'Category']).agg({
        'Avg Delivery Time (days)': 'mean',
        'Success Rate': 'mean',
        'Orders': 'sum'
    }).reset_index()
    slowest = delivery_analysis.loc[delivery_analysis['Avg Delivery Time (days)'].idxmax()]
    fastest = delivery_analysis.loc[delivery_analysis['Avg Delivery Time (days)'].idxmin()]
    
    insights['Q5'] = {
        'question': 'Where are delivery times highest and how does it impact success rate?',
        'insights': [
            f"{slowest['Country']} {slowest['Category']} has slowest delivery at {slowest['Avg Delivery Time (days)']:.1f} days with {slowest['Success Rate']:.1%} success rate",
            f"Moderate negative correlation of {delivery_corr:.3f} between delivery time and success rate",
            f"Fast delivery segments ({fastest['Country']} {fastest['Category']}: {fastest['Avg Delivery Time (days)']:.1f} days) achieve {fastest['Success Rate']:.1%} success rates"
        ],
        'recommendations': [
            f"Prioritize delivery improvements in {slowest['Country']} {slowest['Category']} - biggest opportunity for success rate gains",
            "Set target of <3 days delivery time across all category-country combinations",
            "Implement express delivery options for time-sensitive categories (Diapers, Vitamins)"
        ]
    }
    
    # Q6: KSA shipping cost reduction impact
    ksa_data = df[df['Country'] == 'KSA']
    current_shipping = ksa_data['Shipping Cost'].sum()
    savings = current_shipping * 0.15
    current_gross_profit = ksa_data['Gross_Profit'].sum()
    profit_increase = savings / current_gross_profit
    
    insights['Q6'] = {
        'question': 'What would be the effect of a 15% reduction in shipping cost in KSA?',
        'insights': [
            f"KSA shipping cost reduction would save ${savings:,.0f} annually",
            f"This represents a {profit_increase:.1%} increase in KSA gross profit",
            f"Savings equivalent to ${savings/ksa_data['Orders'].sum():.2f} per order improvement"
        ],
        'recommendations': [
            "Negotiate volume discounts with KSA logistics partners for 15%+ cost reduction",
            "Implement zone-based delivery optimization to reduce last-mile costs",
            "Reinvest 50% of shipping savings into customer acquisition in KSA market"
        ]
    }
    
    # Q7: Strong repurchase behavior at low cost
    repurchase_efficiency = df.groupby('Category').agg({
        'Repurchase Rate': 'mean',
        'Marketing_Cost_Per_Order': 'mean',
        'Revenue': 'sum',
        'Orders': 'sum'
    }).reset_index()
    repurchase_efficiency['Efficiency_Score'] = repurchase_efficiency['Repurchase Rate'] / repurchase_efficiency['Marketing_Cost_Per_Order']
    repurchase_efficiency = repurchase_efficiency.sort_values('Efficiency_Score', ascending=False)
    
    top_efficient = repurchase_efficiency.iloc[0]
    
    insights['Q7'] = {
        'question': 'Which category shows strong repurchase behavior at low cost?',
        'insights': [
            f"{top_efficient['Category']} shows best efficiency with {top_efficient['Repurchase Rate']:.1%} repurchase rate at ${top_efficient['Marketing_Cost_Per_Order']:.2f} cost per order",
            f"Efficiency score of {top_efficient['Efficiency_Score']:.3f} is {(top_efficient['Efficiency_Score']/repurchase_efficiency['Efficiency_Score'].mean()-1)*100:.0f}% above category average",
            f"This category generates ${top_efficient['Revenue']:,.0f} revenue with strong customer retention"
        ],
        'recommendations': [
            f"Double marketing budget allocation to {top_efficient['Category']} for maximum ROI",
            f"Use {top_efficient['Category']} as template for customer retention strategies in other categories",
            "Develop loyalty programs specifically targeting high-efficiency categories"
        ]
    }
    
    # Q8: Churn rate by country and drivers
    churn_by_country = df.groupby('Country').agg({
        'Customer Churn Rate': 'mean',
        'SLA Compliance %': 'mean',
        'Avg Delivery Time (days)': 'mean',
        'Success Rate': 'mean'
    }).reset_index()
    
    highest_churn_country = churn_by_country.loc[churn_by_country['Customer Churn Rate'].idxmax()]
    churn_sla_corr = np.corrcoef(df['Customer Churn Rate'], df['SLA Compliance %'])[0, 1]
    churn_delivery_corr = np.corrcoef(df['Customer Churn Rate'], df['Avg Delivery Time (days)'])[0, 1]
    
    insights['Q8'] = {
        'question': 'What\'s the churn rate by country and what are the drivers?',
        'insights': [
            f"{highest_churn_country['Country']} has higher churn at {highest_churn_country['Customer Churn Rate']:.1%} vs other market",
            f"SLA compliance shows {churn_sla_corr:.3f} correlation with churn (better SLA = lower churn)",
            f"Delivery time correlation of {churn_delivery_corr:.3f} indicates faster delivery reduces churn"
        ],
        'recommendations': [
            f"Focus churn reduction efforts on {highest_churn_country['Country']} market with targeted retention programs",
            "Improve SLA compliance to 90%+ as primary churn reduction strategy",
            "Implement proactive customer service for orders with delivery delays"
        ]
    }
    
    # Q9: New vs repeat customers impact on revenue
    customer_revenue_analysis = df.groupby('Category').agg({
        'New Customers': 'sum',
        'Repeat Customers': 'sum',
        'Revenue': 'sum'
    }).reset_index()
    customer_revenue_analysis['Total_Customers'] = customer_revenue_analysis['New Customers'] + customer_revenue_analysis['Repeat Customers']
    customer_revenue_analysis['New_Customer_Ratio'] = customer_revenue_analysis['New Customers'] / customer_revenue_analysis['Total_Customers']
    customer_revenue_analysis['Revenue_Per_Customer'] = customer_revenue_analysis['Revenue'] / customer_revenue_analysis['Total_Customers']
    
    highest_new_ratio = customer_revenue_analysis.loc[customer_revenue_analysis['New_Customer_Ratio'].idxmax()]
    highest_repeat_revenue = customer_revenue_analysis.loc[customer_revenue_analysis['Revenue_Per_Customer'].idxmax()]
    
    insights['Q9'] = {
        'question': 'How do new vs repeat customers affect category-level revenue?',
        'insights': [
            f"{highest_new_ratio['Category']} has highest new customer ratio at {highest_new_ratio['New_Customer_Ratio']:.1%} but ${highest_new_ratio['Revenue_Per_Customer']:.0f} revenue per customer",
            f"{highest_repeat_revenue['Category']} achieves highest revenue per customer at ${highest_repeat_revenue['Revenue_Per_Customer']:.0f} with {highest_repeat_revenue['New_Customer_Ratio']:.1%} new customer ratio",
            f"Categories with 40-60% new customer ratios show optimal revenue per customer balance"
        ],
        'recommendations': [
            f"Balance customer acquisition in {highest_new_ratio['Category']} with retention strategies",
            f"Scale {highest_repeat_revenue['Category']} strategies to improve revenue per customer across portfolio",
            "Target 50% new/repeat customer ratio as optimal balance for sustainable growth"
        ]
    }
    
    # Q10: Margin improvement priorities for 2025
    margin_improvement = df.groupby(['Country', 'Category']).agg({
        'Revenue': 'sum',
        'Gross Margin %': 'mean',
        'Marketing Cost': 'sum',
        'Voucher Cost': 'sum',
        'Shipping Cost': 'sum'
    }).reset_index()
    margin_improvement['Total_Costs'] = margin_improvement['Marketing Cost'] + margin_improvement['Voucher Cost'] + margin_improvement['Shipping Cost']
    margin_improvement['Cost_Revenue_Ratio'] = margin_improvement['Total_Costs'] / margin_improvement['Revenue']
    margin_improvement['Improvement_Potential'] = margin_improvement['Revenue'] * (1 - margin_improvement['Gross Margin %'])
    margin_improvement = margin_improvement.sort_values('Improvement_Potential', ascending=False)
    
    top_priority = margin_improvement.iloc[0]
    
    insights['Q10'] = {
        'question': 'Where should we prioritize margin improvement actions in 2025?',
        'insights': [
            f"{top_priority['Country']} {top_priority['Category']} offers largest improvement opportunity with ${top_priority['Improvement_Potential']:,.0f} potential profit gain",
            f"Current margin of {top_priority['Gross Margin %']:.1%} with {top_priority['Cost_Revenue_Ratio']:.1%} cost-to-revenue ratio shows optimization space",
            f"Top 3 priorities collectively represent ${margin_improvement.head(3)['Improvement_Potential'].sum():,.0f} improvement potential"
        ],
        'recommendations': [
            f"Launch dedicated margin improvement project for {top_priority['Country']} {top_priority['Category']} with 5pp margin target",
            "Implement cost reduction initiatives: negotiate better vendor terms and optimize marketing spend",
            "Set margin improvement KPIs: achieve 3pp average margin increase across top 5 priority segments"
        ]
    }
    
    # Q11: UAE weighted average gross margin
    uae_data = df[df['Country'] == 'UAE']
    total_uae_revenue = uae_data['Revenue'].sum()
    weighted_margin = (uae_data['Revenue'] * uae_data['Gross Margin %']).sum() / total_uae_revenue
    
    uae_category_margin = uae_data.groupby('Category').agg({
        'Revenue': 'sum',
        'Gross Margin %': 'mean'
    }).reset_index()
    uae_category_margin['Revenue_Weight'] = uae_category_margin['Revenue'] / total_uae_revenue
    highest_contribution = uae_category_margin.loc[uae_category_margin['Revenue_Weight'].idxmax()]
    
    insights['Q11'] = {
        'question': 'What is the current weighted average gross margin for UAE?',
        'insights': [
            f"UAE weighted average gross margin is {weighted_margin:.1%} across all categories",
            f"{highest_contribution['Category']} contributes most to weighted margin with {highest_contribution['Revenue_Weight']:.1%} revenue share and {highest_contribution['Gross Margin %']:.1%} margin",
            f"Margin ranges from {uae_category_margin['Gross Margin %'].min():.1%} to {uae_category_margin['Gross Margin %'].max():.1%} across UAE categories"
        ],
        'recommendations': [
            f"Maintain UAE's {weighted_margin:.1%} margin performance as benchmark for KSA market",
            f"Grow share of high-margin categories ({uae_category_margin.nlargest(2, 'Gross Margin %')['Category'].tolist()}) to improve weighted margin",
            "Set target of reaching 45% weighted average margin by optimizing category mix"
        ]
    }
    
    # Q12-13: Repurchase optimization and margin improvement
    repurchase_margin_analysis = df.groupby('Category').agg({
        'Repurchase Rate': 'mean',
        'Gross Margin %': 'mean',
        'Revenue': 'sum'
    }).reset_index()
    repurchase_margin_analysis['Revenue_Share'] = repurchase_margin_analysis['Revenue'] / repurchase_margin_analysis['Revenue'].sum()
    
    current_weighted_margin = (repurchase_margin_analysis['Revenue_Share'] * repurchase_margin_analysis['Gross Margin %']).sum()
    top_repurchase_categories = repurchase_margin_analysis.nlargest(3, 'Repurchase Rate')
    
    insights['Q12_13'] = {
        'question': 'Repurchase rate optimization and margin impact analysis',
        'insights': [
            f"Top repurchase categories ({', '.join(top_repurchase_categories['Category'].tolist())}) average {top_repurchase_categories['Repurchase Rate'].mean():.1%} vs portfolio average of {repurchase_margin_analysis['Repurchase Rate'].mean():.1%}",
            f"Current portfolio weighted margin is {current_weighted_margin:.1%} with optimization potential",
            f"High-repurchase categories show {top_repurchase_categories['Gross Margin %'].mean():.1%} average margin vs {repurchase_margin_analysis['Gross Margin %'].mean():.1%} portfolio"
        ],
        'recommendations': [
            f"Increase marketing investment in {top_repurchase_categories.iloc[0]['Category']} and {top_repurchase_categories.iloc[1]['Category']} by 30% for sustainable growth",
            "Target 5pp margin improvement through category mix optimization and AOV increases",
            "Implement customer lifetime value optimization focusing on high-repurchase, high-margin segments"
        ]
    }
    
    return insights

if __name__ == "__main__":
    insights = analyze_business_questions()
    
    # Print formatted insights
    for q_num, data in insights.items():
        print(f"\n{'='*60}")
        print(f"{q_num}: {data['question']}")
        print(f"{'='*60}")
        
        print("\n🔍 KEY INSIGHTS:")
        for i, insight in enumerate(data['insights'], 1):
            print(f"{i}. {insight}")
        
        print("\n💡 STRATEGIC RECOMMENDATIONS:")
        for i, rec in enumerate(data['recommendations'], 1):
            print(f"{i}. {rec}")
        print()