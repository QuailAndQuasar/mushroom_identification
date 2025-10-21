"""
Tests for loading pipeline orchestrator.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.load.loading_pipeline import LoadingPipeline
from src.load.database_loader import DatabaseLoader
from src.load.file_loader import FileLoader

class TestLoadingPipeline:
    """Test loading pipeline orchestrator."""
    
    def test_initialization(self):
        """Test pipeline initialization."""
        pipeline = LoadingPipeline()
        
        assert pipeline.loaders == []
        assert pipeline.results == {}
        assert pipeline.stats == {}
    
    def test_add_loader(self):
        """Test adding loaders."""
        pipeline = LoadingPipeline()
        
        # Create mock loaders
        mock_db_loader = Mock(spec=DatabaseLoader)
        mock_db_loader.name = "database_loader"
        
        mock_file_loader = Mock(spec=FileLoader)
        mock_file_loader.name = "file_loader"
        
        pipeline.add_loader(mock_db_loader)
        pipeline.add_loader(mock_file_loader)
        
        assert len(pipeline.loaders) == 2
        assert pipeline.loaders[0] == mock_db_loader
        assert pipeline.loaders[1] == mock_file_loader
    
    def test_run_loadings_success(self):
        """Test running loadings successfully."""
        pipeline = LoadingPipeline()
        
        # Create mock loaders
        mock_db_loader = Mock(spec=DatabaseLoader)
        mock_db_loader.name = "database_loader"
        mock_db_loader.load.return_value = True
        mock_db_loader.validate.return_value = True
        
        mock_file_loader = Mock(spec=FileLoader)
        mock_file_loader.name = "file_loader"
        mock_file_loader.load.return_value = True
        mock_file_loader.validate.return_value = True
        
        pipeline.add_loader(mock_db_loader)
        pipeline.add_loader(mock_file_loader)
        
        # Create test data
        test_data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        
        result = pipeline.run_loadings(test_data)
        
        assert result is True
        assert len(pipeline.results) == 2
        assert "database_loader" in pipeline.results
        assert "file_loader" in pipeline.results
    
    def test_run_loadings_with_failure(self):
        """Test running loadings with some failures."""
        pipeline = LoadingPipeline()
        
        # Create successful loader
        mock_db_loader = Mock(spec=DatabaseLoader)
        mock_db_loader.name = "database_loader"
        mock_db_loader.load.return_value = True
        mock_db_loader.validate.return_value = True
        
        # Create failing loader
        mock_file_loader = Mock(spec=FileLoader)
        mock_file_loader.name = "file_loader"
        mock_file_loader.load.return_value = False
        mock_file_loader.validate.return_value = True
        
        pipeline.add_loader(mock_db_loader)
        pipeline.add_loader(mock_file_loader)
        
        test_data = pd.DataFrame({'col1': [1, 2]})
        
        result = pipeline.run_loadings(test_data)
        
        # Should continue with successful loadings
        assert result is True  # At least one succeeded
        assert len(pipeline.results) == 1
        assert "database_loader" in pipeline.results
        assert "file_loader" not in pipeline.results
    
    def test_run_loadings_all_fail(self):
        """Test running loadings when all fail."""
        pipeline = LoadingPipeline()
        
        # Create failing loaders
        mock_db_loader = Mock(spec=DatabaseLoader)
        mock_db_loader.name = "database_loader"
        mock_db_loader.load.return_value = False
        mock_db_loader.validate.return_value = True
        
        mock_file_loader = Mock(spec=FileLoader)
        mock_file_loader.name = "file_loader"
        mock_file_loader.load.return_value = False
        mock_file_loader.validate.return_value = True
        
        pipeline.add_loader(mock_db_loader)
        pipeline.add_loader(mock_file_loader)
        
        test_data = pd.DataFrame({'col1': [1, 2]})
        
        result = pipeline.run_loadings(test_data)
        
        assert result is False
        assert len(pipeline.results) == 0
    
    def test_run_loadings_with_validation_failure(self):
        """Test running loadings with validation failure."""
        pipeline = LoadingPipeline()
        
        # Create loader that fails validation
        mock_loader = Mock(spec=DatabaseLoader)
        mock_loader.name = "database_loader"
        mock_loader.validate.return_value = False  # Validation fails
        
        pipeline.add_loader(mock_loader)
        
        test_data = pd.DataFrame({'col1': [1, 2]})
        
        result = pipeline.run_loadings(test_data)
        
        # Should not include failed validation
        assert len(pipeline.results) == 0
    
    def test_get_loading_summary(self):
        """Test getting loading summary."""
        pipeline = LoadingPipeline()
        
        # Add some results
        pipeline.results = {
            "database_loader": True,
            "file_loader": True
        }
        
        summary = pipeline.get_loading_summary()
        
        assert summary["total_loaders"] == 0  # No loaders added yet
        assert summary["successful_loadings"] == 2
        assert summary["failed_loadings"] == 0
        assert "database_loader" in summary["loaders"]
        assert "file_loader" in summary["loaders"]
    
    def test_save_loading_logs(self, tmp_path):
        """Test saving loading logs."""
        pipeline = LoadingPipeline()
        
        # Add some results
        pipeline.results = {
            "database_loader": True,
            "file_loader": False
        }
        
        with patch('src.load.loading_pipeline.config') as mock_config:
            mock_config.processed_data_dir = tmp_path
            
            pipeline.save_loading_logs()
            
            # Check if log file was created
            log_file = tmp_path / "loading_logs.json"
            assert log_file.exists()
    
    def test_pipeline_with_real_loaders(self, tmp_path):
        """Test pipeline with real loader instances."""
        pipeline = LoadingPipeline()
        
        # Add real loaders
        db_loader = DatabaseLoader({"table_name": "test_table"})
        file_loader = FileLoader({
            "file_format": "csv",
            "output_dir": str(tmp_path)
        })
        
        pipeline.add_loader(db_loader)
        pipeline.add_loader(file_loader)
        
        # Create test data
        test_data = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
        
        # Mock database operations to avoid actual DB connection
        with patch.object(db_loader, 'load', return_value=True):
            result = pipeline.run_loadings(test_data)
        
        assert result is True
        assert len(pipeline.results) == 2
        assert "database_loader" in pipeline.results
        assert "file_loader" in pipeline.results
    
    def test_run_loadings_with_custom_destinations(self):
        """Test running loadings with custom destinations."""
        pipeline = LoadingPipeline()
        
        # Create mock loaders
        mock_loader = Mock(spec=DatabaseLoader)
        mock_loader.name = "test_loader"
        mock_loader.load.return_value = True
        mock_loader.validate.return_value = True
        
        pipeline.add_loader(mock_loader)
        
        test_data = pd.DataFrame({'col1': [1, 2]})
        destinations = {"test_loader": "custom_destination"}
        
        result = pipeline.run_loadings(test_data, destinations)
        
        assert result is True
        # Verify loader was called with custom destination
        mock_loader.load.assert_called_with(test_data, "custom_destination")
    
    def test_run_loadings_with_partial_destinations(self):
        """Test running loadings with partial destinations."""
        pipeline = LoadingPipeline()
        
        # Create mock loaders
        mock_loader1 = Mock(spec=DatabaseLoader)
        mock_loader1.name = "loader1"
        mock_loader1.load.return_value = True
        mock_loader1.validate.return_value = True
        
        mock_loader2 = Mock(spec=FileLoader)
        mock_loader2.name = "loader2"
        mock_loader2.load.return_value = True
        mock_loader2.validate.return_value = True
        
        pipeline.add_loader(mock_loader1)
        pipeline.add_loader(mock_loader2)
        
        test_data = pd.DataFrame({'col1': [1, 2]})
        destinations = {"loader1": "custom_destination"}
        
        result = pipeline.run_loadings(test_data, destinations)
        
        assert result is True
        # Verify loaders were called with appropriate destinations
        mock_loader1.load.assert_called_with(test_data, "custom_destination")
        mock_loader2.load.assert_called_with(test_data, None)  # Default destination
