"""
Tests for UCI Mushroom extractor.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch, mock_open
from src.extract.uci_mushroom_extractor import UCIMushroomExtractor

class TestUCIMushroomExtractor:
    """Test UCI Mushroom extractor."""
    
    def test_initialization(self):
        """Test extractor initialization."""
        extractor = UCIMushroomExtractor()
        
        assert extractor.name == "uci_mushroom"
        assert "url" in extractor.config
        assert "output_file" in extractor.config
        assert len(extractor.column_names) == 23
    
    def test_validate_valid_data(self):
        """Test validation with valid data."""
        extractor = UCIMushroomExtractor()
        
        # Create valid test data
        valid_data = pd.DataFrame({
            'class': ['e', 'p'],
            'cap-shape': ['x', 'b'],
            'cap-surface': ['s', 's'],
            'cap-color': ['n', 'y']
        })
        
        result = extractor.validate(valid_data)
        assert result is True
    
    def test_validate_empty_data(self):
        """Test validation with empty data."""
        extractor = UCIMushroomExtractor()
        
        empty_data = pd.DataFrame()
        result = extractor.validate(empty_data)
        assert result is False
    
    def test_validate_missing_columns(self):
        """Test validation with missing required columns."""
        extractor = UCIMushroomExtractor()
        
        # Data missing required columns
        invalid_data = pd.DataFrame({
            'class': ['e', 'p'],
            'wrong_column': ['x', 'y']
        })
        
        result = extractor.validate(invalid_data)
        assert result is False
    
    @patch('src.extract.uci_mushroom_extractor.requests.get')
    @patch('src.extract.uci_mushroom_extractor.config')
    def test_extract_success(self, mock_config, mock_get):
        """Test successful data extraction."""
        # Mock configuration
        mock_config.raw_data_dir = "/tmp/test"
        mock_config.uci_mushroom_url = "http://test.com/data"
        
        # Mock HTTP response
        mock_response = Mock()
        mock_response.text = "e,x,s,n,t,p,f,c,n,k,e,e,s,s,w,w,p,w,o,p,k,s,u\np,x,s,y,t,a,f,c,b,k,e,c,s,s,w,w,p,w,o,p,n,n,g"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        extractor = UCIMushroomExtractor()
        
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('pandas.read_csv') as mock_read_csv:
                with patch('pathlib.Path.mkdir') as mock_mkdir:
                    with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
                        mock_read_csv.return_value = pd.DataFrame({
                            'class': ['e', 'p'],
                            'cap-shape': ['x', 'x']
                        })
                        
                        result = extractor.extract()
                        
                        assert isinstance(result, pd.DataFrame)
                        mock_get.assert_called_once()
    
    @patch('src.extract.uci_mushroom_extractor.requests.get')
    def test_extract_http_error(self, mock_get):
        """Test extraction with HTTP error."""
        mock_get.side_effect = Exception("HTTP Error")
        
        extractor = UCIMushroomExtractor()
        
        with pytest.raises(Exception):
            extractor.extract()
