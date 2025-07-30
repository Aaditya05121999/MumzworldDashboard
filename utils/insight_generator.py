import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from utils.data_processor import DataProcessor

class InsightGenerator:
    def __init__(self, data):
        self.data = data
        self.processor = DataProcessor(data)
        
    def generate_all_insights(self):
        """Generate comprehensive insights from the data"""
        insights = {}
        
        # Key findings
        insights['key_findings'] = self.generate_key_findings()
        
        # Correlations
        insights['correlations'] = self.find_strong_correlations()
        
        # Outliers
        insights['outliers'] = self.detect_all_outliers()
        
        # Trends
        insights['trends'] = self.analyze_all_trends()
        
        # Data quality
        insights['data_quality'] = self.processor.get_data_quality_summary()
        
        # Distribution insights
        insights['distributions'] = self.analyze_distributions()
        
        return insights
    
    def generate_key_findings(self):
        """Generate key findings about the dataset"""
        findings = []
        
        # Dataset size insight
        findings.append(f"Dataset contains {len(self.data):,} records with {len(self.data.columns)} features")
        
        # Missing data insight
        missing_percent = (self.data.isnull().sum().sum() / (len(self.data) * len(self.data.columns))) * 100
        if missing_percent > 10:
            findings.append(f"High missing data: {missing_percent:.1f}% of values are missing")
        elif missing_percent > 0:
            findings.append(f"Low missing data: {missing_percent:.1f}% of values are missing")
        else:
            findings.append("Complete dataset: No missing values detected")
        
        # Data types insight
        numeric_cols = len(self.data.select_dtypes(include=[np.number]).columns)
        categorical_cols = len(self.data.select_dtypes(include=['object', 'category']).columns)
        findings.append(f"Data types: {numeric_cols} numeric, {categorical_cols} categorical columns")
        
        # Duplicates insight
        duplicates = self.data.duplicated().sum()
        if duplicates > 0:
            findings.append(f"Found {duplicates} duplicate records ({duplicates/len(self.data)*100:.1f}%)")
        
        # Unique values insight
        for col in self.data.columns:
            unique_ratio = self.data[col].nunique() / len(self.data)
            if unique_ratio > 0.95 and self.data[col].dtype == 'object':
                findings.append(f"{col} appears to be a unique identifier (95%+ unique values)")
            elif unique_ratio < 0.05 and len(self.data) > 100:
                findings.append(f"{col} has very low variability (less than 5% unique values)")
        
        return findings[:5]  # Return top 5 findings
    
    def find_strong_correlations(self, threshold=0.7):
        """Find strong correlations between numeric variables"""
        correlations = []
        corr_matrix = self.processor.get_correlation_matrix()
        
        if corr_matrix is None:
            return correlations
        
        # Find strong correlations
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_value,
                        'strength': 'Strong positive' if corr_value > 0 else 'Strong negative'
                    })
        
        # Sort by absolute correlation strength
        correlations.sort(key=lambda x: abs(x['correlation']), reverse=True)
        return correlations[:5]  # Return top 5
    
    def detect_all_outliers(self):
        """Detect outliers in all numeric columns"""
        outliers = []
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            outlier_indices = self.processor.detect_outliers(col)
            if len(outlier_indices) > 0:
                outliers.append({
                    'column': col,
                    'count': len(outlier_indices),
                    'percentage': (len(outlier_indices) / len(self.data)) * 100
                })
        
        return outliers
    
    def analyze_all_trends(self):
        """Analyze trends in all numeric columns"""
        trends = []
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            trend = self.processor.analyze_trends(col)
            if trend and abs(trend['slope']) > 0.001:  # Only significant trends
                trends.append(trend)
        
        return trends
    
    def analyze_distributions(self):
        """Analyze distribution characteristics of numeric columns"""
        distributions = []
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            col_data = self.data[col].dropna()
            if len(col_data) == 0:
                continue
                
            # Calculate distribution metrics
            skewness = col_data.skew()
            kurtosis = col_data.kurtosis()
            
            dist_info = {
                'column': col,
                'mean': col_data.mean(),
                'median': col_data.median(),
                'std': col_data.std(),
                'skewness': skewness,
                'kurtosis': kurtosis
            }
            
            # Interpret skewness
            if abs(skewness) < 0.5:
                dist_info['skew_interpretation'] = 'Approximately symmetric'
            elif skewness > 0.5:
                dist_info['skew_interpretation'] = 'Right-skewed (positive skew)'
            else:
                dist_info['skew_interpretation'] = 'Left-skewed (negative skew)'
            
            # Interpret kurtosis
            if abs(kurtosis) < 0.5:
                dist_info['kurtosis_interpretation'] = 'Normal tail heaviness'
            elif kurtosis > 0.5:
                dist_info['kurtosis_interpretation'] = 'Heavy-tailed'
            else:
                dist_info['kurtosis_interpretation'] = 'Light-tailed'
            
            distributions.append(dist_info)
        
        return distributions
    
    def find_categorical_patterns(self):
        """Find patterns in categorical variables"""
        patterns = []
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        
        for col in categorical_cols:
            value_counts = self.data[col].value_counts()
            
            pattern_info = {
                'column': col,
                'unique_count': len(value_counts),
                'most_common': value_counts.index[0],
                'most_common_count': value_counts.iloc[0],
                'most_common_percentage': (value_counts.iloc[0] / len(self.data)) * 100
            }
            
            # Check for dominance
            if pattern_info['most_common_percentage'] > 80:
                pattern_info['pattern'] = f"Heavily dominated by '{pattern_info['most_common']}'"
            elif pattern_info['most_common_percentage'] > 50:
                pattern_info['pattern'] = f"Moderately dominated by '{pattern_info['most_common']}'"
            else:
                pattern_info['pattern'] = "Well distributed across categories"
            
            patterns.append(pattern_info)
        
        return patterns
    
    def suggest_analysis_steps(self):
        """Suggest next analysis steps based on data characteristics"""
        suggestions = []
        
        # Check for time series data
        for col in self.data.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                suggestions.append("Consider time series analysis for temporal patterns")
                break
        
        # Check for clustering potential
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) >= 2:
            suggestions.append("Dataset suitable for clustering analysis")
        
        # Check for classification potential
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            suggestions.append("Consider classification modeling with categorical targets")
        
        # Check for regression potential
        if len(numeric_cols) >= 2:
            suggestions.append("Multiple numeric variables suitable for regression analysis")
        
        return suggestions
