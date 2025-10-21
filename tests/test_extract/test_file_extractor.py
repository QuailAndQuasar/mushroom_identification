"""
Tests for file extractor.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from src.extract.file_extractor import FileExtractor

class TestFileExtractor:
    """Test file extractor."""
    
    def test_initialization(self):
        """Test extractor initialization."""
        extractor = FileExtractor("test.csv", "csv")
        
        assert extractor.name == "file_test"
        assert extractor.config["file_path"] == "test.csv"
        assert extractor.config["file_type"] == "csv"
    
    def test_validate_valid_data(self):
        """Test validation with valid data."""
        extractor = FileExtractor("test.csv", "csv")
        
        valid_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        result = extractor.validate(valid_data)
        assert result is True
    
    def test_validate_empty_data(self):
        """Test validation with empty data."""
        extractor = FileExtractor("test.csv", "csv")
        
        empty_data = pd.DataFrame()
        result = extractor.validate(empty_data)
        assert result is False
    
    def test_validate_high_missing_values(self):
        """Test validation with high missing values."""
        extractor = FileExtractor("test.csv", "csv")
        
        # Create data with high missing values
        data_with_missing = pd.DataFrame({
            'col1': [1, None, None, None, None],
            'col2': ['a', None, None, None, None]
        })
        
        result = extractor.validate(data_with_missing)
        assert result is True  # Should pass but with warning
    
    @patch('pandas.read_csv')
    @patch('pathlib.Path.exists')
    def test_extract_csv_success(self, mock_exists, mock_read_csv):
        """Test successful CSV extraction."""
        mock_exists.return_value = True
        mock_read_csv.return_value = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        
        extractor = FileExtractor("test.csv", "csv")
        
        with patch('src.extract.file_extractor.config') as mock_config:
            mock_config.raw_data_dir = "/tmp/test"
            
            result = extractor.extract()
            
            assert isinstance(result, pd.DataFrame)
            mock_read_csv.assert_called_once()
    
    @patch('pathlib.Path.exists')
    def test_extract_file_not_found(self, mock_exists):
        """Test extraction with missing file."""
        mock_exists.return_value = False
        
        extractor = FileExtractor("nonexistent.csv", "csv")
        
        with pytest.raises(FileNotFoundError):
            extractor.extract()
    
    def test_extract_unsupported_file_type(self):
        """Test extraction with unsupported file type."""
        extractor = FileExtractor("test.xyz", "xyz")
        
        with patch('pathlib.Path.exists', return_value=True):
            with pytest.raises(ValueError, match="Unsupported file type"):
                extractor.extract()
