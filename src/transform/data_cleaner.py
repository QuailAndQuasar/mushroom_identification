"""
Data cleaning transformer for handling missing values and inconsistencies.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from .base_transformer import BaseTransformer

class DataCleaner(BaseTransformer):
    """Transformer for cleaning and standardizing data."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize data cleaner.
        
        Args:
            config: Configuration dictionary
        """
        default_config = {
            "handle_missing": "drop",  # drop, fill, impute
            "missing_threshold": 0.5,  # Drop columns with >50% missing
            "outlier_method": "iqr",    # iqr, zscore, isolation_forest
            "outlier_threshold": 3.0,  # Z-score threshold
            "standardize_text": True,   # Standardize text columns
            "remove_duplicates": True,  # Remove duplicate rows
        }
        
        if config:
            default_config.update(config)
        
        super().__init__(
            name="data_cleaner",
            config=default_config
        )
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the input data.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        self.logger.info(f"Starting data cleaning for {len(data)} records")
        
        # Store original stats
        self.stats["original_shape"] = data.shape
        self.stats["original_missing"] = data.isnull().sum().sum()
        self.stats["original_duplicates"] = data.duplicated().sum()
        
        # Start with a copy
        cleaned_data = data.copy()
        
        # Remove duplicates
        if self.config["remove_duplicates"]:
            before_dup = len(cleaned_data)
            cleaned_data = cleaned_data.drop_duplicates()
            self.stats["duplicates_removed"] = before_dup - len(cleaned_data)
            self.logger.info(f"Removed {self.stats['duplicates_removed']} duplicate rows")
        
        # Handle missing values
        cleaned_data = self._handle_missing_values(cleaned_data)
        
        # Handle outliers
        cleaned_data = self._handle_outliers(cleaned_data)
        
        # Standardize text
        if self.config["standardize_text"]:
            cleaned_data = self._standardize_text(cleaned_data)
        
        # Update stats
        self.stats["final_shape"] = cleaned_data.shape
        self.stats["final_missing"] = cleaned_data.isnull().sum().sum()
        self.stats["records_removed"] = self.stats["original_shape"][0] - self.stats["final_shape"][0]
        
        self.logger.info(f"Data cleaning completed: {self.stats['records_removed']} records removed")
        return cleaned_data
    
    def _handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values based on configuration."""
        missing_cols = data.columns[data.isnull().any()].tolist()
        
        if not missing_cols:
            return data
        
        self.logger.info(f"Handling missing values in {len(missing_cols)} columns")
        
        if self.config["handle_missing"] == "drop":
            # Drop columns with high missing percentage
            threshold = self.config["missing_threshold"]
            cols_to_drop = []
            
            for col in missing_cols:
                missing_pct = data[col].isnull().sum() / len(data)
                if missing_pct > threshold:
                    cols_to_drop.append(col)
                    self.logger.warning(f"Dropping column {col} ({missing_pct:.1%} missing)")
            
            data = data.drop(columns=cols_to_drop)
            self.stats["columns_dropped"] = len(cols_to_drop)
            
            # Drop rows with any remaining missing values
            before_rows = len(data)
            data = data.dropna()
            self.stats["rows_dropped_missing"] = before_rows - len(data)
            
        elif self.config["handle_missing"] == "fill":
            # Fill missing values
            for col in missing_cols:
                if data[col].dtype in ['int64', 'float64']:
                    data[col] = data[col].fillna(data[col].median())
                else:
                    data[col] = data[col].fillna(data[col].mode().iloc[0] if not data[col].mode().empty else 'Unknown')
        
        return data
    
    def _handle_outliers(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle outliers based on configuration."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return data
        
        self.logger.info(f"Handling outliers in {len(numeric_cols)} numeric columns")
        
        if self.config["outlier_method"] == "iqr":
            data = self._remove_outliers_iqr(data, numeric_cols)
        elif self.config["outlier_method"] == "zscore":
            data = self._remove_outliers_zscore(data, numeric_cols)
        
        return data
    
    def _remove_outliers_iqr(self, data: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Remove outliers using IQR method."""
        outliers_removed = 0
        
        for col in cols:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            before = len(data)
            data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
            outliers_removed += before - len(data)
        
        self.stats["outliers_removed"] = outliers_removed
        return data
    
    def _remove_outliers_zscore(self, data: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        """Remove outliers using Z-score method."""
        outliers_removed = 0
        threshold = self.config["outlier_threshold"]
        
        for col in cols:
            z_scores = np.abs((data[col] - data[col].mean()) / data[col].std())
            before = len(data)
            data = data[z_scores < threshold]
            outliers_removed += before - len(data)
        
        self.stats["outliers_removed"] = outliers_removed
        return data
    
    def _standardize_text(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize text columns."""
        text_cols = data.select_dtypes(include=['object']).columns
        
        for col in text_cols:
            # Convert to lowercase and strip whitespace
            data[col] = data[col].astype(str).str.lower().str.strip()
            
            # Replace multiple spaces with single space
            data[col] = data[col].str.replace(r'\s+', ' ', regex=True)
        
        self.logger.info(f"Standardized {len(text_cols)} text columns")
        return data
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate cleaned data.
        
        Args:
            data: Cleaned DataFrame
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if data is empty
            if data.empty:
                self.logger.error("Cleaned data is empty")
                return False
            
            # Check for remaining missing values
            missing_count = data.isnull().sum().sum()
            if missing_count > 0:
                self.logger.warning(f"Found {missing_count} remaining missing values")
            
            # Check data types
            if len(data.columns) == 0:
                self.logger.error("No columns remaining after cleaning")
                return False
            
            self.logger.info("Data cleaning validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False