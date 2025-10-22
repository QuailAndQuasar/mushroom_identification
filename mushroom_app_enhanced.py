#!/usr/bin/env python3
"""
Enhanced Mushroom Identifier Web Application

This Flask app provides mushroom identification with species names and detailed information.
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from pathlib import Path
import json
import numpy as np

app = Flask(__name__)

# Load the trained model
model_path = Path("models/random_forest.joblib")
if model_path.exists():
    model = joblib.load(model_path)
    print("✅ Model loaded successfully")
else:
    print("❌ Model not found. Train the model first!")
    model = None

# Load feature names from training data
try:
    df = pd.read_csv('data/processed/loaded_data.csv')
    feature_names = df.drop('class', axis=1).columns.tolist()
    print(f"✅ Loaded {len(feature_names)} feature names")
except:
    feature_names = []
    print("❌ Could not load feature names")

# Load mushroom species database
try:
    with open('data/mushroom_species.json', 'r') as f:
        species_db = json.load(f)
    print("✅ Loaded mushroom species database")
except:
    species_db = {"species": {"edible": {}, "poisonous": {}}}
    print("❌ Could not load species database")

def identify_mushroom_species(features):
    """
    Identify the most likely mushroom species based on features.
    
    Args:
        features: Dictionary of mushroom features
        
    Returns:
        dict: Species information or None if no match
    """
    if not species_db or "species" not in species_db:
        return None
    
    best_match = None
    best_score = 0
    
    # Check edible species
    for species_id, species_info in species_db["species"]["edible"].items():
        score = calculate_similarity_score(features, species_info["characteristics"])
        if score > best_score:
            best_score = score
            best_match = {
                "species_id": species_id,
                "species_info": species_info,
                "category": "edible",
                "confidence": score
            }
    
    # Check poisonous species
    for species_id, species_info in species_db["species"]["poisonous"].items():
        score = calculate_similarity_score(features, species_info["characteristics"])
        if score > best_score:
            best_score = score
            best_match = {
                "species_id": species_id,
                "species_info": species_info,
                "category": "poisonous",
                "confidence": score
            }
    
    # Only return if confidence is above threshold
    if best_match and best_match["confidence"] > 0.3:
        return best_match
    
    return None

def calculate_similarity_score(features, species_characteristics):
    """
    Calculate similarity score between input features and species characteristics.
    
    Args:
        features: Input mushroom features
        species_characteristics: Species characteristic ranges
        
    Returns:
        float: Similarity score (0-1)
    """
    score = 0
    total_features = 0
    
    for feature_name, feature_value in features.items():
        if feature_value:  # Only check if feature is True
            total_features += 1
            
            # Extract the base feature name (e.g., 'cap-shape' from 'cap-shape_b')
            base_feature = feature_name.rsplit('_', 1)[0]
            feature_code = feature_name.split('_')[-1]
            
            if base_feature in species_characteristics:
                if feature_code in species_characteristics[base_feature]:
                    score += 1
    
    return score / max(total_features, 1) if total_features > 0 else 0

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('mushroom_identifier.html')

@app.route('/predict', methods=['POST'])
def predict_mushroom():
    """API endpoint for mushroom classification."""
    try:
        # Get features from request
        features = request.json
        
        if model is None:
            return jsonify({'error': 'Model not available'}), 500
        
        # Convert to DataFrame with all features
        features_df = pd.DataFrame([{col: False for col in feature_names}])
        
        # Set provided features to True
        for feature, value in features.items():
            if feature in features_df.columns:
                features_df[feature] = bool(value)
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0]
        
        # Identify specific species
        species_info = identify_mushroom_species(features)
        
        result = {
            'edible': bool(prediction),
            'confidence': float(max(probability)),
            'edible_probability': float(probability[1]),
            'poisonous_probability': float(probability[0])
        }
        
        # Add species information if identified
        if species_info:
            result['species'] = {
                'common_name': species_info['species_info']['common_name'],
                'scientific_name': species_info['species_info']['scientific_name'],
                'description': species_info['species_info']['description'],
                'category': species_info['category'],
                'species_confidence': species_info['confidence']
            }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/species', methods=['GET'])
def get_species_info():
    """Get information about all known species."""
    return jsonify(species_db)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy', 
        'model_loaded': model is not None,
        'features_loaded': len(feature_names) > 0,
        'species_db_loaded': len(species_db.get('species', {}).get('edible', {})) > 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Using port 5001 to avoid conflicts
