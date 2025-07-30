import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

class ChartGenerator:
    def __init__(self, data):
        self.data = data
        
    def create_distribution_chart(self, column):
        """Create distribution chart for a numeric column"""
        if not pd.api.types.is_numeric_dtype(self.data[column]):
            # For categorical data, create bar chart
            value_counts = self.data[column].value_counts().head(20)
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f"Distribution of {column}",
                labels={'x': column, 'y': 'Count'}
            )
        else:
            # For numeric data, create histogram with box plot
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=[f'Histogram of {column}', f'Box Plot of {column}'],
                vertical_spacing=0.15,
                row_heights=[0.7, 0.3]
            )
            
            # Histogram
            fig.add_trace(
                go.Histogram(x=self.data[column], name='Distribution', nbinsx=30),
                row=1, col=1
            )
            
            # Box plot
            fig.add_trace(
                go.Box(x=self.data[column], name='Box Plot', orientation='h'),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f"Distribution Analysis: {column}",
                showlegend=False,
                height=600
            )
        
        # Mobile optimization
        fig.update_layout(
            font=dict(size=12),
            margin=dict(l=20, r=20, t=60, b=20),
            dragmode='pan'
        )
        
        return fig
    
    def create_correlation_matrix(self):
        """Create correlation heatmap for numeric columns"""
        numeric_data = self.data.select_dtypes(include=[np.number])
        
        if len(numeric_data.columns) < 2:
            return None
            
        corr_matrix = numeric_data.corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )
        
        fig.update_layout(
            height=max(400, len(corr_matrix) * 30),
            font=dict(size=10),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_time_series_chart(self, date_column, value_column):
        """Create time series chart"""
        try:
            # Try to convert to datetime
            if not pd.api.types.is_datetime64_any_dtype(self.data[date_column]):
                date_data = pd.to_datetime(self.data[date_column], errors='coerce')
            else:
                date_data = self.data[date_column]
            
            # Remove rows with invalid dates
            valid_dates = ~date_data.isna()
            plot_data = self.data[valid_dates].copy()
            plot_data[date_column] = date_data[valid_dates]
            plot_data = plot_data.sort_values(date_column)
            
            fig = px.line(
                plot_data,
                x=date_column,
                y=value_column,
                title=f"{value_column} Over Time",
                markers=True
            )
            
            # Add trend line
            x_numeric = np.arange(len(plot_data))
            coeffs = np.polyfit(x_numeric, plot_data[value_column], 1)
            trend_line = coeffs[0] * x_numeric + coeffs[1]
            
            fig.add_trace(
                go.Scatter(
                    x=plot_data[date_column],
                    y=trend_line,
                    mode='lines',
                    name='Trend',
                    line=dict(dash='dash', color='red')
                )
            )
            
            fig.update_layout(
                height=400,
                font=dict(size=12),
                margin=dict(l=20, r=20, t=60, b=20),
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            return None
    
    def create_comparison_chart(self, category_column, value_column):
        """Create comparison chart (box plot or bar chart)"""
        # Limit categories for mobile display
        top_categories = self.data[category_column].value_counts().head(10).index
        filtered_data = self.data[self.data[category_column].isin(top_categories)]
        
        if pd.api.types.is_numeric_dtype(self.data[value_column]):
            # Box plot for numeric data
            fig = px.box(
                filtered_data,
                x=category_column,
                y=value_column,
                title=f"{value_column} by {category_column}"
            )
        else:
            # Grouped bar chart for categorical data
            cross_tab = pd.crosstab(filtered_data[category_column], filtered_data[value_column])
            fig = px.bar(
                cross_tab,
                title=f"{value_column} Distribution by {category_column}"
            )
        
        fig.update_layout(
            height=400,
            font=dict(size=12),
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis_tickangle=-45
        )
        
        return fig
    
    def create_scatter_chart(self, x_column, y_column, color_column=None):
        """Create scatter plot"""
        fig = px.scatter(
            self.data,
            x=x_column,
            y=y_column,
            color=color_column,
            title=f"{y_column} vs {x_column}",
            trendline="ols" if pd.api.types.is_numeric_dtype(self.data[x_column]) and pd.api.types.is_numeric_dtype(self.data[y_column]) else None
        )
        
        fig.update_layout(
            height=400,
            font=dict(size=12),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_custom_chart(self, x_column, y_column, chart_type='scatter'):
        """Create custom chart based on user selection"""
        if chart_type == 'scatter':
            return self.create_scatter_chart(x_column, y_column)
        
        elif chart_type == 'line':
            fig = px.line(
                self.data,
                x=x_column,
                y=y_column,
                title=f"{y_column} vs {x_column}",
                markers=True
            )
        
        elif chart_type == 'bar':
            # Aggregate data if needed
            if pd.api.types.is_numeric_dtype(self.data[y_column]):
                agg_data = self.data.groupby(x_column)[y_column].mean().reset_index()
                fig = px.bar(
                    agg_data,
                    x=x_column,
                    y=y_column,
                    title=f"Average {y_column} by {x_column}"
                )
            else:
                # Count frequency
                count_data = self.data[x_column].value_counts().reset_index()
                count_data.columns = [x_column, 'count']
                fig = px.bar(
                    count_data,
                    x=x_column,
                    y='count',
                    title=f"Count by {x_column}"
                )
        
        else:
            # Default to scatter
            return self.create_scatter_chart(x_column, y_column)
        
        fig.update_layout(
            height=400,
            font=dict(size=12),
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis_tickangle=-45 if chart_type == 'bar' else 0
        )
        
        return fig
    
    def create_summary_dashboard(self):
        """Create a summary dashboard with key charts"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        
        if len(numeric_cols) == 0:
            return None
        
        # Create subplots
        rows = min(3, len(numeric_cols))
        fig = make_subplots(
            rows=rows, cols=2,
            subplot_titles=[f'Distribution: {col}' for col in numeric_cols[:rows*2]],
            vertical_spacing=0.1
        )
        
        # Add histograms for numeric columns
        for i, col in enumerate(numeric_cols[:rows*2]):
            row = (i // 2) + 1
            col_pos = (i % 2) + 1
            
            fig.add_trace(
                go.Histogram(x=self.data[col], name=col, nbinsx=20),
                row=row, col=col_pos
            )
        
        fig.update_layout(
            height=200 * rows,
            title="Data Overview Dashboard",
            showlegend=False,
            font=dict(size=10),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
