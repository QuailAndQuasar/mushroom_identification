
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
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
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
    