"""
Configuration management for the ETL pipeline.
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings

class ETLConfig(BaseSettings):
    """Main ETL configuration."""
    # Database configuration
    database_url: str = Field(default="sqlite:///data/mushroom_etl.db", description="Database connection URL")
    database_echo: bool = Field(default=False, description="Enable SQLAlchemy echo")
    database_pool_size: int = Field(default=5, description="Connection pool size")
    database_max_overflow: int = Field(default=10, description="Max overflow connections")
    
    # Data source configuration
    uci_mushroom_url: str = Field(
        default="https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data",
        description="UCI Mushroom dataset URL"
    )
    
    # Logging configuration
    log_level: str = Field(default="INFO", description="Log level")
    log_file: str = Field(default="logs/etl_pipeline.log", description="Log file path")
    log_format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format")
    
    # Model configuration
    model_version: str = Field(default="1.0.0", description="Model version")
    model_path: str = Field(default="models/", description="Model storage path")
    
    # Project paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data")
    raw_data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "raw")
    processed_data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "processed")
    models_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent / "data" / "models")
    
    # Processing settings
    batch_size: int = Field(default=1000, description="Processing batch size")
    max_workers: int = Field(default=4, description="Max worker processes")
    
    @field_validator('data_dir', 'raw_data_dir', 'processed_data_dir', 'models_dir')
    @classmethod
    def ensure_directories(cls, v):
        """Ensure directories exist."""
        v.mkdir(parents=True, exist_ok=True)
        return v
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Allow extra fields from environment
    )

# Global configuration instance
config = ETLConfig()