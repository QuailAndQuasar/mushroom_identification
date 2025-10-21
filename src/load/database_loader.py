"""
Database loader for SQL databases using SQLAlchemy.
"""
import pandas as pd
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, Integer, Float, Boolean
from sqlalchemy.exc import SQLAlchemyError
from .base_loader import BaseLoader
from ..utils.config import config

class DatabaseLoader(BaseLoader):
    """Loader for SQL databases."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize database loader.
        
        Args:
            config: Configuration dictionary
        """
        default_config = {
            "database_url": config.database.url,
            "table_name": "mushroom_data",
            "if_exists": "replace",  # replace, append, fail
            "index": False,
            "chunksize": 1000,
            "create_schema": True
        }
        
        if config:
            default_config.update(config)
        
        super().__init__(
            name="database_loader",
            config=default_config
        )
        
        self.engine = None
        self.metadata = None
    
    def _create_engine(self) -> None:
        """Create database engine."""
        try:
            self.engine = create_engine(
                self.config["database_url"],
                echo=self.config.get("echo", False),
                pool_size=self.config.get("pool_size", 5),
                max_overflow=self.config.get("max_overflow", 10)
            )
            self.metadata = MetaData()
            self.logger.info("Database engine created successfully")
        except Exception as e:
            self.logger.error(f"Failed to create database engine: {e}")
            raise
    
    def _create_schema(self, data: pd.DataFrame) -> None:
        """Create database schema based on data."""
        if not self.config.get("create_schema", True):
            return
        
        try:
            # Create table with appropriate columns
            columns = []
            for col, dtype in data.dtypes.items():
                if dtype == 'object':
                    columns.append(Column(col, String(255)))
                elif dtype in ['int64', 'int32']:
                    columns.append(Column(col, Integer))
                elif dtype in ['float64', 'float32']:
                    columns.append(Column(col, Float))
                elif dtype == 'bool':
                    columns.append(Column(col, Boolean))
                else:
                    columns.append(Column(col, String(255)))
            
            table = Table(
                self.config["table_name"],
                self.metadata,
                *columns
            )
            
            # Create table
            table.create(self.engine, checkfirst=True)
            self.logger.info(f"Schema created for table: {self.config['table_name']}")
            
        except Exception as e:
            self.logger.error(f"Failed to create schema: {e}")
            raise
    
    def load(self, data: pd.DataFrame, destination: str = None) -> bool:
        """
        Load data to database.
        
        Args:
            data: DataFrame to load
            destination: Table name (optional, uses config default)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Starting database loading for {len(data)} records")
            
            # Create engine if not exists
            if self.engine is None:
                self._create_engine()
            
            # Use destination or default table name
            table_name = destination or self.config["table_name"]
            
            # Create schema
            self._create_schema(data)
            
            # Load data
            data.to_sql(
                table_name,
                self.engine,
                if_exists=self.config["if_exists"],
                index=self.config["index"],
                chunksize=self.config["chunksize"]
            )
            
            # Update stats
            self.stats["records_loaded"] = len(data)
            self.stats["table_name"] = table_name
            self.stats["columns"] = list(data.columns)
            self.stats["loading_successful"] = True
            
            self.logger.info(f"Database loading completed: {len(data)} records to {table_name}")
            return True
            
        except SQLAlchemyError as e:
            self.logger.error(f"Database loading failed: {e}")
            self.stats["loading_successful"] = False
            self.stats["error"] = str(e)
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error during database loading: {e}")
            self.stats["loading_successful"] = False
            self.stats["error"] = str(e)
            return False
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate data before loading.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Check if data is empty
            if data.empty:
                self.logger.error("Data is empty")
                return False
            
            # Check for required columns
            if len(data.columns) == 0:
                self.logger.error("No columns in data")
                return False
            
            # Check for infinite values
            numeric_cols = data.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                if data[numeric_cols].isin([float('inf'), float('-inf')]).any().any():
                    self.logger.warning("Found infinite values in numeric columns")
            
            # Check data types
            for col, dtype in data.dtypes.items():
                if dtype == 'object':
                    # Check for very long strings
                    max_length = data[col].astype(str).str.len().max()
                    if max_length > 255:
                        self.logger.warning(f"Column {col} has strings longer than 255 characters")
            
            self.logger.info("Database loading validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            if self.engine is None:
                self._create_engine()
            
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.logger.info("Database connection test successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return False