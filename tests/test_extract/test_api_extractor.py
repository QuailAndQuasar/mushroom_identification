"""
Tests for API extractor.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.extract.api_extractor import APIExtractor

class TestAPIExtractor:
    """Test API extractor."""
    
    def test_initialization(self):
        """Test extractor initialization."""
        extractor = APIExtractor(
            name="test_api",
            base_url="https://api.test.com",
            endpoint="/data"
        )
        
        assert extractor.name == "test_api"
        assert extractor.config["base_url"] == "https://api.test.com"
        assert extractor.config["endpoint"] == "/data"
    
    def test_validate_valid_data(self):
        """Test validation with valid data."""
        extractor = APIExtractor("test_api", "https://api.test.com", "/data")
        
        valid_data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['a', 'b', 'c']
        })
        
        result = extractor.validate(valid_data)
        assert result is True
    
    def test_validate_empty_data(self):
        """Test validation with empty data."""
        extractor = APIExtractor("test_api", "https://api.test.com", "/data")
        
        empty_data = pd.DataFrame()
        result = extractor.validate(empty_data)
        assert result is False
    
    @patch('src.extract.api_extractor.requests.get')
    @patch('src.extract.api_extractor.config')
    def test_extract_success(self, mock_config, mock_get):
        """Test successful API extraction."""
        # Mock configuration
        mock_config.raw_data_dir = "/tmp/test"
        
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = [{'id': 1, 'name': 'test'}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        extractor = APIExtractor("test_api", "https://api.test.com", "/data")
        
        with patch('builtins.open', mock_open()) as mock_file:
            result = extractor.extract()
            
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
            mock_get.assert_called_once()
    
    @patch('src.extract.api_extractor.requests.get')
    def test_extract_api_error(self, mock_get):
        """Test extraction with API error."""
        mock_get.side_effect = Exception("API Error")
        
        extractor = APIExtractor("test_api", "https://api.test.com", "/data")
        
        with pytest.raises(Exception):
            extractor.extract()
