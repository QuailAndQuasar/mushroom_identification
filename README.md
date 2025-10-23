# 🍄 Mushroom Identification Project

A complete machine learning pipeline for mushroom classification with web interface, species identification, and production deployment capabilities.

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone <repository-url>
cd mushroom_identification
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-compatible.txt
```

### 2. Run the Complete Pipeline
```bash
# Process data and train model
python scripts/run_complete_etl.py
python scripts/create_ml_model.py

# Start web application
python mushroom_app_enhanced.py
```

### 3. Access the Application
- **Web Interface**: http://localhost:5001
- **API Health**: http://localhost:5001/health
- **Species Database**: http://localhost:5001/species

## 🎯 What This Project Does

### Core Features
- **🍄 Mushroom Classification**: Binary classification (edible vs poisonous)
- **🔍 Species Identification**: Identifies specific mushroom species when edible
- **🌐 Web Interface**: User-friendly web application
- **📊 Data Pipeline**: Complete ETL pipeline with data processing
- **🤖 Machine Learning**: Multiple ML models (Random Forest, Logistic Regression, SVM)
- **📱 Mobile Ready**: React Native and Flutter mobile apps
- **🚀 Production Ready**: Docker, Kubernetes, CI/CD deployment

### Data Science Pipeline
1. **Data Extraction**: UCI Mushroom Dataset processing
2. **Feature Engineering**: One-hot encoding, scaling, selection
3. **Model Training**: Multiple algorithms with evaluation
4. **Model Selection**: Best performing model (Random Forest)
5. **Production Deployment**: Web API and user interface

## 📁 Project Structure

```
mushroom_identification/
├── 🍄 Core Application
│   ├── mushroom_app_enhanced.py      # Main Flask web app
│   ├── templates/mushroom_identifier.html  # Web interface
│   └── data/mushroom_species.json    # Species database
├── 🤖 Machine Learning
│   ├── models/random_forest.joblib  # Trained ML model
│   ├── scripts/create_ml_model.py   # Model training
│   └── scripts/explore_mushroom_data.py  # Data analysis
├── 🔧 Data Pipeline
│   ├── src/                         # ETL pipeline modules
│   ├── scripts/run_complete_etl.py  # Complete pipeline
│   └── data/processed/loaded_data.csv  # Processed dataset
├── 📱 Mobile Apps
│   ├── mobile_app/                  # React Native & Flutter
│   └── deploy_mobile.sh            # Mobile deployment
├── 🚀 Production
│   ├── docker-compose.yml          # Container orchestration
│   ├── k8s-deployment.yaml         # Kubernetes deployment
│   └── terraform/                  # AWS infrastructure
└── 🧪 Testing & AI
    ├── tests/                      # Comprehensive test suite
    └── scripts/ai_agents.py        # AI development tools
```

## 🛠️ Available Scripts

### Data & ML Scripts
```bash
# Complete ETL pipeline
python scripts/run_complete_etl.py

# Train ML models
python scripts/create_ml_model.py

# Explore data
python scripts/explore_mushroom_data.py
python scripts/show_data_summary.py
python scripts/query_mushroom_data.py
```

### Web Application
```bash
# Start enhanced web app (with species identification)
python mushroom_app_enhanced.py

# Start basic web app
python mushroom_app.py

# API testing
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"cap-shape": "x", "odor": "n", "bruises": "t"}'
```

### Development & Testing
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# AI development tools
python scripts/ai_agents.py
python scripts/ai_enhancements.py
```

## 🌐 Web Application Features

### User Interface
- **Interactive Form**: Select mushroom characteristics
- **Real-time Prediction**: Instant edible/poisonous classification
- **Species Identification**: Shows specific mushroom species when edible
- **Confidence Scores**: Displays prediction confidence
- **Responsive Design**: Works on desktop and mobile

### API Endpoints
- `GET /` - Main web interface
- `POST /predict` - Classification API
- `GET /health` - Health check
- `GET /species` - Species database

