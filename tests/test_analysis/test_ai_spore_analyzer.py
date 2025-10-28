#!/usr/bin/env python3
"""
Tests for AI-Enhanced Spore Analysis Module

This module tests the AI spore analyzer functionality.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from analysis.ai_spore_analyzer import AISporeAnalyzer


class TestAISporeAnalyzer:
    """Test cases for AISporeAnalyzer class"""
    
    @pytest.fixture
    def sample_spore_database(self):
        """Create a sample spore database for testing"""
        return [
            {
                "species": "Agaricus bisporus",
                "common_name": "Button Mushroom",
                "spore_characteristics": {
                    "spore_print_color": "dark_brown",
                    "spore_shape": "ellipsoid",
                    "spore_size": "6-8 x 4-5 μm",
                    "spore_surface": "smooth"
                },
                "microscopic_features": {
                    "basidia": "4-spored",
                    "cheilocystidia": "present",
                    "pleurocystidia": "absent"
                }
            },
            {
                "species": "Amanita phalloides",
                "common_name": "Death Cap",
                "spore_characteristics": {
                    "spore_print_color": "white",
                    "spore_shape": "globose",
                    "spore_size": "8-10 x 7-9 μm",
                    "spore_surface": "smooth"
                },
                "microscopic_features": {
                    "basidia": "4-spored",
                    "cheilocystidia": "absent",
                    "pleurocystidia": "absent"
                }
            }
        ]
    
    @pytest.fixture
    def temp_database_file(self, sample_spore_database):
        """Create a temporary database file for testing"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_spore_database, f)
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        os.unlink(temp_path)
    
    def test_initialization(self, temp_database_file):
        """Test AISporeAnalyzer initialization"""
        analyzer = AISporeAnalyzer(temp_database_file)
        
        assert analyzer.spore_database_path == Path(temp_database_file)
        assert len(analyzer.spore_database) == 2
        assert analyzer.image_classifier is None  # Placeholder
        assert analyzer.nlp_classifier is None    # Placeholder
        assert analyzer.pattern_recognizer is None  # Placeholder
    
    def test_load_spore_database_success(self, temp_database_file):
        """Test successful spore database loading"""
        analyzer = AISporeAnalyzer(temp_database_file)
        
        assert len(analyzer.spore_database) == 2
        assert analyzer.spore_database[0]["species"] == "Agaricus bisporus"
        assert analyzer.spore_database[1]["species"] == "Amanita phalloides"
    
    def test_load_spore_database_file_not_found(self):
        """Test handling of missing database file"""
        analyzer = AISporeAnalyzer("nonexistent_file.json")
        
        assert analyzer.spore_database == []
    
    def test_load_spore_database_invalid_json(self):
        """Test handling of invalid JSON in database file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name
        
        try:
            analyzer = AISporeAnalyzer(temp_path)
            assert analyzer.spore_database == []
        finally:
            os.unlink(temp_path)
    
    @patch('PIL.Image.open')
    @patch('numpy.array')
    def test_analyze_spore_image_success(self, mock_numpy_array, mock_image_open, temp_database_file):
        """Test successful spore image analysis"""
        # Mock image object
        mock_image = Mock()
        mock_image.size = (100, 100)
        mock_image_open.return_value = mock_image
        
        # Mock numpy array operations properly
        mock_array = Mock()
        mock_array.astype.return_value.__truediv__ = Mock(return_value=mock_array)
        mock_numpy_array.return_value = mock_array
        
        analyzer = AISporeAnalyzer(temp_database_file)
        
        result = analyzer.analyze_spore_image("test_image.jpg")
        
        assert "species_predictions" in result
        assert "confidence" in result
        assert "visual_features" in result
        assert "analysis_method" in result
        assert result["analysis_method"] == "AI Computer Vision"
    
    def test_analyze_spore_image_file_not_found(self, temp_database_file):
        """Test handling of missing image file"""
        analyzer = AISporeAnalyzer(temp_database_file)
        
        result = analyzer.analyze_spore_image("nonexistent_image.jpg")
        
        assert "error" in result
        assert "No such file or directory" in result["error"]
    
    def test_analyze_text_description_success(self, temp_database_file):
        """Test successful text description analysis"""
        analyzer = AISporeAnalyzer(temp_database_file)
        
        description = "White spore print with globose spores"
        result = analyzer.analyze_text_description(description)
        
        assert "species_prediction" in result
        assert "confidence" in result
        assert "extracted_features" in result
        assert "analysis_method" in result
        assert result["analysis_method"] == "AI Natural Language Processing"
    
    def test_analyze_text_description_empty(self, temp_database_file):
        """Test handling of empty description"""
        analyzer = AISporeAnalyzer(temp_database_file)
        
        result = analyzer.analyze_text_description("")
        
        assert "species_prediction" in result
        assert "confidence" in result
        assert "extracted_features" in result
    
    def test_comprehensive_ai_analysis_success(self, temp_database_file):
        """Test comprehensive AI analysis"""
        analyzer = AISporeAnalyzer(temp_database_file)
        
        # Test without image path to avoid file not found error
        result = analyzer.comprehensive_ai_analysis(
            text_description="Dark brown spores with smooth surface",
            manual_features={"spore_print_color": "dark_brown"}
        )
        
        assert "image_analysis" in result
        assert "text_analysis" in result
        assert "pattern_analysis" in result
        assert "feature_suggestions" in result
        assert "combined_prediction" in result
    
    def test_intelligent_feature_suggestion(self, temp_database_file):
        """Test intelligent feature suggestion functionality"""
        analyzer = AISporeAnalyzer(temp_database_file)
        
        current_features = {"spore_print_color": "white"}
        suggestions = analyzer.intelligent_feature_suggestion(current_features)
        
        assert "current_confidence" in suggestions
        assert "suggestions" in suggestions
        assert "next_steps" in suggestions
        assert "analysis_method" in suggestions
        assert isinstance(suggestions["suggestions"], list)
    
    def test_pattern_recognition_analysis(self, temp_database_file):
        """Test pattern recognition analysis"""
        analyzer = AISporeAnalyzer(temp_database_file)
        
        features = {
            "spore_print_color": "white",
            "spore_shape": "globose",
            "spore_surface": "smooth"
        }
        
        result = analyzer.pattern_recognition_analysis(features)
        
        assert "detected_patterns" in result
        assert "similar_species" in result
        assert "pattern_confidence" in result
        assert "analysis_method" in result
        assert isinstance(result["similar_species"], list)


class TestAISporeAnalyzerIntegration:
    """Integration tests for AISporeAnalyzer"""
    
    def test_end_to_end_analysis_workflow(self):
        """Test complete analysis workflow"""
        # Create temporary database
        sample_data = [
            {
                "species": "Test Species",
                "common_name": "Test Mushroom",
                "spore_characteristics": {
                    "spore_print_color": "white",
                    "spore_shape": "globose",
                    "spore_size": "8-10 x 7-9 μm",
                    "spore_surface": "smooth"
                },
                "microscopic_features": {
                    "basidia": "4-spored",
                    "cheilocystidia": "absent",
                    "pleurocystidia": "absent"
                }
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_data, f)
            temp_path = f.name
        
        try:
            analyzer = AISporeAnalyzer(temp_path)
            
            # Test basic functionality
            assert len(analyzer.spore_database) == 1
            assert analyzer.spore_database[0]["species"] == "Test Species"
            
            # Test text analysis
            result = analyzer.analyze_text_description("White spores")
            assert "species_prediction" in result
            
            # Test feature suggestions
            suggestions = analyzer.intelligent_feature_suggestion({"spore_print_color": "white"})
            assert "suggestions" in suggestions
            
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__])
