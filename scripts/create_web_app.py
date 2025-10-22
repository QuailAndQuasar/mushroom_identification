#!/usr/bin/env python3
"""
Create Web Application for Mushroom Identification

This script creates a user-friendly web interface for mushroom classification.
"""

from pathlib import Path

def create_html_interface():
    """Create an HTML interface for mushroom identification."""
    html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍄 Mushroom Identifier</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }
        select, input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
        }
        .button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: transform 0.2s;
        }
        .button:hover {
            transform: translateY(-2px);
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .edible {
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }
        .poisonous {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }
        .confidence {
            font-size: 14px;
            margin-top: 10px;
            opacity: 0.8;
        }
        .warning {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            border: 1px solid #ffeaa7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍄 Mushroom Identifier</h1>
        <p style="text-align: center; color: #666; margin-bottom: 30px;">
            Identify if a mushroom is edible or poisonous based on its characteristics
        </p>
        
        <form id="mushroomForm">
            <div class="form-group">
                <label for="cap-shape">Cap Shape:</label>
                <select id="cap-shape" name="cap-shape">
                    <option value="">Select cap shape...</option>
                    <option value="b">Bell</option>
                    <option value="c">Conical</option>
                    <option value="f">Flat</option>
                    <option value="k">Knobbed</option>
                    <option value="s">Sunken</option>
                    <option value="x">Convex</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="cap-surface">Cap Surface:</label>
                <select id="cap-surface" name="cap-surface">
                    <option value="">Select cap surface...</option>
                    <option value="f">Fibrous</option>
                    <option value="g">Grooves</option>
                    <option value="s">Smooth</option>
                    <option value="y">Scaly</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="cap-color">Cap Color:</label>
                <select id="cap-color" name="cap-color">
                    <option value="">Select cap color...</option>
                    <option value="b">Buff</option>
                    <option value="c">Cinnamon</option>
                    <option value="e">Red</option>
                    <option value="g">Gray</option>
                    <option value="n">Brown</option>
                    <option value="p">Pink</option>
                    <option value="r">Green</option>
                    <option value="u">Purple</option>
                    <option value="w">White</option>
                    <option value="y">Yellow</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="bruises">Bruises:</label>
                <select id="bruises" name="bruises">
                    <option value="">Select bruising...</option>
                    <option value="f">No</option>
                    <option value="t">Yes</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="odor">Odor:</label>
                <select id="odor" name="odor">
                    <option value="">Select odor...</option>
                    <option value="a">Almond</option>
                    <option value="c">Creosote</option>
                    <option value="f">Foul</option>
                    <option value="l">Anise</option>
                    <option value="m">Musty</option>
                    <option value="n">None</option>
                    <option value="p">Pungent</option>
                    <option value="s">Spicy</option>
                    <option value="y">Fishy</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="gill-size">Gill Size:</label>
                <select id="gill-size" name="gill-size">
                    <option value="">Select gill size...</option>
                    <option value="b">Broad</option>
                    <option value="n">Narrow</option>
                </select>
            </div>
            
            <button type="submit" class="button">🔍 Identify Mushroom</button>
        </form>
        
        <div id="result" style="display: none;"></div>
        
        <div class="warning">
            <strong>⚠️ Important:</strong> This tool is for educational purposes only. 
            Never rely solely on automated identification for mushroom consumption. 
            Always consult with expert mycologists before consuming any wild mushrooms.
        </div>
    </div>

    <script>
        document.getElementById('mushroomForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const features = {};
            
            // Convert form data to feature format
            for (let [key, value] of formData.entries()) {
                if (value) {
                    features[key + '_' + value] = true;
                }
            }
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(features)
                });
                
                const result = await response.json();
                displayResult(result);
            } catch (error) {
                console.error('Error:', error);
                displayResult({error: 'Failed to get prediction'});
            }
        });
        
        function displayResult(result) {
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            
            if (result.error) {
                resultDiv.innerHTML = `
                    <div class="result" style="background: #f8d7da; color: #721c24;">
                        ❌ Error: ${result.error}
                    </div>
                `;
                return;
            }
            
            const isEdible = result.edible;
            const confidence = (result.confidence * 100).toFixed(1);
            
            resultDiv.innerHTML = `
                <div class="result ${isEdible ? 'edible' : 'poisonous'}">
                    ${isEdible ? '✅ EDIBLE' : '☠️ POISONOUS'}
                    <div class="confidence">
                        Confidence: ${confidence}%
                    </div>
                </div>
            `;
        }
    </script>