### Example API Usage
```bash
# Classify a mushroom
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cap-shape": "x",
    "cap-surface": "s", 
    "cap-color": "n",
    "bruises": "t",
    "odor": "n",
    "gill-attachment": "f",
    "gill-spacing": "c",
    "gill-size": "n",
    "gill-color": "k",
    "stalk-shape": "e",
    "stalk-root": "e",
    "stalk-surface-above-ring": "s",
    "stalk-surface-below-ring": "s",
    "stalk-color-above-ring": "w",
    "stalk-color-below-ring": "w",
    "veil-type": "p",
    "veil-color": "w",
    "ring-number": "o",
    "ring-type": "p",
    "spore-print-color": "n",
    "population": "v",
    "habitat": "d"
  }'
```

## 🤖 Machine Learning Details

### Models Trained
- **Random Forest**: 100% accuracy (selected for production)
- **Logistic Regression**: 100% accuracy
- **Support Vector Machine**: 100% accuracy

### Features
- **117 Features**: One-hot encoded from 22 original attributes
- **Binary Classification**: Edible (e) vs Poisonous (p)
- **Feature Engineering**: Scaling, selection, validation

### Model Performance
```
Random Forest Results:
- Accuracy: 100%
- Precision: 100% (Edible), 100% (Poisonous)
- Recall: 100% (Edible), 100% (Poisonous)
- F1-Score: 100% (Edible), 100% (Poisonous)
```

## 📱 Mobile Applications

### React Native
```bash
cd mobile_app
npm install
npx react-native run-ios  # or run-android
```

### Flutter
```bash
cd mobile_app
flutter pub get
flutter run
```

## 🚀 Production Deployment

### Docker
```bash
# Build and run
docker-compose up -d

# Scale services
docker-compose up --scale web=3
```

### Kubernetes
```bash
# Deploy to Kubernetes
kubectl apply -f k8s-deployment.yaml
```

### AWS (Terraform)
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## 🧪 Testing

### Test Coverage
- **Core Functionality**: All essential components tested
- **Error Handling**: Failure scenarios covered
- **Data Validation**: Quality checks implemented
- **Mock Testing**: External dependencies isolated

### Running Tests
```bash
# All tests
python -m pytest tests/ -v

# Specific component
python -m pytest tests/test_extract/ -v

# With coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

## 🤖 AI-Powered Development

### AI Agents
- **Code Generation**: Automated code creation
- **Testing**: AI-generated test suites
- **Monitoring**: System health analysis
- **Optimization**: Performance improvements

### AI Codexes
- **Architecture Understanding**: Codebase analysis
- **Dependency Mapping**: Component relationships
- **Documentation**: Auto-generated docs
- **Pattern Recognition**: Code quality analysis

## 📊 Data Flow

```
Raw Data (UCI Dataset)
    ↓
ETL Pipeline (src/)
    ↓
Processed Data (data/processed/)
    ↓
ML Training (scripts/create_ml_model.py)
    ↓
Trained Model (models/random_forest.joblib)
    ↓
Web Application (mushroom_app_enhanced.py)
    ↓
User Interface (templates/mushroom_identifier.html)
```

## 🔧 Troubleshooting

### Common Issues
1. **Port conflicts**: Use different ports (5001 instead of 5000)
2. **Dependencies**: Use `requirements-compatible.txt` for Python 3.13
3. **Model loading**: Ensure `models/random_forest.joblib` exists
4. **Data files**: Run ETL pipeline first

### Validation
```bash
# Check setup
python scripts/validate_setup.py

# Verify data
python scripts/show_data_summary.py

# Test API
curl http://localhost:5001/health
```

## 📚 Documentation

- **API Documentation**: Available at `/health` endpoint
- **Deployment Guide**: `DEPLOYMENT.md`
- **Mobile Integration**: `MOBILE_INTEGRATION.md`
- **Production Guide**: `PRODUCTION_DEPLOYMENT.md`

## 🎯 Use Cases

### Educational
- Learn machine learning fundamentals
- Understand ETL pipelines
- Practice web development
- Explore data science workflows

### Professional
- Production-ready ML application
- Full-stack development example
- DevOps and deployment practices
- AI-powered development tools

### Research
- Mushroom classification research
- ML model comparison
- Feature engineering techniques
- Species identification algorithms

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and test: `python -m pytest tests/`
4. Commit with conventional format: `feat(scope): description`
5. Push and create pull request

## 📄 License

This project is for educational and research purposes. Please ensure responsible use of mushroom identification information.

---

**🚀 Ready to identify mushrooms? Start with `python mushroom_app_enhanced.py` and visit http://localhost:5001!**