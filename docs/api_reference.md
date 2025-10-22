# API Reference

This document provides a comprehensive reference for all classes, methods, and functions in the Mushroom ETL Pipeline.

## 📚 Table of Contents

- [Extraction Module](#extraction-module)
- [Transformation Module](#transformation-module)
- [Loading Module](#loading-module)
- [Orchestration Module](#orchestration-module)
- [Utilities](#utilities)

## Extraction Module

### BaseExtractor

Abstract base class for all data extractors.

```python
class BaseExtractor:
    def __init__(self, name: str, config: Optional[Dict] = None)
    def extract(self) -> pd.DataFrame
    def validate(self, data: pd.DataFrame) -> bool
    def save_metadata(self, metadata: Dict) -> None
    def log_extraction(self, message: str) -> None
```

**Parameters:**
- `name` (str): Name of the extractor
- `config` (Optional[Dict]): Configuration dictionary

**Methods:**
- `extract()`: Abstract method to extract data
- `validate()`: Abstract method to validate extracted data
- `save_metadata()`: Save extraction metadata
- `log_extraction()`: Log extraction messages

### UCIMushroomExtractor

Extractor for UCI Mushroom dataset.

```python
class UCIMushroomExtractor(BaseExtractor):
    def __init__(self, url: str = None, config: Optional[Dict] = None)
    def extract(self) -> pd.DataFrame
    def validate(self, data: pd.DataFrame) -> bool
```

**Parameters:**
- `url` (str): URL to UCI Mushroom dataset
- `config` (Optional[Dict]): Configuration dictionary

### FileExtractor

Generic file extractor for various file formats.

```python
class FileExtractor(BaseExtractor):
    def __init__(self, file_path: str, file_type: str = None, config: Optional[Dict] = None)
    def extract(self) -> pd.DataFrame
    def validate(self, data: pd.DataFrame) -> bool
```

**Parameters:**
- `file_path` (str): Path to the file
- `file_type` (str): Type of file (csv, json, excel, parquet)
- `config` (Optional[Dict]): Configuration dictionary

### APIExtractor

Generic API extractor for REST APIs.

```python
class APIExtractor(BaseExtractor):
    def __init__(self, url: str, headers: Dict = None, params: Dict = None, config: Optional[Dict] = None)
    def extract(self) -> pd.DataFrame
    def validate(self, data: pd.DataFrame) -> bool
```

**Parameters:**
- `url` (str): API endpoint URL
- `headers` (Dict): HTTP headers
- `params` (Dict): Query parameters
- `config` (Optional[Dict]): Configuration dictionary

### ExtractionOrchestrator

Orchestrates multiple extractors.

```python
class ExtractionOrchestrator:
    def __init__(self, config: Optional[Dict] = None)
    def add_extractor(self, extractor: BaseExtractor) -> None
    def run_all_extractions(self) -> Dict[str, pd.DataFrame]
    def get_extraction_summary(self) -> Dict
```

## Transformation Module

### BaseTransformer

Abstract base class for all data transformers.

```python
class BaseTransformer:
    def __init__(self, name: str, config: Optional[Dict] = None)
    def transform(self, data: pd.DataFrame) -> pd.DataFrame
    def validate(self, data: pd.DataFrame) -> bool
    def save_statistics(self, stats: Dict) -> None
    def log_transformation(self, message: str) -> None
```

### DataCleaner

Data cleaning transformer.

```python
class DataCleaner(BaseTransformer):
    def __init__(self, config: Optional[Dict] = None)
    def transform(self, data: pd.DataFrame) -> pd.DataFrame
    def validate(self, data: pd.DataFrame) -> bool
    def remove_duplicates(self, data: pd.DataFrame) -> pd.DataFrame
    def handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame
    def detect_outliers(self, data: pd.DataFrame) -> pd.DataFrame
    def standardize_text(self, data: pd.DataFrame) -> pd.DataFrame
```

**Configuration Options:**
- `handle_missing`: Strategy for missing values (drop, fill, median, mode)
- `remove_duplicates`: Whether to remove duplicates
- `outlier_method`: Method for outlier detection (iqr, zscore)
- `standardize_text`: Whether to standardize text columns

### FeatureEngineer

Feature engineering transformer.

```python
class FeatureEngineer(BaseTransformer):
    def __init__(self, config: Optional[Dict] = None)
    def transform(self, data: pd.DataFrame) -> pd.DataFrame
    def validate(self, data: pd.DataFrame) -> bool
    def encode_categorical(self, data: pd.DataFrame) -> pd.DataFrame
    def scale_features(self, data: pd.DataFrame) -> pd.DataFrame
    def select_features(self, data: pd.DataFrame) -> pd.DataFrame
    def create_interactions(self, data: pd.DataFrame) -> pd.DataFrame
```

**Configuration Options:**
- `categorical_encoding`: Encoding method (onehot, label, target)
- `feature_scaling`: Whether to scale features
- `feature_selection`: Whether to select features
- `n_features`: Number of features to select
- `create_interactions`: Whether to create feature interactions

### TransformationPipeline

Orchestrates multiple transformers.

```python
class TransformationPipeline:
    def __init__(self, config: Optional[Dict] = None)
    def add_transformer(self, transformer: BaseTransformer) -> None
    def run_transformations(self, data: pd.DataFrame) -> pd.DataFrame
    def get_transformation_summary(self) -> Dict
```

## Loading Module

### BaseLoader

Abstract base class for all data loaders.

```python
class BaseLoader:
    def __init__(self, name: str, config: Optional[Dict] = None)
    def load(self, data: pd.DataFrame) -> bool
    def validate(self, data: pd.DataFrame) -> bool
    def save_statistics(self, stats: Dict) -> None
    def log_loading(self, message: str) -> None
```

### DatabaseLoader

Database loader using SQLAlchemy.

```python
class DatabaseLoader(BaseLoader):
    def __init__(self, config: Optional[Dict] = None)
    def load(self, data: pd.DataFrame) -> bool
    def validate(self, data: pd.DataFrame) -> bool
    def create_engine(self) -> Engine
    def create_schema(self, data: pd.DataFrame) -> None
    def test_connection(self) -> bool
```

**Configuration Options:**
- `database_url`: Database connection URL
- `table_name`: Target table name
- `if_exists`: Action if table exists (replace, append, fail)
- `chunk_size`: Chunk size for loading

### FileLoader

File loader for various formats.

```python
class FileLoader(BaseLoader):
    def __init__(self, config: Optional[Dict] = None)
    def load(self, data: pd.DataFrame) -> bool
    def validate(self, data: pd.DataFrame) -> bool
    def save_to_csv(self, data: pd.DataFrame) -> bool
    def save_to_parquet(self, data: pd.DataFrame) -> bool
    def save_to_json(self, data: pd.DataFrame) -> bool
    def save_to_excel(self, data: pd.DataFrame) -> bool
```

**Configuration Options:**
- `file_format`: Output format (csv, parquet, json, excel)
- `output_dir`: Output directory
- `compression`: Compression method
- `index`: Whether to include index

### LoadingPipeline

Orchestrates multiple loaders.

```python
class LoadingPipeline:
    def __init__(self, config: Optional[Dict] = None)
    def add_loader(self, loader: BaseLoader) -> None
    def run_loadings(self, data: pd.DataFrame) -> bool
    def get_loading_summary(self) -> Dict
```

## Orchestration Module

### ETLPipeline

Main ETL pipeline orchestrator.

```python
class ETLPipeline:
    def __init__(self, config: Optional[Dict] = None)
    def configure_extraction(self, extractors: List[BaseExtractor]) -> None
    def configure_transformation(self, transformers: List[BaseTransformer]) -> None
    def configure_loading(self, loaders: List[BaseLoader]) -> None
    def run_pipeline(self) -> bool
    def get_pipeline_stats(self) -> Dict
    def get_pipeline_health(self) -> Dict
    def save_pipeline_logs(self) -> None
```

**Methods:**
- `configure_extraction()`: Configure extraction stage
- `configure_transformation()`: Configure transformation stage
- `configure_loading()`: Configure loading stage
- `run_pipeline()`: Run complete ETL pipeline
- `get_pipeline_stats()`: Get pipeline statistics
- `get_pipeline_health()`: Get pipeline health status
- `save_pipeline_logs()`: Save pipeline logs

## Utilities

### Configuration

Configuration management using Pydantic.

```python
class ETLConfig(BaseSettings):
    # Database configuration
    database_url: str = "sqlite:///data/mushroom_etl.db"
    
    # Data source configuration
    uci_mushroom_url: str = "https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data"
    
    # Logging configuration
    log_level: str = "INFO"
    log_file: str = "logs/etl_pipeline.log"
    
    # Data directories
    raw_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    models_dir: str = "data/models"
```

### Logging

Centralized logging system.

```python
def setup_logging(config: ETLConfig) -> None
def get_logger(name: str) -> Logger
```

## 📝 Usage Examples

### Basic ETL Pipeline

```python
from src.orchestration.etl_pipeline import ETLPipeline
from src.extract.uci_mushroom_extractor import UCIMushroomExtractor
from src.transform.data_cleaner import DataCleaner
from src.load.database_loader import DatabaseLoader

# Initialize pipeline
pipeline = ETLPipeline()

# Configure stages
extractor = UCIMushroomExtractor()
cleaner = DataCleaner()
db_loader = DatabaseLoader()

pipeline.configure_extraction([extractor])
pipeline.configure_transformation([cleaner])
pipeline.configure_loading([db_loader])

# Run pipeline
success = pipeline.run_pipeline()
```

### Custom Configuration

```python
# Custom extractor configuration
extractor_config = {
    "url": "https://custom-dataset.com/data.csv",
    "timeout": 30
}
extractor = UCIMushroomExtractor(config=extractor_config)

# Custom transformer configuration
transformer_config = {
    "handle_missing": "fill",
    "outlier_method": "zscore",
    "feature_scaling": True
}
cleaner = DataCleaner(config=transformer_config)

# Custom loader configuration
loader_config = {
    "table_name": "custom_table",
    "if_exists": "append"
}
db_loader = DatabaseLoader(config=loader_config)
```

## 🔧 Error Handling

All classes include comprehensive error handling:

```python
try:
    result = pipeline.run_pipeline()
    if result:
        print("Pipeline completed successfully!")
    else:
        print("Pipeline failed!")
except Exception as e:
    print(f"Pipeline error: {e}")
```

## 📊 Return Values

### DataFrames
All extractors and transformers return pandas DataFrames with:
- Consistent column naming
- Proper data types
- Validated data quality

### Statistics
All components return statistics dictionaries with:
- Processing metrics
- Quality metrics
- Performance metrics
- Error information

### Health Status
Pipeline health includes:
- Overall status
- Stage completion
- Error counts
- Performance metrics
