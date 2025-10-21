"""
Configuration management for the ETL pipeline.
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseSettings, Field, validator

class DatabaseConfig(BaseSettings):
    """Database configuration."""
    url: str = Field(default="sqlite:///data/mushroom_etl.db", description="Database connection URL")
    echo: bool = Field(default=False, description="Enable SQLAlchemy echo")
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Max overflow connections")
    
    class Config:
        env_prefix = "DATABASE_"

class DataSourceConfig(BaseSettings):
    """Data source configuration."""
    uci_mushroom_url: str = Field(
        default="https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data",
        description="UCI Mushroom dataset URL"
    )
    
    class Config:
        env_prefix = "DATA_"

class LoggingConfig(BaseSettings):
    """Logging configuration."""
    level: str = Field(default="INFO", description="Log level")
    file: str = Field(default="logs/etl_pipeline.log", description="Log file path")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format")
    
    class Config:
        env_prefix = "LOG_"

class ModelConfig(BaseSettings):
    """Model configuration."""
    version: str = Field(default="1.0.0", description="Model version")
    path: str = Field(default="models/", description="Model storage path")
    
    class Config:
        env_prefix = "MODEL_"

class ETLConfig(BaseSettings):
    """Main ETL configuration."""
    # Project paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data")
    raw_data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "raw")
    processed_data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "processed")
    models_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "models")
    
    # Sub-configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    data_source: DataSourceConfig = Field(default_factory=DataSourceConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    
    # Processing settings
    batch_size: int = Field(default=1000, description="Processing batch size")
    max_workers: int = Field(default=4, description="Max worker processes")
    
    @validator('data_dir', 'raw_data_dir', 'processed_data_dir', 'models_dir')
    def ensure_directories(cls, v):
        """Ensure directories exist."""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global configuration instance
config = ETLConfig()