"""
Tests for base transformer functionality.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.transform.base_transformer import BaseTransformer

class TestBaseTransformer:
    """Test base transformer abstract class."""
    
    def test_initialization(self):
        """Test transformer initialization."""
        # Create a concrete implementation for testing
        class TestTransformer(BaseTransformer):
            def transform(self, data):
                return data
            
            def validate(self, data):
                return True
        
        transformer = TestTransformer("test_transformer", {"key": "value"})
        
        assert transformer.name == "test_transformer"
        assert transformer.config == {"key": "value"}
        assert transformer.logger.name.endswith("test_transformer")
        assert transformer.stats == {}
    
    def test_get_stats(self):
        """Test getting transformation statistics."""
        class TestTransformer(BaseTransformer):
            def transform(self, data):
                return data
            
            def validate(self, data):
                return True
        
        transformer = TestTransformer("test_transformer")
        transformer.stats = {"test": "value", "count": 100}
        
        stats = transformer.get_stats()
        assert stats == {"test": "value", "count": 100}
    
    def test_save_stats(self, tmp_path):
        """Test saving transformation statistics."""
        class TestTransformer(BaseTransformer):
            def transform(self, data):
                return data
            
            def validate(self, data):
                return True
        
        transformer = TestTransformer("test_transformer")
        transformer.stats = {"test": "value", "count": 100}
        
        with patch('src.transform.base_transformer.config') as mock_config:
            mock_config.processed_data_dir = tmp_path
            transformer.save_stats()
            
            # Check if stats file was created
            stats_file = tmp_path / "test_transformer_stats.json"
            assert stats_file.exists()
    
    def test_log_transformation_success(self):
        """Test successful transformation logging."""
        class TestTransformer(BaseTransformer):
            def transform(self, data):
                return data
            
            def validate(self, data):
                return True
        
        transformer = TestTransformer("test_transformer")
        
        with patch.object(transformer.logger, 'info') as mock_info:
            transformer.log_transformation(
                success=True, 
                input_shape=(100, 5), 
                output_shape=(100, 5)
            )
            mock_info.assert_called_with("Transformation successful: (100, 5) -> (100, 5)")
    
    def test_log_transformation_failure(self):
        """Test failed transformation logging."""
        class TestTransformer(BaseTransformer):
            def transform(self, data):
                return data
            
            def validate(self, data):
                return True
        
        transformer = TestTransformer("test_transformer")
        
        with patch.object(transformer.logger, 'error') as mock_error:
            transformer.log_transformation(
                success=False, 
                input_shape=(100, 5), 
                output_shape=(0, 0),
                error="Test error"
            )
            mock_error.assert_called_with("Transformation failed: Test error")
