import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DataProcessor:
    def __init__(self, data):
        self.data = data
        
    def get_column_info(self):
        """Get comprehensive column information"""
        info = []
        for col in self.data.columns:
            col_data = self.data[col]
            info.append({
                'Column': col,
                'Type': str(col_data.dtype),
                'Non-Null Count': col_data.count(),
                'Null Count': col_data.isnull().sum(),
                'Null %': f"{(col_data.isnull().sum() / len(col_data) * 100):.1f}%",
                'Unique Values': col_data.nunique(),
                'Sample Values': ', '.join(str(x) for x in col_data.dropna().unique()[:3])
            })
        return pd.DataFrame(info)
    
    def create_missing_values_chart(self):
        """Create a heatmap of missing values"""
        missing_data = self.data.isnull()
        
        # Calculate missing percentages
        missing_percent = (missing_data.sum() / len(self.data) * 100).sort_values(ascending=False)
        missing_percent = missing_percent[missing_percent > 0]
        
        if len(missing_percent) == 0:
            return None
            
        fig = px.bar(
            x=missing_percent.index,
            y=missing_percent.values,
            title="Missing Values by Column",
            labels={'x': 'Columns', 'y': 'Missing %'}
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_tickangle=-45
        )
        
        return fig
    
    def detect_outliers(self, column, method='iqr'):
        """Detect outliers in a numeric column"""
        if not pd.api.types.is_numeric_dtype(self.data[column]):
            return []
            
        col_data = self.data[column].dropna()
        
        if method == 'iqr':
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
        else:  # z-score method
            z_scores = np.abs((col_data - col_data.mean()) / col_data.std())
            outliers = col_data[z_scores > 3]
            
        return outliers.index.tolist()
    
    def get_correlation_matrix(self):
        """Calculate correlation matrix for numeric columns"""
        numeric_cols = self.data.select_dtypes(include=[np.number])
        if len(numeric_cols.columns) < 2:
            return None
        return numeric_cols.corr()
    
    def get_data_quality_summary(self):
        """Get comprehensive data quality summary"""
        total_cells = len(self.data) * len(self.data.columns)
        missing_cells = self.data.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        
        duplicates = self.data.duplicated().sum()
        
        recommendations = []
        if completeness < 95:
            recommendations.append("Consider handling missing values")
        if duplicates > 0:
            recommendations.append(f"Remove {duplicates} duplicate rows")
            
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            outliers = self.detect_outliers(col)
            if len(outliers) > len(self.data) * 0.05:  # More than 5% outliers
                recommendations.append(f"Investigate outliers in {col}")
        
        return {
            'completeness': completeness,
            'duplicates': duplicates,
            'recommendations': recommendations
        }
    
    def analyze_trends(self, column):
        """Analyze trends in a numeric column"""
        if not pd.api.types.is_numeric_dtype(self.data[column]):
            return None
            
        col_data = self.data[column].dropna()
        
        # Basic trend analysis
        if len(col_data) < 3:
            return None
            
        # Calculate trend using linear regression
        x = np.arange(len(col_data))
        coeffs = np.polyfit(x, col_data, 1)
        slope = coeffs[0]
        
        if slope > 0:
            trend_desc = f"Increasing trend (slope: {slope:.3f})"
        elif slope < 0:
            trend_desc = f"Decreasing trend (slope: {slope:.3f})"
        else:
            trend_desc = "No clear trend"
            
        return {
            'column': column,
            'slope': slope,
            'description': trend_desc
        }
