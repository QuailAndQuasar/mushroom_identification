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

## Git Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Individual feature development
- `release/*`: Release preparation
- `hotfix/*`: Critical bug fixes

### Development Process
1. **Create feature branch**: `git checkout -b feature/your-feature-name`
2. **Make changes**: Develop your feature
3. **Test changes**: Run tests and validation
4. **Commit changes**: Use conventional commit messages
5. **Push branch**: `git push origin feature/your-feature-name`
6. **Create PR**: Pull request to develop branch
7. **Review**: Code review and approval
8. **Merge**: Merge to develop, then to main

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

**Types**: feat, fix, docs, style, refactor, test, chore
**Scope**: component affected (e.g., config, extract, transform, load)
**Description**: clear, concise description

### Examples
- `feat(extract): add API data extractor`
- `fix(transform): resolve data type conversion issue`
- `docs(readme): update setup instructions`
- `test(load): add database loading tests`

## Testing

This project includes comprehensive tests for all ETL pipeline components. The test suite focuses on core functionality without bloat.

### Test Structure

```
tests/
├── conftest.py                    # Test configuration and fixtures
├── test_extract/                  # Data extraction tests
│   ├── test_base_extractor.py     # Base extractor interface tests
│   ├── test_uci_mushroom_extractor.py  # UCI dataset extractor tests
│   ├── test_file_extractor.py     # File-based extractor tests
│   ├── test_api_extractor.py      # API extractor tests
│   └── test_extraction_orchestrator.py  # Orchestrator tests
├── test_transform/                # Data transformation tests (coming soon)
├── test_load/                     # Data loading tests (coming soon)
└── test_integration/              # End-to-end integration tests (coming soon)
```

### Running Tests

#### Quick Test Run
```bash
# Run all tests
python scripts/run_tests.py

# Run specific test file
python -m pytest tests/test_extract/test_base_extractor.py -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

#### Test Categories

| Test Type | Command | Purpose |
|-----------|---------|---------|
| **All Tests** | `python scripts/run_tests.py` | Run complete test suite with coverage |
| **Extraction Tests** | `python -m pytest tests/test_extract/ -v` | Test data extraction components |
| **Specific File** | `python -m pytest tests/test_extract/test_uci_mushroom_extractor.py -v` | Test specific component |
| **Coverage Report** | `python -m pytest tests/ --cov=src --cov-report=html` | Generate HTML coverage report |

#### Test Coverage

The test suite covers:
- ✅ **Core Functionality**: All essential extractor behaviors
- ✅ **Error Handling**: Failure scenarios and edge cases  
- ✅ **Data Validation**: Quality checks for extracted data
- ✅ **Mock Testing**: External dependencies properly isolated
- ✅ **Integration**: Orchestrator coordination testing

#### Test Development

When adding new tests:

1. **Follow Naming Convention**: `test_<component>_<functionality>.py`
2. **Use Fixtures**: Leverage `conftest.py` for reusable test data
3. **Mock External Dependencies**: Use `unittest.mock` for HTTP requests, file I/O
4. **Test Edge Cases**: Empty data, missing files, network errors
5. **Keep Tests Focused**: One concept per test, clear assertions

#### Example Test Structure

```python
class TestComponentName:
    """Test component functionality."""
    
    def test_initialization(self):
        """Test component initialization."""
        # Test setup and configuration
        
    def test_success_case(self):
        """Test successful operation."""
        # Test happy path
        
    def test_error_handling(self):
        """Test error scenarios."""
        # Test failure cases
```

### Test Troubleshooting

If tests fail:

1. **Check Dependencies**: Ensure all test packages are installed
   ```bash
   pip install pytest pytest-cov
   ```

2. **Verify Environment**: Run validation script
   ```bash
   python scripts/validate_setup.py
   ```

3. **Check Test Files**: Ensure test files are in correct directories
   ```bash
   find tests/ -name "*.py" -type f
   ```

4. **Run Individual Tests**: Isolate failing tests
   ```bash
   python -m pytest tests/test_extract/test_base_extractor.py::TestBaseExtractor::test_initialization -v
   ```

## Development

- **Run tests**: `python scripts/run_tests.py`
- **Run ETL pipeline**: `python scripts/run_etl.py`
- **Start Jupyter**: `jupyter lab`
- **Validate setup**: `python scripts/validate_setup.py`

## Project Status

### ✅ Completed Foundation (Steps 1.1-1.5)
- **Project Structure**: Complete directory organization
- **Dependencies**: All required packages installed and validated
- **Configuration**: Pydantic-based configuration management
- **Environment Variables**: Secure handling of sensitive data
- **Logging**: Centralized logging system
- **Git Integration**: Version control with quality hooks
- **Documentation**: Complete setup and usage instructions

### 🚧 Next Steps (Step 2+)
- **Data Extraction**: Build extractors for multiple data sources
- **Data Transformation**: Implement cleaning and feature engineering
- **Data Loading**: Create loading modules for different targets
- **Machine Learning**: Build classification models
- **ETL Orchestration**: Complete pipeline automation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
