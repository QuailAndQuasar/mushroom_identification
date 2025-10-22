"""
Tests for database loader.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from src.load.database_loader import DatabaseLoader

class TestDatabaseLoader:
    """Test database loader."""
    
    def test_initialization(self):
        """Test loader initialization."""
        loader = DatabaseLoader()
        
        assert loader.name == "database_loader"
        assert loader.config["table_name"] == "mushroom_data"
        assert loader.config["if_exists"] == "replace"
        assert loader.config["index"] is False
        assert loader.config["chunksize"] == 1000
    
    def test_initialization_with_config(self):
        """Test loader initialization with custom config."""
        config = {
            "table_name": "custom_table",
            "if_exists": "append",
            "chunksize": 500
        }
        loader = DatabaseLoader(config)
        
        assert loader.config["table_name"] == "custom_table"
        assert loader.config["if_exists"] == "append"
        assert loader.config["chunksize"] == 500
    
    @patch('src.load.database_loader.create_engine')
    def test_create_engine_success(self, mock_create_engine):
        """Test successful engine creation."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        loader = DatabaseLoader()
        loader._create_engine()
        
        assert loader.engine == mock_engine
        assert loader.metadata is not None
        mock_create_engine.assert_called_once()
    
    @patch('src.load.database_loader.create_engine')
    def test_create_engine_failure(self, mock_create_engine):
        """Test engine creation failure."""
        mock_create_engine.side_effect = Exception("Connection failed")
        
        loader = DatabaseLoader()
        
        with pytest.raises(Exception, match="Connection failed"):
            loader._create_engine()
    
    @patch('src.load.database_loader.create_engine')
    def test_create_schema(self, mock_create_engine):
        """Test schema creation."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        loader = DatabaseLoader()
        loader._create_engine()
        
        # Create test data
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c'],
            'col3': [1.1, 2.2, 3.3]
        })
        
        loader._create_schema(test_data)
        
        # Verify table creation was called
        assert loader.metadata is not None
    
    @patch('src.load.database_loader.create_engine')
    def test_load_success(self, mock_create_engine):
        """Test successful data loading."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        loader = DatabaseLoader()
        loader._create_engine()
        
        # Create test data
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            mock_to_sql.return_value = None
            
            result = loader.load(test_data, "test_table")
            
            assert result is True
            assert loader.stats["records_loaded"] == 3
            assert loader.stats["table_name"] == "test_table"
            assert loader.stats["loading_successful"] is True
    
    @patch('src.load.database_loader.create_engine')
    def test_load_with_sqlalchemy_error(self, mock_create_engine):
        """Test loading with SQLAlchemy error."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        # Mock to_sql to raise SQLAlchemyError
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            mock_to_sql.side_effect = SQLAlchemyError("Database error")
            
            loader = DatabaseLoader()
            loader._create_engine()
            
            test_data = pd.DataFrame({'col1': [1, 2, 3]})
            result = loader.load(test_data)
            
            assert result is False
            assert loader.stats["loading_successful"] is False
            assert "error" in loader.stats
    
    @patch('src.load.database_loader.create_engine')
    def test_load_with_general_error(self, mock_create_engine):
        """Test loading with general error."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        # Mock to_sql to raise general error
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            mock_to_sql.side_effect = Exception("General error")
            
            loader = DatabaseLoader()
            loader._create_engine()
            
            test_data = pd.DataFrame({'col1': [1, 2, 3]})
            result = loader.load(test_data)
            
            assert result is False
            assert loader.stats["loading_successful"] is False
            assert "error" in loader.stats
    
    def test_validate_clean_data(self):
        """Test validation with clean data."""
        loader = DatabaseLoader()
        
        clean_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c'],
            'col3': [1.1, 2.2, 3.3]
        })
        
        result = loader.validate(clean_data)
        assert result is True
    
    def test_validate_empty_data(self):
        """Test validation with empty data."""
        loader = DatabaseLoader()
        
        empty_data = pd.DataFrame()
        result = loader.validate(empty_data)
        assert result is False
    
    def test_validate_data_with_inf(self):
        """Test validation with infinite values."""
        loader = DatabaseLoader()
        
        data_with_inf = pd.DataFrame({
            'col1': [1, 2, np.inf],
            'col2': ['a', 'b', 'c']
        })
        
        result = loader.validate(data_with_inf)
        assert result is True  # Should pass but with warning
    
    def test_validate_data_with_long_strings(self):
        """Test validation with long strings."""
        loader = DatabaseLoader()
        
        # Create data with long strings
        long_string = "a" * 300  # Longer than 255 characters
        data_with_long_strings = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', long_string]
        })
        
        result = loader.validate(data_with_long_strings)
        assert result is True  # Should pass but with warning
    
    @patch('src.load.database_loader.create_engine')
    def test_test_connection_success(self, mock_create_engine):
        """Test successful connection test."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        # Mock successful connection
        mock_conn = Mock()
        mock_conn.execute.return_value = None
        
        # Mock context manager
        mock_context = Mock()
        mock_context.__enter__ = Mock(return_value=mock_conn)
        mock_context.__exit__ = Mock(return_value=None)
        mock_engine.connect.return_value = mock_context
        
        loader = DatabaseLoader()
        result = loader.test_connection()
        
        assert result is True
        mock_create_engine.assert_called_once()
    
    @patch('src.load.database_loader.create_engine')
    def test_test_connection_failure(self, mock_create_engine):
        """Test connection test failure."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        # Mock connection failure
        mock_engine.connect.side_effect = Exception("Connection failed")
        
        loader = DatabaseLoader()
        result = loader.test_connection()
        
        assert result is False
    
    def test_get_stats(self):
        """Test getting loading statistics."""
        loader = DatabaseLoader()
        
        # Set some stats
        loader.stats = {
            "records_loaded": 100,
            "table_name": "test_table",
            "loading_successful": True
        }
        
        stats = loader.get_stats()
        assert stats["records_loaded"] == 100
        assert stats["table_name"] == "test_table"
        assert stats["loading_successful"] is True
    
    @patch('src.load.database_loader.create_engine')
    def test_load_with_custom_destination(self, mock_create_engine):
        """Test loading with custom destination."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        loader = DatabaseLoader()
        loader._create_engine()
        
        test_data = pd.DataFrame({'col1': [1, 2, 3]})
        
        # Mock the to_sql method
        with patch.object(test_data, 'to_sql') as mock_to_sql:
            mock_to_sql.return_value = None
            
            result = loader.load(test_data, "custom_table")
            
            assert result is True
            assert loader.stats["table_name"] == "custom_table"
    
    @patch('src.load.database_loader.create_engine')
    def test_load_with_default_destination(self, mock_create_engine):
        """Test loading with default destination."""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        loader = DatabaseLoader({"table_name": "default_table"})
        loader._create_engine()
        
        test_data = pd.DataFrame({'col1': [1, 2, 3]})
        
        # Mock the to_sql method
        with patch.object(test_data, 'to_sql') as mock_to_sql:
            mock_to_sql.return_value = None
            
            result = loader.load(test_data)
            
            assert result is True
            assert loader.stats["table_name"] == "default_table"
