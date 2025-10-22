
from flask import Flask, request, jsonify
import pandas as pd
import joblib
from pathlib import Path

app = Flask(__name__)

# Load the trained model
model_path = Path("models/random_forest.joblib")
if model_path.exists():
    model = joblib.load(model_path)
    print("✅ Model loaded successfully")
else:
    print("❌ Model not found. Train the model first!")
    model = None

@app.route('/predict', methods=['POST'])
def predict_mushroom():
    """API endpoint for mushroom classification."""
    try:
        # Get features from request
        features = request.json
        
        # Convert to DataFrame
        features_df = pd.DataFrame([features])
        
        # Make prediction
        if model is not None:
            prediction = model.predict(features_df)[0]
            probability = model.predict_proba(features_df)[0]
            
            result = {
                'edible': bool(prediction),
                'confidence': float(max(probability)),
                'edible_probability': float(probability[1]),
                'poisonous_probability': float(probability[0])
            }
        else:
            result = {'error': 'Model not available'}
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    