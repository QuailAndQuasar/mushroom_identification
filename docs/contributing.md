# Contributing Guide

Thank you for your interest in contributing to the Mushroom ETL Pipeline! This guide will help you get started with contributing to the project.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Code of Conduct](#code-of-conduct)

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Virtual environment (venv)
- Basic understanding of ETL concepts
- Familiarity with pandas, scikit-learn, and SQLAlchemy

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/mushroom_etl_project.git
   cd mushroom_etl_project
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/mushroom_etl_project.git
   ```

## Development Setup

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install
```

### 2. Project Structure

```
mushroom_etl_project/
├── src/                     # Source code
│   ├── extract/            # Data extraction
│   ├── transform/          # Data transformation
│   ├── load/               # Data loading
│   ├── orchestration/      # ETL orchestration
│   └── utils/              # Utilities
├── tests/                  # Test suite
├── docs/                   # Documentation
├── scripts/                # Standalone scripts
├── config/                 # Configuration files
├── data/                   # Data storage
└── logs/                   # Log files
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
vim .env

# Test configuration
python scripts/validate_setup.py
```

## Code Style

### 1. Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Good
def process_data(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """Process data according to configuration.
    
    Args:
        data: Input DataFrame
        config: Processing configuration
        
    Returns:
        Processed DataFrame
    """
    # Implementation here
    return processed_data

# Bad
def process_data(data,config):
    # Implementation here
    return processed_data
```

### 2. Naming Conventions

- **Variables**: `snake_case` (e.g., `user_name`, `data_frame`)
- **Functions**: `snake_case` (e.g., `process_data`, `validate_input`)
- **Classes**: `PascalCase` (e.g., `DataCleaner`, `FeatureEngineer`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_BATCH_SIZE`, `DEFAULT_TIMEOUT`)
- **Private methods**: `_snake_case` (e.g., `_validate_config`)

### 3. Documentation

```python
def extract_data(source: str, config: Optional[Dict] = None) -> pd.DataFrame:
    """Extract data from specified source.
    
    Args:
        source: Data source identifier
        config: Optional configuration dictionary
        
    Returns:
        Extracted DataFrame
        
    Raises:
        ValueError: If source is invalid
        ConnectionError: If connection fails
        
    Example:
        >>> data = extract_data('uci_mushroom')
        >>> print(data.shape)
        (8124, 23)
    """
    # Implementation here
    pass
```

### 4. Type Hints

```python
from typing import Dict, List, Optional, Union
import pandas as pd

def process_data(
    data: pd.DataFrame,
    config: Optional[Dict[str, Union[str, int, bool]]] = None
) -> pd.DataFrame:
    """Process data with optional configuration."""
    # Implementation here
    pass
```

## Testing

### 1. Test Structure

```python
# tests/test_extract/test_uci_mushroom_extractor.py
import pytest
import pandas as pd
from unittest.mock import Mock, patch
from src.extract.uci_mushroom_extractor import UCIMushroomExtractor

class TestUCIMushroomExtractor:
    """Test UCI Mushroom Extractor."""
    
    def test_initialization(self):
        """Test extractor initialization."""
        extractor = UCIMushroomExtractor()
        assert extractor.name == "uci_mushroom"
        assert extractor.config is not None
    
    def test_extract_success(self):
        """Test successful data extraction."""
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = "e,x,s,n,t,p,f,c,n,k,e,e,s,s,w,w,p,w,o,p,k,s,u\n"
            
            extractor = UCIMushroomExtractor()
            result = extractor.extract()
            
            assert isinstance(result, pd.DataFrame)
            assert not result.empty
    
    def test_extract_failure(self):
        """Test extraction failure handling."""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Connection failed")
            
            extractor = UCIMushroomExtractor()
            
            with pytest.raises(Exception):
                extractor.extract()
```

### 2. Running Tests

```bash
# Run all tests
python scripts/run_tests.py

# Run specific test file
python -m pytest tests/test_extract/test_uci_mushroom_extractor.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test
python -m pytest tests/test_extract/test_uci_mushroom_extractor.py::TestUCIMushroomExtractor::test_extract_success -v
```

### 3. Test Coverage

- **Minimum coverage**: 80%
- **Target coverage**: 90%
- **Critical components**: 95%

```bash
# Check coverage
python -m pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### 4. Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: Component integration testing
- **End-to-End Tests**: Complete pipeline testing
- **Performance Tests**: Pipeline performance testing
- **Error Tests**: Error handling and recovery testing

## Documentation

### 1. Code Documentation

```python
class DataCleaner(BaseTransformer):
    """Data cleaning transformer for ETL pipeline.
    
    This transformer handles data cleaning operations including:
    - Missing value handling
    - Duplicate removal
    - Outlier detection
    - Text standardization
    
    Attributes:
        name: Transformer name
        config: Configuration dictionary
        stats: Processing statistics
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize DataCleaner.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__("data_cleaner", config)
        self.config = config or {}
```

### 2. API Documentation

```python
def extract_data(source: str, config: Optional[Dict] = None) -> pd.DataFrame:
    """Extract data from specified source.
    
    This function extracts data from various sources including:
    - UCI ML Repository
    - Local files
    - REST APIs
    
    Args:
        source: Data source identifier
        config: Optional configuration dictionary
        
    Returns:
        Extracted DataFrame
        
    Raises:
        ValueError: If source is invalid
        ConnectionError: If connection fails
        
    Example:
        >>> data = extract_data('uci_mushroom')
        >>> print(data.shape)
        (8124, 23)
    """
    # Implementation here
    pass
```

### 3. README Updates

When adding new features:

1. **Update README.md** with new functionality
2. **Add examples** showing how to use new features
3. **Update configuration** documentation
4. **Add troubleshooting** information if needed

### 4. Documentation Standards

- **Clear and concise** descriptions
- **Code examples** for all public methods
- **Type hints** for all parameters and returns
- **Error handling** documentation
- **Usage examples** in docstrings

## Pull Request Process

### 1. Before Submitting

```bash
# Ensure all tests pass
python scripts/run_tests.py

# Check code style
black src/ tests/
flake8 src/ tests/

# Check type hints
mypy src/

# Update documentation
# Edit relevant .md files in docs/
```

### 2. Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Documentation
- [ ] Code documentation updated
- [ ] README updated
- [ ] API documentation updated
- [ ] Configuration documentation updated

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] No breaking changes
- [ ] Performance impact considered
```

### 3. Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation** review
5. **Performance** impact assessment

### 4. Merge Requirements

- **All tests** must pass
- **Code review** approval
- **Documentation** updated
- **No conflicts** with main branch
- **Performance** benchmarks met

## Issue Reporting

### 1. Bug Reports

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: macOS 11.7
- Python: 3.10.0
- Dependencies: (list versions)

**Additional Context**
Any other relevant information
```

### 2. Feature Requests

```markdown
**Feature Description**
Clear description of the feature

**Use Case**
Why this feature is needed

**Proposed Solution**
How you think it should work

**Alternatives**
Other solutions considered

**Additional Context**
Any other relevant information
```

### 3. Issue Labels

- **bug**: Something isn't working
- **enhancement**: New feature or request
- **documentation**: Improvements to documentation
- **good first issue**: Good for newcomers
- **help wanted**: Extra attention needed
- **question**: Further information requested

## Code of Conduct

### 1. Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### 2. Expected Behavior

- **Respectful** communication
- **Constructive** feedback
- **Collaborative** approach
- **Professional** conduct

### 3. Unacceptable Behavior

- **Harassment** of any kind
- **Discriminatory** language
- **Personal attacks**
- **Trolling** or inflammatory comments

### 4. Reporting

If you experience or witness unacceptable behavior:

1. **Contact** project maintainers
2. **Provide** specific details
3. **Include** relevant evidence
4. **Expect** prompt response

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/new-extractor

# Make changes
# Add tests
# Update documentation

# Commit changes
git add .
git commit -m "feat: add new data extractor"

# Push branch
git push origin feature/new-extractor

# Create pull request
```

### 2. Bug Fixes

```bash
# Create bugfix branch
git checkout -b bugfix/fix-memory-leak

# Fix the bug
# Add regression test
# Update documentation

# Commit changes
git add .
git commit -m "fix: resolve memory leak in data loader"

# Push branch
git push origin bugfix/fix-memory-leak

# Create pull request
```

### 3. Documentation Updates

```bash
# Create docs branch
git checkout -b docs/update-api-reference

# Update documentation
# Add examples
# Fix typos

# Commit changes
git add .
git commit -m "docs: update API reference with examples"

# Push branch
git push origin docs/update-api-reference

# Create pull request
```

## Getting Help

### 1. Documentation

- **README.md**: Project overview and quick start
- **API Reference**: Complete API documentation
- **Configuration Guide**: Configuration options
- **Troubleshooting**: Common issues and solutions

### 2. Community

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Code Review**: Learn from others' contributions

### 3. Contact

- **Maintainers**: @maintainer-username
- **Email**: maintainer@example.com
- **Discord**: [Community Discord Server]

## Recognition

### 1. Contributors

We recognize all contributors in our README and release notes.

### 2. Special Recognition

- **Major contributors** get special mention
- **First-time contributors** are celebrated
- **Long-term contributors** receive recognition

### 3. Contribution Types

- **Code contributions**
- **Documentation improvements**
- **Bug reports**
- **Feature requests**
- **Community support**

Thank you for contributing to the Mushroom ETL Pipeline! 🍄
