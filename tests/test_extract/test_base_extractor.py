"""
Tests for base extractor functionality.
"""
import pytest
from unittest.mock import Mock, patch
from src.extract.base_extractor import BaseExtractor

class TestBaseExtractor:
    """Test base extractor abstract class."""
    
    def test_initialization(self):
        """Test extractor initialization."""
        # Create a concrete implementation for testing
        class TestExtractor(BaseExtractor):
            def extract(self):
                return "test_data"
            
            def validate(self, data):
                return True
        
        extractor = TestExtractor("test_extractor", {"key": "value"})
        
        assert extractor.name == "test_extractor"
        assert extractor.config == {"key": "value"}
        assert extractor.logger.name.endswith("test_extractor")
    
    def test_save_metadata(self, tmp_path):
        """Test metadata saving functionality."""
        class TestExtractor(BaseExtractor):
            def extract(self):
                return "test_data"
            
            def validate(self, data):
                return True
        
        extractor = TestExtractor("test_extractor")
        metadata = {"test": "value", "count": 100}
        
        with patch('src.extract.base_extractor.config') as mock_config:
            mock_config.raw_data_dir = tmp_path
            extractor.save_metadata(metadata)
            
            # Check if metadata file was created
            metadata_file = tmp_path / "test_extractor_metadata.json"
            assert metadata_file.exists()
    
    def test_log_extraction_success(self):
        """Test successful extraction logging."""
        class TestExtractor(BaseExtractor):
            def extract(self):
                return "test_data"
            
            def validate(self, data):
                return True
        
        extractor = TestExtractor("test_extractor")
        
        with patch.object(extractor.logger, 'info') as mock_info:
            extractor.log_extraction(success=True, records_count=100)
            mock_info.assert_called_with("Extraction successful: 100 records")
    
    def test_log_extraction_failure(self):
        """Test failed extraction logging."""
        class TestExtractor(BaseExtractor):
            def extract(self):
                return "test_data"
            
            def validate(self, data):
                return True
        
        extractor = TestExtractor("test_extractor")
        
        with patch.object(extractor.logger, 'error') as mock_error:
            extractor.log_extraction(success=False, error="Test error")
            mock_error.assert_called_with("Extraction failed: Test error")