</body>
</html>
    '''
    
    html_file = Path("mushroom_identifier.html")
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"🌐 HTML Interface created: {html_file}")
    return html_file

def create_flask_app():
    """Create a Flask web application."""
    flask_code = '''
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
    '''
    
    flask_file = Path("mushroom_app.py")
    with open(flask_file, 'w') as f:
        f.write(flask_code)
    
    print(f"🐍 Flask App created: {flask_file}")
    return flask_file

def create_requirements():
    """Create requirements file for deployment."""
    requirements = '''
flask==2.3.3
pandas==2.0.3
scikit-learn==1.3.0
numpy==1.24.3
joblib==1.3.2
gunicorn==21.2.0
    '''
    
    req_file = Path("requirements.txt")
    with open(req_file, 'w') as f:
        f.write(requirements)
    
    print(f"📦 Requirements file created: {req_file}")

def create_dockerfile():
    """Create Dockerfile for containerization."""
    dockerfile = '''
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "mushroom_app:app"]
    '''
    
    docker_file = Path("Dockerfile")
    with open(docker_file, 'w') as f:
        f.write(dockerfile)
    
    print(f"🐳 Dockerfile created: {docker_file}")

def create_deployment_guide():
    """Create deployment guide."""
    guide = '''
# 🍄 Mushroom Identifier - Deployment Guide

## Local Development

1. **Train the model:**
   ```bash
   python scripts/create_ml_model.py
   ```

2. **Run the web app:**
   ```bash
   python mushroom_app.py
   ```

3. **Open browser:**
   ```
   http://localhost:5000
   ```

## Cloud Deployment

### Heroku
1. Create `Procfile`:
   ```
   web: gunicorn mushroom_app:app
   ```

2. Deploy:
   ```bash
   git add .
   git commit -m "Deploy mushroom app"
   git push heroku main
   ```

### AWS/GCP/Azure
1. Use Docker:
   ```bash
   docker build -t mushroom-app .
   docker run -p 5000:5000 mushroom-app
   ```

2. Or use cloud services:
   - AWS: Elastic Beanstalk, ECS, or Lambda
   - GCP: Cloud Run or App Engine
   - Azure: Container Instances or App Service

## Mobile App Integration

### React Native
```javascript
const predictMushroom = async (features) => {
  const response = await fetch('https://your-api.com/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(features)
  });
  return await response.json();
};
```

### Flutter
```dart
Future<Map<String, dynamic>> predictMushroom(Map<String, dynamic> features) async {
  final response = await http.post(
    Uri.parse('https://your-api.com/predict'),
    headers: {'Content-Type': 'application/json'},
    body: json.encode(features),
  );
  return json.decode(response.body);
}
```

## API Usage

### cURL Example
```bash
curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "cap-shape_b": true,
    "odor_n": true,
    "bruises_t": true
  }'
```

### Python Example
```python
import requests

response = requests.post('http://localhost:5000/predict', json={
    'cap-shape_b': True,
    'odor_n': True,
    'bruises_t': True
})

result = response.json()
print(f"Edible: {result['edible']}")
print(f"Confidence: {result['confidence']}")
```

## Production Considerations

1. **Security**: Add authentication, rate limiting
2. **Monitoring**: Add logging, health checks
3. **Scaling**: Use load balancers, auto-scaling
4. **Data**: Consider model versioning, A/B testing
    '''
    
    guide_file = Path("DEPLOYMENT.md")
    with open(guide_file, 'w') as f:
        f.write(guide)
    
    print(f"📖 Deployment guide created: {guide_file}")

def main():
    """Create web application components."""
    print("🌐 CREATING WEB APPLICATION")
    print("=" * 50)
    
    # Create components
    html_file = create_html_interface()
    flask_file = create_flask_app()
    create_requirements()
    create_dockerfile()
    create_deployment_guide()
    
    print("\n🎉 Web Application Created!")
    print("=" * 40)
    print("📁 Files created:")
    print("   - mushroom_identifier.html (Frontend)")
    print("   - mushroom_app.py (Backend)")
    print("   - requirements.txt (Dependencies)")
    print("   - Dockerfile (Containerization)")
    print("   - DEPLOYMENT.md (Deployment guide)")
    
    print("\n🚀 Next steps:")
    print("1. Train model: python scripts/create_ml_model.py")
    print("2. Run app: python mushroom_app.py")
    print("3. Open: http://localhost:5000")
    print("4. Deploy to cloud for production use")

if __name__ == "__main__":
    main()
