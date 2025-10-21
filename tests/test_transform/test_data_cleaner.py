"""
Tests for data cleaner transformer.
"""
import pytest
import pandas as pd
import numpy as np
from src.transform.data_cleaner import DataCleaner

class TestDataCleaner:
    """Test data cleaner transformer."""
    
    def test_initialization(self):
        """Test cleaner initialization."""
        cleaner = DataCleaner()
        
        assert cleaner.name == "data_cleaner"
        assert cleaner.config["handle_missing"] == "drop"
        assert cleaner.config["missing_threshold"] == 0.5
        assert cleaner.config["outlier_method"] == "iqr"
        assert cleaner.config["standardize_text"] is True
    
    def test_initialization_with_config(self):
        """Test cleaner initialization with custom config."""
        config = {
            "handle_missing": "fill",
            "missing_threshold": 0.3,
            "outlier_method": "zscore"
        }
        cleaner = DataCleaner(config)
        
        assert cleaner.config["handle_missing"] == "fill"
        assert cleaner.config["missing_threshold"] == 0.3
        assert cleaner.config["outlier_method"] == "zscore"
    
    def test_transform_clean_data(self):
        """Test transformation with clean data."""
        cleaner = DataCleaner()
        
        # Create clean test data
        clean_data = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5],
            'col2': ['a', 'b', 'c', 'd', 'e'],
            'col3': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        result = cleaner.transform(clean_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 5
        assert len(result.columns) == 3
    
    def test_transform_with_duplicates(self):
        """Test transformation with duplicate rows."""
        cleaner = DataCleaner({"remove_duplicates": True})
        
        # Create data with duplicates
        data_with_duplicates = pd.DataFrame({
            'col1': [1, 2, 1, 3, 2],
            'col2': ['a', 'b', 'a', 'c', 'b']
        })
        
        result = cleaner.transform(data_with_duplicates)
        
        assert len(result) == 3  # Duplicates removed
        assert cleaner.stats["duplicates_removed"] == 2
    
    def test_transform_with_missing_values_drop(self):
        """Test transformation with missing values using drop strategy."""
        cleaner = DataCleaner({"handle_missing": "drop"})
        
        # Create data with missing values
        data_with_missing = pd.DataFrame({
            'col1': [1, 2, None, 4, 5],
            'col2': ['a', 'b', 'c', None, 'e'],
            'col3': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        result = cleaner.transform(data_with_missing)
        
        # Should drop rows with missing values
        assert len(result) == 3  # Rows with missing values dropped
        assert result.isnull().sum().sum() == 0
    
    def test_transform_with_missing_values_fill(self):
        """Test transformation with missing values using fill strategy."""
        cleaner = DataCleaner({"handle_missing": "fill"})
        
        # Create data with missing values
        data_with_missing = pd.DataFrame({
            'col1': [1, 2, None, 4, 5],
            'col2': ['a', 'b', 'c', None, 'e'],
            'col3': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        
        result = cleaner.transform(data_with_missing)
        
        # Should fill missing values
        assert len(result) == 5  # No rows dropped
        assert result.isnull().sum().sum() == 0
    
    def test_transform_with_outliers_iqr(self):
        """Test transformation with outliers using IQR method."""
        cleaner = DataCleaner({"outlier_method": "iqr"})
        
        # Create data with outliers
        data_with_outliers = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5, 100],  # 100 is an outlier
            'col2': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6]
        })
        
        result = cleaner.transform(data_with_outliers)
        
        # Should remove outliers
        assert len(result) < 6
        assert cleaner.stats["outliers_removed"] > 0
    
    def test_transform_with_outliers_zscore(self):
        """Test transformation with outliers using Z-score method."""
        cleaner = DataCleaner({"outlier_method": "zscore", "outlier_threshold": 2.0})
        
        # Create data with outliers
        data_with_outliers = pd.DataFrame({
            'col1': [1, 2, 3, 4, 5, 100],  # 100 is an outlier
            'col2': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6]
        })
        
        result = cleaner.transform(data_with_outliers)
        
        # Should remove outliers
        assert len(result) < 6
        assert cleaner.stats["outliers_removed"] > 0
    
    def test_transform_standardize_text(self):
        """Test text standardization."""
        cleaner = DataCleaner({"standardize_text": True})
        
        # Create data with inconsistent text
        data_with_text = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['  A  ', 'B', '  C  '],
            'col3': ['Hello World', 'HELLO WORLD', 'hello world']
        })
        
        result = cleaner.transform(data_with_text)
        
        # Check text standardization
        assert result['col2'].iloc[0] == 'a'
        assert result['col2'].iloc[1] == 'b'
        assert result['col2'].iloc[2] == 'c'
        assert result['col3'].iloc[0] == 'hello world'
    
    def test_validate_clean_data(self):
        """Test validation with clean data."""
        cleaner = DataCleaner()
        
        clean_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        result = cleaner.validate(clean_data)
        assert result is True
    
    def test_validate_empty_data(self):
        """Test validation with empty data."""
        cleaner = DataCleaner()
        
        empty_data = pd.DataFrame()
        result = cleaner.validate(empty_data)
        assert result is False
    
    def test_validate_data_with_missing(self):
        """Test validation with missing values."""
        cleaner = DataCleaner()
        
        data_with_missing = pd.DataFrame({
            'col1': [1, 2, None],
            'col2': ['a', 'b', 'c']
        })
        
        result = cleaner.validate(data_with_missing)
        assert result is True  # Should pass but with warning
    
    def test_get_stats(self):
        """Test getting transformation statistics."""
        cleaner = DataCleaner()
        
        # Transform some data to generate stats
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        cleaner.transform(test_data)
        stats = cleaner.get_stats()
        
        assert "original_shape" in stats
        assert "final_shape" in stats
        assert "records_removed" in stats
