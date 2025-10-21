"""
Tests for feature engineer transformer.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
from src.transform.feature_engineer import FeatureEngineer

class TestFeatureEngineer:
    """Test feature engineer transformer."""
    
    def test_initialization(self):
        """Test engineer initialization."""
        engineer = FeatureEngineer()
        
        assert engineer.name == "feature_engineer"
        assert engineer.config["target_column"] == "class"
        assert engineer.config["categorical_encoding"] == "onehot"
        assert engineer.config["feature_scaling"] is True
        assert engineer.config["feature_selection"] is True
    
    def test_initialization_with_config(self):
        """Test engineer initialization with custom config."""
        config = {
            "target_column": "target",
            "categorical_encoding": "label",
            "feature_scaling": False,
            "n_features": 10
        }
        engineer = FeatureEngineer(config)
        
        assert engineer.config["target_column"] == "target"
        assert engineer.config["categorical_encoding"] == "label"
        assert engineer.config["feature_scaling"] is False
        assert engineer.config["n_features"] == 10
    
    def test_transform_with_categorical_data(self):
        """Test transformation with categorical data."""
        engineer = FeatureEngineer({"categorical_encoding": "onehot"})
        
        # Create data with categorical variables
        data = pd.DataFrame({
            'class': ['e', 'p', 'e', 'p'],
            'cap_shape': ['x', 'b', 'x', 'c'],
            'cap_surface': ['s', 's', 'f', 's'],
            'numeric_col': [1, 2, 3, 4]
        })
        
        result = engineer.transform(data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 4
        # Should have more columns due to one-hot encoding
        assert len(result.columns) > 4
    
    def test_transform_with_label_encoding(self):
        """Test transformation with label encoding."""
        engineer = FeatureEngineer({"categorical_encoding": "label"})
        
        # Create data with categorical variables
        data = pd.DataFrame({
            'class': ['e', 'p', 'e', 'p'],
            'cap_shape': ['x', 'b', 'x', 'c'],
            'numeric_col': [1, 2, 3, 4]
        })
        
        result = engineer.transform(data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 4
        # Should have same number of columns
        assert len(result.columns) == 3
    
    def test_transform_with_feature_scaling(self):
        """Test transformation with feature scaling."""
        engineer = FeatureEngineer({"feature_scaling": True})
        
        # Create data with numeric variables
        data = pd.DataFrame({
            'class': ['e', 'p', 'e', 'p'],
            'numeric1': [1, 10, 2, 20],
            'numeric2': [0.1, 1.0, 0.2, 2.0]
        })
        
        result = engineer.transform(data)
        
        assert isinstance(result, pd.DataFrame)
        # Check that scaling was applied (values should be standardized)
        numeric_cols = result.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # Scaled values should have mean close to 0 and std close to 1
            for col in numeric_cols:
                if col != 'class':  # Skip target if it's numeric
                    mean_val = result[col].mean()
                    std_val = result[col].std()
                    assert abs(mean_val) < 0.1  # Mean should be close to 0
                    assert abs(std_val - 1.0) < 0.1  # Std should be close to 1
    
    def test_transform_with_feature_selection(self):
        """Test transformation with feature selection."""
        engineer = FeatureEngineer({
            "feature_selection": True,
            "n_features": 2
        })
        
        # Create data with multiple features
        data = pd.DataFrame({
            'class': ['e', 'p', 'e', 'p', 'e', 'p'],
            'feature1': [1, 2, 1, 2, 1, 2],
            'feature2': [10, 20, 10, 20, 10, 20],
            'feature3': [100, 200, 100, 200, 100, 200],
            'feature4': [1000, 2000, 1000, 2000, 1000, 2000]
        })
        
        result = engineer.transform(data)
        
        assert isinstance(result, pd.DataFrame)
        # Should have target + selected features
        assert len(result.columns) <= 3  # target + 2 selected features
    
    def test_transform_with_interactions(self):
        """Test transformation with feature interactions."""
        engineer = FeatureEngineer({
            "create_interactions": True,
            "feature_selection": False
        })
        
        # Create data with numeric variables
        data = pd.DataFrame({
            'class': ['e', 'p', 'e', 'p'],
            'feature1': [1, 2, 3, 4],
            'feature2': [10, 20, 30, 40]
        })
        
        result = engineer.transform(data)
        
        assert isinstance(result, pd.DataFrame)
        # Should have more columns due to interactions
        assert len(result.columns) > 3
        assert engineer.stats["interactions_created"] > 0
    
    def test_transform_without_target(self):
        """Test transformation without target column."""
        engineer = FeatureEngineer({"target_column": "nonexistent"})
        
        # Create data without target
        data = pd.DataFrame({
            'feature1': [1, 2, 3, 4],
            'feature2': ['a', 'b', 'c', 'd']
        })
        
        result = engineer.transform(data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 4
    
    def test_validate_engineered_data(self):
        """Test validation with engineered data."""
        engineer = FeatureEngineer()
        
        # Create simple data
        data = pd.DataFrame({
            'class': ['e', 'p'],
            'feature1': [1, 2],
            'feature2': ['a', 'b']
        })
        
        result = engineer.transform(data)
        validation_result = engineer.validate(result)
        
        assert validation_result is True
    
    def test_validate_empty_data(self):
        """Test validation with empty data."""
        engineer = FeatureEngineer()
        
        empty_data = pd.DataFrame()
        result = engineer.validate(empty_data)
        assert result is False
    
    def test_validate_data_with_inf(self):
        """Test validation with infinite values."""
        engineer = FeatureEngineer()
        
        # Create data with infinite values
        data_with_inf = pd.DataFrame({
            'class': ['e', 'p'],
            'feature1': [1, np.inf],
            'feature2': [2, 3]
        })
        
        result = engineer.validate(data_with_inf)
        assert result is True  # Should pass but with warning
    
    def test_get_feature_importance(self):
        """Test getting feature importance."""
        engineer = FeatureEngineer({
            "feature_selection": True,
            "n_features": 2
        })
        
        # Create data for feature selection
        data = pd.DataFrame({
            'class': ['e', 'p', 'e', 'p', 'e', 'p'],
            'feature1': [1, 2, 1, 2, 1, 2],
            'feature2': [10, 20, 10, 20, 10, 20],
            'feature3': [100, 200, 100, 200, 100, 200]
        })
        
        engineer.transform(data)
        importance = engineer.get_feature_importance()
        
        # Should have feature importance scores
        assert isinstance(importance, dict)
    
    def test_get_engineered_features(self):
        """Test getting engineered feature names."""
        engineer = FeatureEngineer()
        
        # Create data
        data = pd.DataFrame({
            'class': ['e', 'p'],
            'feature1': [1, 2],
            'feature2': ['a', 'b']
        })
        
        engineer.transform(data)
        features = engineer.get_engineered_features()
        
        assert isinstance(features, list)
        assert len(features) > 0
    
    def test_transform_with_mixed_data_types(self):
        """Test transformation with mixed data types."""
        engineer = FeatureEngineer()
        
        # Create data with mixed types
        data = pd.DataFrame({
            'class': ['e', 'p', 'e', 'p'],
            'categorical': ['a', 'b', 'a', 'b'],
            'numeric': [1, 2, 3, 4],
            'float': [1.1, 2.2, 3.3, 4.4]
        })
        
        result = engineer.transform(data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 4
        assert len(result.columns) > 4  # Should have more columns due to encoding
