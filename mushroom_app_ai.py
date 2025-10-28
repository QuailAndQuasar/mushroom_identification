#!/usr/bin/env python3
"""
Enhanced Mushroom Identification App with AI-Powered Spore Analysis

This Flask application provides both traditional rule-based and AI-enhanced spore analysis.
"""

import os
import sys
import json
import joblib
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from typing import Dict, Any, Optional

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from analysis.spore_analyzer import SporeAnalyzer
from analysis.ai_spore_analyzer import AISporeAnalyzer

app = Flask(__name__)

# Global variables for model and data
model = None
feature_names = None
spore_analyzer = None
ai_spore_analyzer = None

def load_model_and_data():
    """Load the trained model and feature names"""
    global model, feature_names, spore_analyzer, ai_spore_analyzer
    
    try:
        # Load the trained model
        model_path = "models/random_forest.joblib"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            print("✅ Model loaded successfully")
        else:
            print("❌ Model file not found")
            return False
        
        # Load feature names
        feature_names_path = "data/processed/loaded_data.csv"
        if os.path.exists(feature_names_path):
            df = pd.read_csv(feature_names_path)
            feature_names = [col for col in df.columns if col != 'class']
            print(f"✅ Loaded {len(feature_names)} feature names")
        else:
            print("❌ Feature names file not found")
            return False
        
        # Initialize traditional spore analyzer
        spore_analyzer = SporeAnalyzer()
        print("✅ Traditional spore analyzer initialized")
        
        # Initialize AI spore analyzer
        ai_spore_analyzer = AISporeAnalyzer()
        print("✅ AI spore analyzer initialized")
        
        return True
    except Exception as e:
        print(f"❌ Error loading model and data: {e}")
        return False

@app.route('/')
def index():
    """Main page with mushroom identification form"""
    return render_template('mushroom_identifier.html')

@app.route('/spore-analysis')
def spore_analysis():
    """Traditional spore analysis page"""
    return render_template('spore_analysis.html')

@app.route('/ai-spore-analysis')
def ai_spore_analysis():
    """AI-enhanced spore analysis page"""
    return render_template('ai_spore_analysis.html')

