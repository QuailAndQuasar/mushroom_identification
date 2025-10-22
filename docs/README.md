# Mushroom ETL Pipeline

A comprehensive ETL (Extract, Transform, Load) pipeline for mushroom classification data, demonstrating modern data engineering practices.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (venv)
- Git

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd mushroom_etl_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration
```

### Running the Pipeline
```bash
# Run complete ETL pipeline
python scripts/run_etl.py

# Run specific stages
python scripts/run_extraction.py
python scripts/run_transformation.py
python scripts/run_loading.py
```

## 📊 Project Overview

This project demonstrates:
- **Data Extraction**: Multiple data sources (UCI dataset, files, APIs)
- **Data Transformation**: Cleaning, validation, feature engineering
- **Data Loading**: Database and file storage
- **ETL Orchestration**: Complete pipeline coordination
- **Testing**: Comprehensive test coverage
- **Monitoring**: Performance and quality tracking

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Extraction    │    │ Transformation  │    │     Loading     │
│                 │    │                 │    │                 │
│ • UCI Dataset   │───▶│ • Data Cleaning │───▶│ • Database      │
│ • File Sources  │    │ • Feature Eng.  │    │ • File Storage  │
│ • API Sources   │    │ • Validation    │    │ • Quality Check │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
mushroom_etl_project/
├── data/                    # Data storage
│   ├── raw/                 # Raw data
│   ├── processed/           # Processed data
│   └── models/              # ML models
├── src/                     # Source code
│   ├── extract/             # Data extraction
│   ├── transform/           # Data transformation
│   ├── load/                # Data loading
│   ├── orchestration/       # ETL orchestration
│   └── utils/               # Utilities
├── tests/                   # Test suite
├── notebooks/               # Jupyter notebooks
├── config/                  # Configuration files
├── scripts/                 # Standalone scripts
└── docs/                    # Documentation
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python scripts/run_tests.py

# Run specific test categories
python -m pytest tests/test_extract/ -v
python -m pytest tests/test_transform/ -v
python -m pytest tests/test_load/ -v
python -m pytest tests/test_integration/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component integration testing
- **End-to-End Tests**: Complete pipeline testing
- **Error Scenario Tests**: Failure case testing
- **Performance Tests**: Pipeline performance testing

## 📈 Monitoring

### Pipeline Health
```bash
# Check pipeline health
python scripts/check_pipeline_health.py

# View pipeline statistics
python scripts/view_pipeline_stats.py
```

### Logs
```bash
# View pipeline logs
tail -f logs/etl_pipeline.log

# View specific stage logs
grep "extraction" logs/etl_pipeline.log
```

## 🚀 Deployment

### Development
```bash
# Run in development mode
python scripts/run_complete_etl.py --mode development
```

### Production
```bash
# Run in production mode
python scripts/run_complete_etl.py --mode production
```

### Docker (Optional)
```bash
# Build Docker image
docker build -t mushroom-etl .

# Run with Docker
docker run -v $(pwd)/data:/app/data mushroom-etl
```

## 🔧 Maintenance

### Data Management
```bash
# Clean old data
python scripts/cleanup_data.py

# Backup data
python scripts/backup_data.py
```

### Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python scripts/migrate.py
```

## 📚 Documentation

- [API Reference](api_reference.md) - Complete API documentation for all classes and methods
- [Configuration Guide](configuration.md) - Comprehensive configuration options and examples
- [Deployment Guide](deployment.md) - Production deployment and monitoring
- [Troubleshooting](troubleshooting.md) - Common issues and solutions
- [Contributing](contributing.md) - How to contribute to the project

## 🔧 Quick Reference

### Configuration Files
- `config/pipeline.yaml` - Pipeline configuration
- `config/database.yaml` - Database configuration
- `.env` - Environment variables (copy from `.env.example`)

### Key Scripts
- `scripts/run_complete_etl.py` - Run complete ETL pipeline
- `scripts/validate_setup.py` - Validate project setup
- `scripts/run_tests.py` - Run test suite
- `scripts/setup_project.py` - Automated project setup

### Data Flow
```
Raw Data → Extraction → Transformation → Loading → Processed Data
    ↓           ↓            ↓           ↓           ↓
  Files    DataFrames   Clean Data   Database    Analytics
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- UCI ML Repository for the mushroom dataset
- Python data science community
- Open source contributors
