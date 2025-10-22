# Configuration Guide

This guide covers all configuration options for the Mushroom ETL Pipeline.

## 📋 Table of Contents

- [Environment Variables](#environment-variables)
- [YAML Configuration](#yaml-configuration)
- [Pipeline Configuration](#pipeline-configuration)
- [Database Configuration](#database-configuration)
- [Logging Configuration](#logging-configuration)
- [Component Configuration](#component-configuration)

## Environment Variables

### Core Environment Variables

```bash
# Environment
ENVIRONMENT=development  # development, production, testing

# Database
DATABASE_URL=sqlite:///data/mushroom_etl.db
DATABASE_ECHO=false
DATABASE_POOL_SIZE=5

# Data Sources
UCI_MUSHROOM_URL=https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/etl_pipeline.log
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Data Directories
RAW_DATA_DIR=data/raw
PROCESSED_DATA_DIR=data/processed
MODELS_DIR=data/models
LOGS_DIR=logs

# Performance
MAX_WORKERS=4
BATCH_SIZE=1000
CHUNK_SIZE=10000

# Security
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

### Production Environment Variables

```bash
# Production Database
DATABASE_URL=postgresql://user:password@localhost:5432/mushroom_etl
DATABASE_ECHO=false
DATABASE_POOL_SIZE=20

# Production Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/mushroom-etl/pipeline.log

# Production Security
SECRET_KEY=production-secret-key
API_KEY=production-api-key
```

## YAML Configuration

### Pipeline Configuration (`config/pipeline.yaml`)

```yaml
pipeline:
  name: "mushroom_etl"
  version: "1.0.0"
  description: "ETL pipeline for mushroom classification data"
  
sources:
  uci_mushroom:
    url: "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
    format: "csv"
    timeout: 30
    retries: 3
    
  file_sources:
    - path: "data/raw/mushroom_data.csv"
      format: "csv"
    - path: "data/raw/mushroom_data.json"
      format: "json"
      
  api_sources:
    - url: "https://api.example.com/mushroom-data"
      headers:
        Authorization: "Bearer ${API_KEY}"
      params:
        limit: 1000
        format: "json"

processing:
  batch_size: 1000
  max_workers: 4
  chunk_size: 10000
  memory_limit: "2GB"
  
  data_cleaning:
    handle_missing: "drop"  # drop, fill, median, mode
    remove_duplicates: true
    outlier_method: "iqr"  # iqr, zscore
    standardize_text: true
    
  feature_engineering:
    categorical_encoding: "onehot"  # onehot, label, target
    feature_scaling: true
    feature_selection: true
    n_features: 20
    create_interactions: false

output:
  database:
    table_name: "mushroom_data"
    if_exists: "replace"  # replace, append, fail
    chunk_size: 1000
    
  files:
    formats: ["csv", "parquet"]
    compression: "gzip"
    output_dir: "data/processed"
    
  monitoring:
    enable_metrics: true
    metrics_interval: 60
    health_check_interval: 300
```

### Database Configuration (`config/database.yaml`)

```yaml
database:
  url: "${DATABASE_URL}"
  echo: false
  pool_size: 5
  max_overflow: 10
  pool_timeout: 30
  pool_recycle: 3600
  
  connection:
    timeout: 30
    retries: 3
    backoff_factor: 2
    
  tables:
    mushroom_data:
      primary_key: "id"
      indexes:
        - "class"
        - "feature1"
        - "feature2"
      constraints:
        - "class IN ('e', 'p')"
        
  migrations:
    enabled: true
    directory: "migrations"
    auto_migrate: true
```

## Pipeline Configuration

### ETL Pipeline Configuration

```python
# config/etl_config.py
from src.utils.config import ETLConfig

# Development configuration
dev_config = ETLConfig(
    environment="development",
    database_url="sqlite:///data/mushroom_etl_dev.db",
    log_level="DEBUG",
    max_workers=2
)

# Production configuration
prod_config = ETLConfig(
    environment="production",
    database_url="postgresql://user:pass@localhost:5432/mushroom_etl",
    log_level="INFO",
    max_workers=8
)
```

### Component-Specific Configuration

#### Extraction Configuration

```python
# UCI Mushroom Extractor
uci_config = {
    "url": "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data",
    "timeout": 30,
    "retries": 3,
    "headers": {
        "User-Agent": "Mushroom-ETL/1.0"
    }
}

# File Extractor
file_config = {
    "file_path": "data/raw/mushroom_data.csv",
    "file_type": "csv",
    "encoding": "utf-8",
    "delimiter": ",",
    "skip_rows": 0
}

# API Extractor
api_config = {
    "url": "https://api.example.com/mushroom-data",
    "headers": {
        "Authorization": "Bearer ${API_KEY}",
        "Content-Type": "application/json"
    },
    "params": {
        "limit": 1000,
        "format": "json"
    },
    "timeout": 30,
    "retries": 3
}
```

#### Transformation Configuration

```python
# Data Cleaner
cleaner_config = {
    "handle_missing": "drop",  # drop, fill, median, mode
    "remove_duplicates": True,
    "outlier_method": "iqr",  # iqr, zscore
    "outlier_threshold": 3.0,
    "standardize_text": True,
    "text_columns": ["cap_shape", "cap_surface", "cap_color"]
}

# Feature Engineer
engineer_config = {
    "categorical_encoding": "onehot",  # onehot, label, target
    "feature_scaling": True,
    "scaling_method": "standard",  # standard, minmax, robust
    "feature_selection": True,
    "selection_method": "mutual_info",  # mutual_info, f_score, chi2
    "n_features": 20,
    "create_interactions": False,
    "interaction_degree": 2
}
```

#### Loading Configuration

```python
# Database Loader
db_config = {
    "database_url": "sqlite:///data/mushroom_etl.db",
    "table_name": "mushroom_data",
    "if_exists": "replace",  # replace, append, fail
    "chunk_size": 1000,
    "index": False,
    "method": "multi"  # multi, single
}

# File Loader
file_config = {
    "file_format": "parquet",  # csv, parquet, json, excel
    "output_dir": "data/processed",
    "compression": "gzip",  # gzip, bz2, xz, None
    "index": False,
    "encoding": "utf-8"
}
```

## Database Configuration

### SQLite Configuration

```python
# Development SQLite
sqlite_config = {
    "database_url": "sqlite:///data/mushroom_etl.db",
    "echo": False,
    "pool_size": 1,
    "connect_args": {
        "check_same_thread": False,
        "timeout": 30
    }
}
```

### PostgreSQL Configuration

```python
# Production PostgreSQL
postgres_config = {
    "database_url": "postgresql://user:password@localhost:5432/mushroom_etl",
    "echo": False,
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "connect_args": {
        "sslmode": "require"
    }
}
```

### MySQL Configuration

```python
# Production MySQL
mysql_config = {
    "database_url": "mysql+pymysql://user:password@localhost:3306/mushroom_etl",
    "echo": False,
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "connect_args": {
        "charset": "utf8mb4"
    }
}
```

## Logging Configuration

### Basic Logging

```python
# config/logging.yaml
version: 1
disable_existing_loggers: false

formatters:
  standard:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: standard
    stream: ext://sys.stdout
    
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: detailed
    filename: logs/etl_pipeline.log
    mode: a
    
  rotating_file:
    class: logging.handlers.RotatingFileHandler
    level: DEBUG
    formatter: detailed
    filename: logs/etl_pipeline.log
    mode: a
    maxBytes: 10485760  # 10MB
    backupCount: 5

loggers:
  src:
    level: DEBUG
    handlers: [console, file]
    propagate: false
    
  src.extract:
    level: INFO
    handlers: [console, file]
    propagate: false
    
  src.transform:
    level: INFO
    handlers: [console, file]
    propagate: false
    
  src.load:
    level: INFO
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console, rotating_file]
```

### Advanced Logging with Structlog

```python
# config/structlog_config.py
import structlog
from structlog.stdlib import LoggerFactory

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

## Component Configuration

### Environment-Specific Configuration

```python
# config/environments.py
import os
from src.utils.config import ETLConfig

def get_config(environment: str = None) -> ETLConfig:
    """Get configuration for specific environment."""
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")
    
    configs = {
        "development": ETLConfig(
            environment="development",
            database_url="sqlite:///data/mushroom_etl_dev.db",
            log_level="DEBUG",
            max_workers=2,
            batch_size=100
        ),
        "testing": ETLConfig(
            environment="testing",
            database_url="sqlite:///data/mushroom_etl_test.db",
            log_level="WARNING",
            max_workers=1,
            batch_size=10
        ),
        "production": ETLConfig(
            environment="production",
            database_url=os.getenv("DATABASE_URL"),
            log_level="INFO",
            max_workers=8,
            batch_size=1000
        )
    }
    
    return configs.get(environment, configs["development"])
```

### Dynamic Configuration Loading

```python
# config/config_loader.py
import yaml
from pathlib import Path
from src.utils.config import ETLConfig

def load_yaml_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def merge_configs(base_config: ETLConfig, yaml_config: dict) -> ETLConfig:
    """Merge base configuration with YAML configuration."""
    # Update base config with YAML values
    for key, value in yaml_config.items():
        if hasattr(base_config, key):
            setattr(base_config, key, value)
    
    return base_config

def load_complete_config(environment: str = None) -> ETLConfig:
    """Load complete configuration for environment."""
    # Load base configuration
    base_config = get_config(environment)
    
    # Load YAML configurations
    config_dir = Path("config")
    
    # Load pipeline configuration
    pipeline_config = load_yaml_config(config_dir / "pipeline.yaml")
    base_config = merge_configs(base_config, pipeline_config)
    
    # Load database configuration
    db_config = load_yaml_config(config_dir / "database.yaml")
    base_config = merge_configs(base_config, db_config)
    
    return base_config
```

## 🔧 Configuration Validation

### Pydantic Validation

```python
# config/validation.py
from pydantic import BaseModel, validator
from typing import Optional, List

class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False
    pool_size: int = 5
    
    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(('sqlite://', 'postgresql://', 'mysql://')):
            raise ValueError('Invalid database URL format')
        return v
    
    @validator('pool_size')
    def validate_pool_size(cls, v):
        if v < 1 or v > 100:
            raise ValueError('Pool size must be between 1 and 100')
        return v

class PipelineConfig(BaseModel):
    name: str
    version: str
    batch_size: int = 1000
    max_workers: int = 4
    
    @validator('batch_size')
    def validate_batch_size(cls, v):
        if v < 1:
            raise ValueError('Batch size must be positive')
        return v
    
    @validator('max_workers')
    def validate_max_workers(cls, v):
        if v < 1 or v > 32:
            raise ValueError('Max workers must be between 1 and 32')
        return v
```

## 📝 Configuration Examples

### Complete Development Configuration

```python
# config/development.py
from src.utils.config import ETLConfig

config = ETLConfig(
    environment="development",
    database_url="sqlite:///data/mushroom_etl_dev.db",
    uci_mushroom_url="https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data",
    log_level="DEBUG",
    log_file="logs/etl_pipeline_dev.log",
    raw_data_dir="data/raw",
    processed_data_dir="data/processed",
    models_dir="data/models",
    max_workers=2,
    batch_size=100
)
```

### Complete Production Configuration

```python
# config/production.py
import os
from src.utils.config import ETLConfig

config = ETLConfig(
    environment="production",
    database_url=os.getenv("DATABASE_URL"),
    uci_mushroom_url=os.getenv("UCI_MUSHROOM_URL"),
    log_level="INFO",
    log_file="/var/log/mushroom-etl/pipeline.log",
    raw_data_dir="/data/raw",
    processed_data_dir="/data/processed",
    models_dir="/data/models",
    max_workers=8,
    batch_size=1000
)
```

## 🚀 Configuration Best Practices

1. **Environment Separation**: Use different configurations for different environments
2. **Secret Management**: Store sensitive data in environment variables
3. **Validation**: Validate all configuration values
4. **Documentation**: Document all configuration options
5. **Defaults**: Provide sensible defaults for all options
6. **Override**: Allow configuration override through environment variables
7. **Testing**: Test configuration loading and validation
8. **Monitoring**: Monitor configuration changes in production
