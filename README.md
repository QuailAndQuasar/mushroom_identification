# Mushroom ETL Pipeline

A comprehensive ETL (Extract, Transform, Load) pipeline for mushroom classification data, demonstrating modern data engineering practices.

## Project Overview

This project demonstrates:
- Data extraction from multiple sources
- Data transformation and cleaning
- Feature engineering for machine learning
- Model training and evaluation
- ETL orchestration and monitoring

## Technology Stack

- **Language**: Python 3.10+
- **Core Libraries**: pandas, numpy, scikit-learn
- **Data Engineering**: SQLAlchemy, PyArrow
- **Testing**: pytest
- **Visualization**: matplotlib, seaborn

## Project Structure

```
mushroom_etl_project/
├── data/           # Data storage (raw, processed, models)
├── src/            # Source code modules
├── tests/          # Test suite
├── notebooks/      # Jupyter notebooks for exploration
├── config/         # Configuration files
└── scripts/        # Standalone scripts
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mushroom_etl_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Scripts

This project includes several utility scripts to help with development and maintenance:

### Setup Script (`scripts/setup_project.py`)
**When to use:** First time setup, after cloning the repository, or when dependencies change.

**What it does:**
- Installs all required dependencies from `requirements.txt`
- Optionally installs development dependencies
- Verifies that all packages can be imported
- Provides guidance for next steps

**How to use:**
```bash
# Make sure you're in your virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the setup script
python scripts/setup_project.py
```

### Validation Script (`scripts/validate_setup.py`)
**When to use:** When troubleshooting dependency issues, after environment changes, or to verify setup.

**What it does:**
- Checks that all required packages are installed
- Shows installed versions of key packages
- Tests basic functionality of core libraries
- Reports any missing packages or issues

**How to use:**
```bash
# Run validation to check current state
python scripts/validate_setup.py
```

### When to Use Each Script

| Script | Use Case | Frequency |
|--------|----------|-----------|
| `setup_project.py` | First setup, dependency changes | As needed |
| `validate_setup.py` | Troubleshooting, verification | Regularly |

### Troubleshooting

If you encounter issues:

1. **Run validation first:**
   ```bash
   python scripts/validate_setup.py
   ```

2. **Check your virtual environment:**
   ```bash
   which python  # Should show your venv path
   ```

3. **Reinstall dependencies:**
   ```bash
   python scripts/setup_project.py
   ```

4. **Check for conflicts:**
   ```bash
   pip list | grep -E "(pandas|numpy|sklearn)"
   ```

## Development

- **Run tests**: `pytest`
- **Run ETL pipeline**: `python scripts/run_etl.py`
- **Start Jupyter**: `jupyter lab`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
