#!/usr/bin/env python3
"""
Enhanced Mushroom Identification App with Spore Analysis

This Flask application provides mushroom identification with advanced spore analysis capabilities.
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

app = Flask(__name__)

# Global variables for model and data
model = None
feature_names = None
spore_analyzer = None

def load_model_and_data():
    """Load the trained model and feature names"""
    global model, feature_names, spore_analyzer
    
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
        
        # Initialize spore analyzer
        spore_analyzer = SporeAnalyzer()
        print("✅ Spore analyzer initialized")
        
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
    """Spore analysis page"""
    return render_template('spore_analysis.html')

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
    """Analyze spore characteristics for identification"""
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

@app.route('/spore_database')
def spore_database():
    """Get spore database information"""
    try:
        if spore_analyzer is None:
            return jsonify({'error': 'Spore analyzer not initialized'}), 500
        
        # Get database statistics
        stats = spore_analyzer.get_database_stats()
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/species_spore_info/<species_name>')
def species_spore_info(species_name):
    """Get spore information for a specific species"""
    try:
        if spore_analyzer is None:
            return jsonify({'error': 'Spore analyzer not initialized'}), 500
        
        # Get spore information for species
        spore_info = spore_analyzer.get_species_spore_info(species_name)
        
        if spore_info is None:
            return jsonify({'error': 'Species not found'}), 404
        
        return jsonify(spore_info)
    
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
        'total_features': len(feature_names) if feature_names else 0
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
    print("🍄 Starting Enhanced Mushroom Identification App with Spore Analysis...")
    print("=" * 70)
    
    # Load model and data
    if load_model_and_data():
        print("🚀 Starting Flask application...")
        print("📱 Web Interface: http://localhost:5002")
        print("🔬 Spore Analysis: http://localhost:5002/spore-analysis")
        print("🏥 Health Check: http://localhost:5002/health")
        print("📊 Species Database: http://localhost:5002/species")
        print("=" * 70)
        
        # Run the app
        app.run(host='0.0.0.0', port=5002, debug=True)
    else:
        print("❌ Failed to load model and data. Exiting.")
        sys.exit(1)
