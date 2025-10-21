"""
Tests for extraction orchestrator.
"""
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.extract.extraction_orchestrator import ExtractionOrchestrator
from src.extract.base_extractor import BaseExtractor

class TestExtractionOrchestrator:
    """Test extraction orchestrator."""
    
    def test_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = ExtractionOrchestrator()
        
        assert orchestrator.extractors == []
        assert orchestrator.results == {}
    
    def test_add_extractor(self):
        """Test adding extractors."""
        orchestrator = ExtractionOrchestrator()
        
        # Create mock extractor
        mock_extractor = Mock(spec=BaseExtractor)
        mock_extractor.name = "test_extractor"
        
        orchestrator.add_extractor(mock_extractor)
        
        assert len(orchestrator.extractors) == 1
        assert orchestrator.extractors[0] == mock_extractor
    
    def test_run_all_extractions_success(self):
        """Test running all extractions successfully."""
        orchestrator = ExtractionOrchestrator()
        
        # Create mock extractors
        mock_extractor1 = Mock(spec=BaseExtractor)
        mock_extractor1.name = "extractor1"
        mock_extractor1.extract.return_value = pd.DataFrame({'col1': [1, 2]})
        mock_extractor1.validate.return_value = True
        
        mock_extractor2 = Mock(spec=BaseExtractor)
        mock_extractor2.name = "extractor2"
        mock_extractor2.extract.return_value = pd.DataFrame({'col2': [3, 4]})
        mock_extractor2.validate.return_value = True
        
        orchestrator.add_extractor(mock_extractor1)
        orchestrator.add_extractor(mock_extractor2)
        
        results = orchestrator.run_all_extractions()
        
        assert len(results) == 2
        assert "extractor1" in results
        assert "extractor2" in results
    
    def test_run_all_extractions_with_failure(self):
        """Test running extractions with some failures."""
        orchestrator = ExtractionOrchestrator()
        
        # Create successful extractor
        mock_extractor1 = Mock(spec=BaseExtractor)
        mock_extractor1.name = "extractor1"
        mock_extractor1.extract.return_value = pd.DataFrame({'col1': [1, 2]})
        mock_extractor1.validate.return_value = True
        
        # Create failing extractor
        mock_extractor2 = Mock(spec=BaseExtractor)
        mock_extractor2.name = "extractor2"
        mock_extractor2.extract.side_effect = Exception("Extraction failed")
        
        orchestrator.add_extractor(mock_extractor1)
        orchestrator.add_extractor(mock_extractor2)
        
        results = orchestrator.run_all_extractions()
        
        assert len(results) == 1
        assert "extractor1" in results
        assert "extractor2" not in results
    
    def test_get_extraction_summary(self):
        """Test getting extraction summary."""
        orchestrator = ExtractionOrchestrator()
        
        # Add some results
        orchestrator.results = {
            "extractor1": pd.DataFrame({'col1': [1, 2]}),
            "extractor2": pd.DataFrame({'col2': [3, 4, 5]})
        }
        
        summary = orchestrator.get_extraction_summary()
        
        assert summary["total_extractors"] == 0  # No extractors added yet
        assert summary["successful_extractions"] == 2
        assert summary["total_records"] == 5
        assert "extractor1" in summary["extractors"]
        assert "extractor2" in summary["extractors"]
