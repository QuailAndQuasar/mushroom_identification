"""
Tests for file loader.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from src.load.file_loader import FileLoader

class TestFileLoader:
    """Test file loader."""
    
    def test_initialization(self):
        """Test loader initialization."""
        loader = FileLoader()
        
        assert loader.name == "file_loader"
        assert loader.config["file_format"] == "csv"
        assert loader.config["output_dir"] is not None
        assert loader.config["index"] is False
    
    def test_initialization_with_config(self, tmp_path):
        """Test loader initialization with custom config."""
        config = {
            "file_format": "parquet",
            "output_dir": str(tmp_path / "custom"),
            "compression": "snappy"
        }
        loader = FileLoader(config)
        
        assert loader.config["file_format"] == "parquet"
        assert loader.config["output_dir"] == str(tmp_path / "custom")
        assert loader.config["compression"] == "snappy"
    
    def test_load_csv_success(self, tmp_path):
        """Test successful CSV loading."""
        loader = FileLoader({
            "file_format": "csv",
            "output_dir": str(tmp_path)
        })
        
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.load(test_data, "test_file.csv")
        
        assert result is True
        assert loader.stats["records_loaded"] == 3
        assert loader.stats["file_path"] == str(tmp_path / "test_file.csv")
        assert loader.stats["loading_successful"] is True
        
        # Check if file was created
        output_file = tmp_path / "test_file.csv"
        assert output_file.exists()
    
    
    def test_load_json_success(self, tmp_path):
        """Test successful JSON loading."""
        loader = FileLoader({
            "file_format": "json",
            "output_dir": str(tmp_path)
        })
        
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.load(test_data, "test_file.json")
        
        assert result is True
        assert loader.stats["records_loaded"] == 3
        
        # Check if file was created
        output_file = tmp_path / "test_file.json"
        assert output_file.exists()
    
    def test_load_excel_success(self, tmp_path):
        """Test successful Excel loading."""
        loader = FileLoader({
            "file_format": "excel",
            "output_dir": str(tmp_path)
        })
        
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.load(test_data, "test_file.xlsx")
        
        assert result is True
        assert loader.stats["records_loaded"] == 3
        
        # Check if file was created
        output_file = tmp_path / "test_file.xlsx"
        assert output_file.exists()
    
    def test_load_with_compression(self, tmp_path):
        """Test loading with compression."""
        loader = FileLoader({
            "file_format": "csv",
            "output_dir": str(tmp_path),
            "compression": "gzip"
        })
        
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.load(test_data, "test_file.csv.gz")
        
        assert result is True
        assert loader.stats["records_loaded"] == 3
        
        # Check if compressed file was created
        output_file = tmp_path / "test_file.csv.gz"
        assert output_file.exists()
    
    def test_load_with_custom_format(self, tmp_path):
        """Test loading with custom format."""
        loader = FileLoader({
            "file_format": "custom",
            "output_dir": str(tmp_path)
        })
        
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.load(test_data, "test_file.custom")
        
        assert result is True
        assert loader.stats["records_loaded"] == 3
        
        # Check if file was created
        output_file = tmp_path / "test_file.custom"
        assert output_file.exists()
    
    def test_load_with_error(self, tmp_path):
        """Test loading with error."""
        loader = FileLoader({
            "file_format": "csv",
            "output_dir": str(tmp_path)
        })
        
        # Mock to_csv to raise error
        with patch.object(pd.DataFrame, 'to_csv') as mock_to_csv:
            mock_to_csv.side_effect = Exception("File write error")
            
            test_data = pd.DataFrame({'col1': [1, 2, 3]})
            result = loader.load(test_data, "test_file.csv")
            
            assert result is False
            assert loader.stats["loading_successful"] is False
            assert "error" in loader.stats
    
    def test_validate_clean_data(self):
        """Test validation with clean data."""
        loader = FileLoader()
        
        clean_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.validate(clean_data)
        assert result is True
    
    def test_validate_empty_data(self):
        """Test validation with empty data."""
        loader = FileLoader()
        
        empty_data = pd.DataFrame()
        result = loader.validate(empty_data)
        assert result is False
    
    def test_validate_data_with_inf(self):
        """Test validation with infinite values."""
        loader = FileLoader()
        
        data_with_inf = pd.DataFrame({
            'col1': [1, 2, np.inf],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.validate(data_with_inf)
        assert result is True  # Should pass but with warning
    
    def test_validate_data_with_nan(self):
        """Test validation with NaN values."""
        loader = FileLoader()
        
        data_with_nan = pd.DataFrame({
            'col1': [1, 2, np.nan],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.validate(data_with_nan)
        assert result is True  # Should pass but with warning
    
    def test_get_stats(self):
        """Test getting loading statistics."""
        loader = FileLoader()
        
        # Set some stats
        loader.stats = {
            "records_loaded": 100,
            "file_path": "/path/to/file.csv",
            "loading_successful": True
        }
        
        stats = loader.get_stats()
        assert stats["records_loaded"] == 100
        assert stats["file_path"] == "/path/to/file.csv"
        assert stats["loading_successful"] is True
    
    def test_load_with_default_filename(self, tmp_path):
        """Test loading with default filename."""
        loader = FileLoader({
            "file_format": "csv",
            "output_dir": str(tmp_path)
        })
        
        test_data = pd.DataFrame({'col1': [1, 2, 3]})
        result = loader.load(test_data)
        
        assert result is True
        assert loader.stats["file_path"] == str(tmp_path / "loaded_data.csv")
    
    def test_load_with_metadata(self, tmp_path):
        """Test loading with metadata."""
        loader = FileLoader({
            "file_format": "csv",
            "output_dir": str(tmp_path),
            "save_metadata": True
        })
        
        test_data = pd.DataFrame({'col1': [1, 2, 3]})
        result = loader.load(test_data, "test_file.csv")
        
        assert result is True
        
        # Check if metadata file was created
        metadata_file = tmp_path / "test_file.json"
        assert metadata_file.exists()
    
    def test_load_with_custom_parameters(self, tmp_path):
        """Test loading with custom parameters."""
        loader = FileLoader({
            "file_format": "csv",
            "output_dir": str(tmp_path),
            "index": True,
            "header": False
        })
        
        test_data = pd.DataFrame({'col1': [1, 2, 3]})
        result = loader.load(test_data, "test_file.csv")
        
        assert result is True
        assert loader.stats["loading_successful"] is True
