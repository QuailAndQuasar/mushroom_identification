"""
Test configuration and fixtures.
"""
import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_data_dir():
    """Create temporary data directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)

@pytest.fixture
def sample_dataframe():
    """Create sample DataFrame for testing."""
    import pandas as pd
    return pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'value': [10.5, 20.3, 30.1]
    })
