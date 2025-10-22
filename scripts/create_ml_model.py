#!/usr/bin/env python3
"""
Create Machine Learning Model for Mushroom Classification

This script demonstrates how to build a practical ML model for mushroom identification.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data():
    """Load and prepare the mushroom dataset."""
    print("🍄 Loading Mushroom Dataset for ML...")
    
    # Load data
    df = pd.read_csv('data/processed/loaded_data.csv')
    print(f"✅ Loaded {len(df):,} mushrooms with {len(df.columns)} features")
    
    # Separate features and target
    X = df.drop('class', axis=1)
    y = df['class']
    
    # Convert target to binary (0 = poisonous, 1 = edible)
    y_binary = (y == 'e').astype(int)
    
    print(f"📊 Features: {X.shape[1]}")
    print(f"🎯 Target distribution: {y.value_counts().to_dict()}")
    
    return X, y_binary, y

def train_models(X, y):
    """Train multiple ML models."""
    print("\n🤖 Training Machine Learning Models...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📊 Training set: {len(X_train):,} samples")
    print(f"📊 Test set: {len(X_test):,} samples")
    
    # Initialize models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'SVM': SVC(random_state=42, probability=True)
    }
    
    results = {}
    
    for name, model in models.items():
        print(f"\n🔧 Training {name}...")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
        
        print(f"✅ {name} Accuracy: {accuracy:.4f}")
    
    return results, X_test, y_test

def evaluate_models(results, X_test, y_test):
    """Evaluate and compare models."""
    print("\n📊 Model Evaluation Results:")
    print("=" * 50)
    
    best_model = None
    best_accuracy = 0
    
    for name, result in results.items():
        accuracy = result['accuracy']
        print(f"\n{name}:")
        print(f"  Accuracy: {accuracy:.4f}")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = name
    
    print(f"\n🏆 Best Model: {best_model} ({best_accuracy:.4f})")
    
    # Detailed evaluation of best model
    best_result = results[best_model]
    print(f"\n📋 Detailed Report for {best_model}:")
    print(classification_report(y_test, best_result['predictions'], 
                              target_names=['Poisonous', 'Edible']))
    
    return best_model, best_result

def save_model(model, model_name):
    """Save the trained model."""
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / f"{model_name.lower().replace(' ', '_')}.joblib"
    joblib.dump(model, model_path)
    
    print(f"💾 Model saved to: {model_path}")
    return model_path

def create_prediction_function(model, feature_names):
    """Create a practical prediction function."""
    def predict_mushroom(features_dict):
        """
        Predict if a mushroom is edible or poisonous.
        
        Args:
            features_dict: Dictionary with mushroom features
            Example: {
                'cap-shape_b': True,
                'odor_n': True,
                'bruises_t': True,
                ...
            }
        
        Returns:
            dict: Prediction results
        """
        # Convert to DataFrame
        features_df = pd.DataFrame([features_dict])
        
        # Ensure all features are present
        for feature in feature_names:
            if feature not in features_df.columns:
                features_df[feature] = False
        
        # Reorder columns to match training data
        features_df = features_df[feature_names]
        
        # Make prediction
        prediction = model.predict(features_df)[0]
        probability = model.predict_proba(features_df)[0]
        
        return {
            'edible': bool(prediction),
            'poisonous': not bool(prediction),
            'confidence': float(max(probability)),
            'edible_probability': float(probability[1]),
            'poisonous_probability': float(probability[0])
        }
    
    return predict_mushroom

def demonstrate_prediction(predict_func):
    """Demonstrate the prediction function."""
    print("\n🎯 Prediction Demonstration:")
    print("=" * 40)
    
    # Example 1: Safe mushroom (edible + no odor + bruises)
    safe_mushroom = {
        'cap-shape_b': True,    # Bell-shaped
        'odor_n': True,         # No odor
        'bruises_t': True,      # Bruises
        'gill-size_b': True,    # Broad gills
        'stalk-surface-above-ring_s': True  # Smooth stalk
    }
    
    result1 = predict_func(safe_mushroom)
    print(f"🍄 Safe Mushroom Prediction:")
    print(f"   Edible: {result1['edible']}")
    print(f"   Confidence: {result1['confidence']:.2f}")
    print(f"   Edible Probability: {result1['edible_probability']:.2f}")
    
    # Example 2: Dangerous mushroom (poisonous + foul odor)
    dangerous_mushroom = {
        'cap-shape_x': True,    # Convex
        'odor_f': True,         # Foul odor
        'bruises_f': True,      # No bruises
        'gill-size_n': True,    # Narrow gills
        'stalk-surface-above-ring_k': True  # Knobby stalk
    }
    
    result2 = predict_func(dangerous_mushroom)
    print(f"\n☠️ Dangerous Mushroom Prediction:")
    print(f"   Edible: {result2['edible']}")
    print(f"   Confidence: {result2['confidence']:.2f}")
    print(f"   Poisonous Probability: {result2['poisonous_probability']:.2f}")

def create_web_api():
    """Create a simple web API for mushroom classification."""
    api_code = '''
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
    '''
    
    api_file = Path("mushroom_api.py")
    with open(api_file, 'w') as f:
        f.write(api_code)
    
    print(f"🌐 Web API created: {api_file}")
    print("   Run with: python mushroom_api.py")
    print("   Test with: curl -X POST http://localhost:5000/predict -H 'Content-Type: application/json' -d '{\"cap-shape_b\": true, \"odor_n\": true}'")

def main():
    """Main function to create ML model."""
    print("🍄 MUSHROOM CLASSIFICATION MODEL")
    print("=" * 50)
    
    # Load and prepare data
    X, y_binary, y_original = load_and_prepare_data()
    
    # Train models
    results, X_test, y_test = train_models(X, y_binary)
    
    # Evaluate models
    best_model_name, best_result = evaluate_models(results, X_test, y_test)
    
    # Save the best model
    model_path = save_model(best_result['model'], best_model_name)
    
    # Create prediction function
    predict_func = create_prediction_function(best_result['model'], X.columns.tolist())
    
    # Demonstrate predictions
    demonstrate_prediction(predict_func)
    
    # Create web API
    create_web_api()
    
    print("\n🎉 Machine Learning Model Created!")
    print("=" * 40)
    print("📁 Files created:")
    print(f"   Model: {model_path}")
    print("   API: mushroom_api.py")
    print("\n🚀 Next steps:")
    print("   1. Test the model with: python mushroom_api.py")
    print("   2. Deploy to cloud (AWS, GCP, Azure)")
    print("   3. Create mobile app integration")
    print("   4. Build web interface for mushroom identification")

if __name__ == "__main__":
    main()
