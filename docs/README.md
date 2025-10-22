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
