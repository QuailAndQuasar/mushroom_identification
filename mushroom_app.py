
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
from pathlib import Path
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
        
        result = {
            'edible': bool(prediction),
            'confidence': float(max(probability)),
            'edible_probability': float(probability[1]),
            'poisonous_probability': float(probability[0])
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy', 
        'model_loaded': model is not None,
        'features_loaded': len(feature_names) > 0
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    