@app.route('/predict', methods=['POST'])
def predict_mushroom():
    """Predict mushroom edibility based on features"""
    try:
        if model is None or feature_names is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get features from request
        features = request.get_json()
        
        # Convert features to DataFrame
        features_df = pd.DataFrame([features])
        
        # Ensure all required features are present
        for feature in feature_names:
            if feature not in features_df.columns:
                features_df[feature] = False
        
        # Reorder columns to match training data
        features_df = features_df[feature_names]
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0]
        
        result = {
            'edible': bool(prediction),
            'confidence': float(max(probability)),
            'edible_probability': float(probability[1]),
            'poisonous_probability': float(probability[0])
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_spores', methods=['POST'])
def analyze_spores():
    """Traditional spore analysis"""
    try:
        if spore_analyzer is None:
            return jsonify({'error': 'Spore analyzer not initialized'}), 500
        
        # Get spore characteristics from request
        data = request.get_json()
        
        # Perform comprehensive spore analysis
        analysis_result = spore_analyzer.comprehensive_spore_analysis(
            spore_print_color=data.get('spore_print_color', ''),
            spore_shape=data.get('spore_shape', ''),
            spore_size=data.get('spore_size', ''),
            spore_surface=data.get('spore_surface', ''),
            basidia=data.get('basidia', ''),
            cheilocystidia=data.get('cheilocystidia', ''),
            pleurocystidia=data.get('pleurocystidia', '')
        )
        
        return jsonify(analysis_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai_analyze_spores', methods=['POST'])
def ai_analyze_spores():
    """AI-enhanced spore analysis"""
    try:
        if ai_spore_analyzer is None:
            return jsonify({'error': 'AI spore analyzer not initialized'}), 500
        
        # Get analysis type and data from request
        data = request.get_json()
        analysis_type = data.get('analysis_type', 'comprehensive')
        
        result = {}
        
        if analysis_type == 'text_description':
            # AI text analysis
            description = data.get('description', '')
            result = ai_spore_analyzer.analyze_text_description(description)
            
        elif analysis_type == 'feature_suggestion':
            # AI feature suggestions
            current_features = data.get('current_features', {})
            result = ai_spore_analyzer.intelligent_feature_suggestion(current_features)
            
        elif analysis_type == 'pattern_recognition':
            # AI pattern recognition
            features = data.get('features', {})
            result = ai_spore_analyzer.pattern_recognition_analysis(features)
            
        elif analysis_type == 'comprehensive':
            # Comprehensive AI analysis
            result = ai_spore_analyzer.comprehensive_ai_analysis(
                image_path=data.get('image_path'),
                text_description=data.get('text_description'),
                manual_features=data.get('manual_features')
            )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare_analysis', methods=['POST'])
def compare_analysis():
    """Compare traditional vs AI analysis"""
    try:
        if spore_analyzer is None or ai_spore_analyzer is None:
            return jsonify({'error': 'Analyzers not initialized'}), 500
        
        # Get features from request
        data = request.get_json()
        
        # Traditional analysis
        traditional_result = spore_analyzer.comprehensive_spore_analysis(
            spore_print_color=data.get('spore_print_color', ''),
            spore_shape=data.get('spore_shape', ''),
            spore_size=data.get('spore_size', ''),
            spore_surface=data.get('spore_surface', ''),
            basidia=data.get('basidia', ''),
            cheilocystidia=data.get('cheilocystidia', ''),
            pleurocystidia=data.get('pleurocystidia', '')
        )
        
        # AI analysis
        ai_result = ai_spore_analyzer.pattern_recognition_analysis({
            'spore_print_color': data.get('spore_print_color', ''),
            'spore_shape': data.get('spore_shape', ''),
            'spore_surface': data.get('spore_surface', ''),
            'basidia': data.get('basidia', '')
        })
        
        # Comparison
        comparison = {
            'traditional_analysis': traditional_result,
            'ai_analysis': ai_result,
            'comparison_summary': {
                'traditional_confidence': traditional_result.get('best_match', {}).get('confidence', 0),
                'ai_confidence': ai_result.get('pattern_confidence', 0),
                'agreement': traditional_result.get('best_match', {}).get('species') == ai_result.get('detected_patterns', {}).get('pattern_type', '').replace('_pattern', ''),
                'recommended_method': 'AI' if ai_result.get('pattern_confidence', 0) > traditional_result.get('best_match', {}).get('confidence', 0) else 'Traditional'
            }
        }
        
        return jsonify(comparison)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'feature_names_loaded': feature_names is not None,
        'spore_analyzer_loaded': spore_analyzer is not None,
        'ai_spore_analyzer_loaded': ai_spore_analyzer is not None,
        'total_features': len(feature_names) if feature_names else 0,
        'ai_capabilities': [
            'Computer Vision',
            'Natural Language Processing', 
            'Pattern Recognition',
            'Intelligent Suggestions',
            'Combined Analysis'
        ]
    })

@app.route('/species')
def species():
    """Get species database"""
    try:
        # Load species database
        species_path = "data/mushroom_species.json"
        if os.path.exists(species_path):
            with open(species_path, 'r') as f:
                species_db = json.load(f)
            return jsonify(species_db)
        else:
            return jsonify({'error': 'Species database not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🤖 Starting AI-Enhanced Mushroom Identification App...")
    print("=" * 70)
    
    # Load model and data
    if load_model_and_data():
        print("🚀 Starting Flask application...")
        print("📱 Basic Interface: http://localhost:5003")
        print("🔬 Traditional Spore Analysis: http://localhost:5003/spore-analysis")
        print("🤖 AI Spore Analysis: http://localhost:5003/ai-spore-analysis")
        print("🏥 Health Check: http://localhost:5003/health")
        print("📊 Species Database: http://localhost:5003/species")
        print("=" * 70)
        
        # Run the app
        app.run(host='0.0.0.0', port=5003, debug=True)
    else:
        print("❌ Failed to load model and data. Exiting.")
        sys.exit(1)
