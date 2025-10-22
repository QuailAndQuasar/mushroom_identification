"""
Tests for complete ETL pipeline integration.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.orchestration.etl_pipeline import ETLPipeline
from src.extract.uci_mushroom_extractor import UCIMushroomExtractor
from src.transform.data_cleaner import DataCleaner
from src.transform.feature_engineer import FeatureEngineer
from src.load.database_loader import DatabaseLoader
from src.load.file_loader import FileLoader

class TestETLPipeline:
    """Test complete ETL pipeline."""
    
    def test_initialization(self):
        """Test pipeline initialization."""
        pipeline = ETLPipeline()
        
        assert pipeline.pipeline_id.startswith("etl_")
        assert pipeline.stats["status"] == "initialized"
        assert pipeline.stats["pipeline_id"] == pipeline.pipeline_id
    
    def test_configure_extraction(self):
        """Test extraction configuration."""
        pipeline = ETLPipeline()
        
        # Create mock extractors
        extractor1 = Mock(spec=UCIMushroomExtractor)
        extractor1.name = "uci_mushroom"
        extractor2 = Mock(spec=UCIMushroomExtractor)
        extractor2.name = "file_extractor"
        
        pipeline.configure_extraction([extractor1, extractor2])
        
        assert len(pipeline.extraction_orchestrator.extractors) == 2
    
    def test_configure_transformation(self):
        """Test transformation configuration."""
        pipeline = ETLPipeline()
        
        # Create mock transformers
        cleaner = Mock(spec=DataCleaner)
        engineer = Mock(spec=FeatureEngineer)
        
        pipeline.configure_transformation([cleaner, engineer])
        
        assert len(pipeline.transformation_pipeline.transformers) == 2
    
    def test_configure_loading(self):
        """Test loading configuration."""
        pipeline = ETLPipeline()
        
        # Create mock loaders
        db_loader = Mock(spec=DatabaseLoader)
        file_loader = Mock(spec=FileLoader)
        
        pipeline.configure_loading([db_loader, file_loader])
        
        assert len(pipeline.loading_pipeline.loaders) == 2
    
    @patch('src.orchestration.etl_pipeline.ExtractionOrchestrator')
    @patch('src.orchestration.etl_pipeline.TransformationPipeline')
    @patch('src.orchestration.etl_pipeline.LoadingPipeline')
    def test_run_pipeline_success(self, mock_loading, mock_transformation, mock_extraction):
        """Test successful pipeline execution."""
        # Mock extraction stage
        mock_extraction_instance = Mock()
        mock_extraction_instance.run_all_extractions.return_value = {
            "uci_mushroom": pd.DataFrame({'class': ['e', 'p'], 'feature1': [1, 2]})
        }
        mock_extraction_instance.get_extraction_summary.return_value = {
            "total_extractors": 1,
            "successful_extractions": 1
        }
        mock_extraction.return_value = mock_extraction_instance
        
        # Mock transformation stage
        mock_transformation_instance = Mock()
        mock_transformation_instance.run_transformations.return_value = pd.DataFrame({
            'class': ['e', 'p'], 'feature1': [1, 2], 'feature2': [3, 4]
        })
        mock_transformation_instance.get_transformation_summary.return_value = {
            "total_transformers": 1,
            "successful_transformations": 1
        }
        mock_transformation_instance.results = {
            "feature_engineer": pd.DataFrame({'class': ['e', 'p'], 'feature1': [1, 2]})
        }
        mock_transformation.return_value = mock_transformation_instance
        
        # Mock loading stage
        mock_loading_instance = Mock()
        mock_loading_instance.run_loadings.return_value = True
        mock_loading_instance.get_loading_summary.return_value = {
            "total_loaders": 1,
            "successful_loadings": 1
        }
        mock_loading.return_value = mock_loading_instance
        
        pipeline = ETLPipeline()
        result = pipeline.run_pipeline()
        
        assert result is True
        assert pipeline.stats["status"] == "completed"
        assert "extraction" in pipeline.stats["stages"]
        assert "transformation" in pipeline.stats["stages"]
        assert "loading" in pipeline.stats["stages"]
    
    @patch('src.orchestration.etl_pipeline.ExtractionOrchestrator')
    def test_run_pipeline_extraction_failure(self, mock_extraction):
        """Test pipeline with extraction failure."""
        # Mock extraction failure
        mock_extraction_instance = Mock()
        mock_extraction_instance.run_all_extractions.return_value = {}
        mock_extraction.return_value = mock_extraction_instance
        
        pipeline = ETLPipeline()
        result = pipeline.run_pipeline()
        
        assert result is False
        assert pipeline.stats["status"] == "failed"
        assert pipeline.stats["stages"]["extraction"]["success"] is False
    
    @patch('src.orchestration.etl_pipeline.ExtractionOrchestrator')
    @patch('src.orchestration.etl_pipeline.TransformationPipeline')
    def test_run_pipeline_transformation_failure(self, mock_transformation, mock_extraction):
        """Test pipeline with transformation failure."""
        # Mock successful extraction
        mock_extraction_instance = Mock()
        mock_extraction_instance.run_all_extractions.return_value = {
            "uci_mushroom": pd.DataFrame({'class': ['e', 'p'], 'feature1': [1, 2]})
        }
        mock_extraction.return_value = mock_extraction_instance
        
        # Mock transformation failure
        mock_transformation_instance = Mock()
        mock_transformation_instance.run_transformations.return_value = pd.DataFrame()
        mock_transformation.return_value = mock_transformation_instance
        
        pipeline = ETLPipeline()
        result = pipeline.run_pipeline()
        
        assert result is False
        assert pipeline.stats["status"] == "failed"
        assert pipeline.stats["stages"]["transformation"]["success"] is False
    
    def test_get_pipeline_stats(self):
        """Test getting pipeline statistics."""
        pipeline = ETLPipeline()
        
        stats = pipeline.get_pipeline_stats()
        
        assert "pipeline_id" in stats
        assert "status" in stats
        assert "stages" in stats
        assert stats["pipeline_id"] == pipeline.pipeline_id
    
    def test_get_pipeline_health(self):
        """Test getting pipeline health status."""
        pipeline = ETLPipeline()
        
        health = pipeline.get_pipeline_health()
        
        assert "pipeline_id" in health
        assert "status" in health
        assert "stages_completed" in health
        assert "total_stages" in health
        assert "overall_health" in health
        assert health["total_stages"] == 3
    
    @patch('src.orchestration.etl_pipeline.config')
    def test_save_pipeline_logs(self, mock_config, tmp_path):
        """Test saving pipeline logs."""
        mock_config.processed_data_dir = tmp_path
        
        pipeline = ETLPipeline()
        pipeline.save_pipeline_logs()
        
        # Check if log file was created
        log_files = list(tmp_path.glob("*_pipeline_logs.json"))
        assert len(log_files) == 1
    
    def test_pipeline_with_real_components(self):
        """Test pipeline with real component instances."""
        pipeline = ETLPipeline()
        
        # Configure with real components
        extractor = UCIMushroomExtractor()
        cleaner = DataCleaner()
        engineer = FeatureEngineer()
        db_loader = DatabaseLoader()
        file_loader = FileLoader()
        
        pipeline.configure_extraction([extractor])
        pipeline.configure_transformation([cleaner, engineer])
        pipeline.configure_loading([db_loader, file_loader])
        
        # Mock the actual operations to avoid external dependencies
        with patch.object(extractor, 'extract') as mock_extract:
            mock_extract.return_value = pd.DataFrame({
                'class': ['e', 'p'], 'feature1': [1, 2], 'feature2': [3, 4]
            })
            
            with patch.object(cleaner, 'transform') as mock_clean:
                mock_clean.return_value = pd.DataFrame({
                    'class': ['e', 'p'], 'feature1': [1, 2], 'feature2': [3, 4]
                })
                
                with patch.object(engineer, 'transform') as mock_engineer:
                    mock_engineer.return_value = pd.DataFrame({
                        'class': ['e', 'p'], 'feature1': [1, 2], 'feature2': [3, 4]
                    })
                    
                    with patch.object(db_loader, 'load') as mock_db_load:
                        mock_db_load.return_value = True
                        
                        with patch.object(file_loader, 'load') as mock_file_load:
                            mock_file_load.return_value = True
                            
                            result = pipeline.run_pipeline()
        
        assert result is True
        assert pipeline.stats["status"] == "completed"