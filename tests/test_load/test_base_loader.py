"""
Tests for base loader functionality.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.load.base_loader import BaseLoader

class TestBaseLoader:
    """Test base loader abstract class."""
    
    def test_initialization(self):
        """Test loader initialization."""
        # Create a concrete implementation for testing
        class TestLoader(BaseLoader):
            def load(self, data, destination):
                return True
            
            def validate(self, data):
                return True
        
        loader = TestLoader("test_loader", {"key": "value"})
        
        assert loader.name == "test_loader"
        assert loader.config == {"key": "value"}
        assert loader.logger.name.endswith("test_loader")
        assert loader.stats == {}
    
    def test_get_stats(self):
        """Test getting loading statistics."""
        class TestLoader(BaseLoader):
            def load(self, data, destination):
                return True
            
            def validate(self, data):
                return True
        
        loader = TestLoader("test_loader")
        loader.stats = {"test": "value", "count": 100}
        
        stats = loader.get_stats()
        assert stats == {"test": "value", "count": 100}
    
    def test_save_stats(self, tmp_path):
        """Test saving loading statistics."""
        class TestLoader(BaseLoader):
            def load(self, data, destination):
                return True
            
            def validate(self, data):
                return True
        
        loader = TestLoader("test_loader")
        loader.stats = {"test": "value", "count": 100}
        
        with patch('src.load.base_loader.config') as mock_config:
            mock_config.processed_data_dir = tmp_path
            loader.save_stats()
            
            # Check if stats file was created
            stats_file = tmp_path / "test_loader_loading_stats.json"
            assert stats_file.exists()
    
    def test_log_loading_success(self):
        """Test successful loading logging."""
        class TestLoader(BaseLoader):
            def load(self, data, destination):
                return True
            
            def validate(self, data):
                return True
        
        loader = TestLoader("test_loader")
        
        with patch.object(loader.logger, 'info') as mock_info:
            loader.log_loading(success=True, records_count=100, destination="test_db")
            mock_info.assert_called_with("Loading successful: 100 records to test_db")
    
    def test_log_loading_failure(self):
        """Test failed loading logging."""
        class TestLoader(BaseLoader):
            def load(self, data, destination):
                return True
            
            def validate(self, data):
                return True
        
        loader = TestLoader("test_loader")
        
        with patch.object(loader.logger, 'error') as mock_error:
            loader.log_loading(success=False, records_count=0, destination="test_db", error="Test error")
            mock_error.assert_called_with("Loading failed to test_db: Test error")
