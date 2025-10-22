"""
Tests for transformation pipeline orchestrator.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.transform.transformation_pipeline import TransformationPipeline
from src.transform.data_cleaner import DataCleaner
from src.transform.feature_engineer import FeatureEngineer

class TestTransformationPipeline:
    """Test transformation pipeline orchestrator."""
    
    def test_initialization(self):
        """Test pipeline initialization."""
        pipeline = TransformationPipeline()
        
        assert pipeline.transformers == []
        assert pipeline.results == {}
        assert pipeline.stats == {}
    
    def test_add_transformer(self):
        """Test adding transformers."""
        pipeline = TransformationPipeline()
        
        # Create mock transformers
        mock_cleaner = Mock(spec=DataCleaner)
        mock_cleaner.name = "data_cleaner"
        
        mock_engineer = Mock(spec=FeatureEngineer)
        mock_engineer.name = "feature_engineer"
        
        pipeline.add_transformer(mock_cleaner)
        pipeline.add_transformer(mock_engineer)
        
        assert len(pipeline.transformers) == 2
        assert pipeline.transformers[0] == mock_cleaner
        assert pipeline.transformers[1] == mock_engineer
    
    def test_run_transformations_success(self):
        """Test running transformations successfully."""
        pipeline = TransformationPipeline()
        
        # Create mock transformers
        mock_cleaner = Mock(spec=DataCleaner)
        mock_cleaner.name = "data_cleaner"
        mock_cleaner.transform.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_cleaner.validate.return_value = True
        
        mock_engineer = Mock(spec=FeatureEngineer)
        mock_engineer.name = "feature_engineer"
        mock_engineer.transform.return_value = pd.DataFrame({'feature1': [1, 2], 'feature2': [3, 4]})
        mock_engineer.validate.return_value = True
        
        pipeline.add_transformer(mock_cleaner)
        pipeline.add_transformer(mock_engineer)
        
        # Create test data
        test_data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        
        result = pipeline.run_transformations(test_data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(pipeline.results) == 2
        assert "data_cleaner" in pipeline.results
        assert "feature_engineer" in pipeline.results
    
    def test_run_transformations_with_failure(self):
        """Test running transformations with some failures."""
        pipeline = TransformationPipeline()
        
        # Create successful transformer
        mock_cleaner = Mock(spec=DataCleaner)
        mock_cleaner.name = "data_cleaner"
        mock_cleaner.transform.return_value = pd.DataFrame({'col1': [1, 2]})
        mock_cleaner.validate.return_value = True
        
        # Create failing transformer
        mock_engineer = Mock(spec=FeatureEngineer)
        mock_engineer.name = "feature_engineer"
        mock_engineer.transform.side_effect = Exception("Transformation failed")
        
        pipeline.add_transformer(mock_cleaner)
        pipeline.add_transformer(mock_engineer)
        
        test_data = pd.DataFrame({'col1': [1, 2]})
        
        result = pipeline.run_transformations(test_data)
        
        # Should continue with successful transformations
        assert isinstance(result, pd.DataFrame)
        assert len(pipeline.results) == 1
        assert "data_cleaner" in pipeline.results
        assert "feature_engineer" not in pipeline.results
    
    
    def test_save_combined_data(self, tmp_path):
        """Test saving combined transformation results."""
        pipeline = TransformationPipeline()
        
        # Add some results
        pipeline.results = {
            "data_cleaner": pd.DataFrame({'col1': [1, 2]}),
            "feature_engineer": pd.DataFrame({'feature1': [1, 2], 'feature2': [3, 4]})
        }
        
        with patch('src.transform.transformation_pipeline.config') as mock_config:
            mock_config.processed_data_dir = tmp_path
            
            pipeline.save_combined_data("test_output.csv")
            
            # Check if file was created
            output_file = tmp_path / "test_output.csv"
            assert output_file.exists()
    
    def test_run_transformations_with_validation_failure(self):
        """Test running transformations with validation failure."""
        pipeline = TransformationPipeline()
        
        # Create transformer that fails validation
        mock_cleaner = Mock(spec=DataCleaner)
        mock_cleaner.name = "data_cleaner"
        mock_cleaner.transform.return_value = pd.DataFrame({'col1': [1, 2]})
        mock_cleaner.validate.return_value = False  # Validation fails
        
        pipeline.add_transformer(mock_cleaner)
        
        test_data = pd.DataFrame({'col1': [1, 2]})
        
        result = pipeline.run_transformations(test_data)
        
        # Should not include failed validation
        assert len(pipeline.results) == 0
    
