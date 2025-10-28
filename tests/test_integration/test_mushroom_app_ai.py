#!/usr/bin/env python3
"""
Tests for AI-Powered Mushroom Flask Application

This module tests the AI-enhanced Flask application functionality.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import the Flask app
import mushroom_app_ai as app_module


class TestMushroomAppAI:
    """Test cases for AI-powered Flask application"""
    
    @pytest.fixture
    def client(self):
        """Create test client for Flask app"""
        app_module.app.config['TESTING'] = True
        
        # Mock the model loading
        with patch.object(app_module, 'load_model_and_data', return_value=True):
            with patch.object(app_module, 'model', Mock()):
                with patch.object(app_module, 'feature_names', ['feature1', 'feature2']):
                    with patch.object(app_module, 'spore_analyzer', Mock()):
                        with patch.object(app_module, 'ai_spore_analyzer', Mock()):
                            client = app_module.app.test_client()
                            yield client
    
    def test_index_route(self, client):
        """Test main index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'mushroom' in response.data.lower()
    
    def test_spore_analysis_route(self, client):
        """Test spore analysis route"""
        response = client.get('/spore-analysis')
        assert response.status_code == 200
        assert b'spore' in response.data.lower()
    
    def test_ai_analysis_route(self, client):
        """Test AI analysis route"""
        response = client.get('/ai-analysis')
        assert response.status_code == 200
        assert b'ai' in response.data.lower()
    
    def test_predict_route_success(self, client):
        """Test successful prediction"""
        # Mock model prediction
        mock_model = Mock()
        mock_model.predict.return_value = [1]  # Edible
        mock_model.predict_proba.return_value = [[0.2, 0.8]]  # [poisonous, edible]
        
        with patch.object(app_module, 'model', mock_model):
            test_data = {
                'feature1': True,
                'feature2': False
            }
            
            response = client.post('/predict', 
                                 json=test_data,
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['edible'] is True
            assert data['confidence'] == 0.8
    
    def test_predict_route_model_not_loaded(self, client):
        """Test prediction when model is not loaded"""
        with patch.object(app_module, 'model', None):
            test_data = {'feature1': True}
            
            response = client.post('/predict', 
                                 json=test_data,
                                 content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_analyze_spores_route_success(self, client):
        """Test successful spore analysis"""
        # Mock spore analyzer
        mock_analyzer = Mock()
        mock_analyzer.comprehensive_spore_analysis.return_value = {
            'best_match': {
                'species': 'Agaricus bisporus',
                'common_name': 'Button Mushroom',
                'confidence': 0.85
            },
            'all_matches': [],
            'analysis_summary': {
                'total_species_analyzed': 5,
                'final_matches': 1
            }
        }
        
        with patch.object(app_module, 'spore_analyzer', mock_analyzer):
            test_data = {
                'spore_print_color': 'dark_brown',
                'spore_shape': 'ellipsoid',
                'spore_size': '6-8 x 4-5 μm',
                'spore_surface': 'smooth',
                'basidia': '4-spored',
                'cheilocystidia': 'present',
                'pleurocystidia': 'absent'
            }
            
            response = client.post('/analyze_spores', 
                                 json=test_data,
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'best_match' in data
            assert data['best_match']['species'] == 'Agaricus bisporus'
    
    def test_analyze_spores_route_analyzer_not_loaded(self, client):
        """Test spore analysis when analyzer is not loaded"""
        with patch.object(app_module, 'spore_analyzer', None):
            test_data = {'spore_print_color': 'white'}
            
            response = client.post('/analyze_spores', 
                                 json=test_data,
                                 content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_ai_analyze_spores_route_success(self, client):
        """Test successful AI spore analysis"""
        # Mock AI spore analyzer
        mock_ai_analyzer = Mock()
        mock_ai_analyzer.comprehensive_ai_analysis.return_value = {
            'image_analysis': {
                'spore_shape': 'ellipsoid',
                'confidence': 0.8
            },
            'text_analysis': {
                'spore_print_color': 'dark_brown',
                'confidence': 0.75
            },
            'combined_confidence': 0.78,
            'suggested_species': 'Agaricus bisporus'
        }
        
        with patch.object(app_module, 'ai_spore_analyzer', mock_ai_analyzer):
            test_data = {
                'image_path': 'test_image.jpg',
                'description': 'Dark brown spores with ellipsoid shape'
            }
            
            response = client.post('/ai_analyze_spores', 
                                 json=test_data,
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'image_analysis' in data
            assert 'text_analysis' in data
            assert 'combined_confidence' in data
    
    def test_ai_analyze_spores_route_analyzer_not_loaded(self, client):
        """Test AI spore analysis when analyzer is not loaded"""
        with patch.object(app_module, 'ai_spore_analyzer', None):
            test_data = {'image_path': 'test.jpg'}
            
            response = client.post('/ai_analyze_spores', 
                                 json=test_data,
                                 content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_spore_database_route(self, client):
        """Test spore database route"""
        # Mock spore analyzer
        mock_analyzer = Mock()
        mock_analyzer.get_database_stats.return_value = {
            'total_species': 5,
            'spore_colors': {'white': 2, 'brown': 3},
            'spore_shapes': {'ellipsoid': 3, 'globose': 2}
        }
        
        with patch.object(app_module, 'spore_analyzer', mock_analyzer):
            response = client.get('/spore_database')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'total_species' in data
            assert data['total_species'] == 5
    
    def test_species_spore_info_route_success(self, client):
        """Test species spore info route"""
        # Mock spore analyzer
        mock_analyzer = Mock()
        mock_analyzer.get_species_spore_info.return_value = {
            'spore_characteristics': {
                'spore_print_color': 'dark_brown',
                'spore_shape': 'ellipsoid'
            },
            'microscopic_features': {
                'basidia': '4-spored',
                'cheilocystidia': 'present'
            }
        }
        
        with patch.object(app_module, 'spore_analyzer', mock_analyzer):
            response = client.get('/species_spore_info/Agaricus%20bisporus')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert 'spore_characteristics' in data
            assert data['spore_characteristics']['spore_print_color'] == 'dark_brown'
    
    def test_species_spore_info_route_not_found(self, client):
        """Test species spore info route when species not found"""
        # Mock spore analyzer
        mock_analyzer = Mock()
        mock_analyzer.get_species_spore_info.return_value = None
        
        with patch.object(app_module, 'spore_analyzer', mock_analyzer):
            response = client.get('/species_spore_info/Nonexistent%20Species')
            
            assert response.status_code == 404
            data = json.loads(response.data)
            assert 'error' in data
    
    def test_health_route(self, client):
        """Test health check route"""
        with patch.object(app_module, 'model', Mock()):
            with patch.object(app_module, 'feature_names', ['feature1']):
                with patch.object(app_module, 'spore_analyzer', Mock()):
                    with patch.object(app_module, 'ai_spore_analyzer', Mock()):
                        response = client.get('/health')
                        
                        assert response.status_code == 200
                        data = json.loads(response.data)
                        assert data['status'] == 'healthy'
                        assert data['model_loaded'] is True
                        assert data['spore_analyzer_loaded'] is True
                        assert data['ai_spore_analyzer_loaded'] is True
    
    def test_species_route(self, client):
        """Test species database route"""
        # Mock species database file
        sample_species = {
            'species': [
                {
                    'scientific_name': 'Agaricus bisporus',
                    'common_name': 'Button Mushroom',
                    'description': 'Common edible mushroom'
                }
            ]
        }
        
        with patch('builtins.open', mock_open(json.dumps(sample_species))):
            with patch('os.path.exists', return_value=True):
                response = client.get('/species')
                
                assert response.status_code == 200
                data = json.loads(response.data)
                assert 'species' in data
                assert len(data['species']) == 1
    
    def test_species_route_file_not_found(self, client):
        """Test species route when database file not found"""
        with patch('os.path.exists', return_value=False):
            response = client.get('/species')
            
            assert response.status_code == 404
            data = json.loads(response.data)
            assert 'error' in data


class TestMushroomAppAIIntegration:
    """Integration tests for AI-powered Flask application"""
    
    def test_load_model_and_data_success(self):
        """Test successful model and data loading"""
        # Mock file existence and model loading
        with patch('os.path.exists', return_value=True):
            with patch('joblib.load', return_value=Mock()):
                with patch('pandas.read_csv', return_value=Mock()):
                    with patch('src.analysis.spore_analyzer.SporeAnalyzer', return_value=Mock()):
                        with patch('src.analysis.ai_spore_analyzer.AISporeAnalyzer', return_value=Mock()):
                            result = app_module.load_model_and_data()
                            assert result is True
    
    def test_load_model_and_data_model_not_found(self):
        """Test model loading when model file not found"""
        with patch('os.path.exists', side_effect=lambda x: 'joblib' not in x):
            result = app_module.load_model_and_data()
            assert result is False
    
    def test_load_model_and_data_feature_names_not_found(self):
        """Test model loading when feature names file not found"""
        with patch('os.path.exists', side_effect=lambda x: 'loaded_data.csv' not in x):
            result = app_module.load_model_and_data()
            assert result is False


def mock_open(content):
    """Helper function to mock file opening"""
    from unittest.mock import mock_open as _mock_open
    return _mock_open(read_data=content)


if __name__ == "__main__":
    pytest.main([__file__])
