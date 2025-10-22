"""
File loader for saving data in various file formats.
"""
import pandas as pd
import json
from typing import Dict, Any, Optional
from pathlib import Path
from .base_loader import BaseLoader
from ..utils.config import config

class FileLoader(BaseLoader):
    """Loader for file-based data storage."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize file loader.
        
        Args:
            config: Configuration dictionary
        """
        default_config = {
            "file_format": "csv",  # csv, parquet, json, excel
            "output_dir": "data/processed",
            "index": False,
            "header": True,
            "compression": None,  # gzip, bz2, xz
            "save_metadata": True
        }
        
        if config:
            default_config.update(config)
        
        super().__init__(
            name="file_loader",
            config=default_config
        )
        
        # Ensure output directory exists
        Path(self.config["output_dir"]).mkdir(parents=True, exist_ok=True)
    
    def load(self, data: pd.DataFrame, destination: str = None) -> bool:
        """
        Load data to file.
        
        Args:
            data: DataFrame to load
            destination: Filename (optional, uses default)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Starting file loading for {len(data)} records")
            
            # Use destination or default filename
            if destination:
                filename = destination
            else:
                filename = f"loaded_data.{self.config['file_format']}"
            
            # Create full file path
            file_path = Path(self.config["output_dir"]) / filename
            
            # Load data based on format
            if self.config["file_format"] == "csv":
                data.to_csv(
                    file_path,
                    index=self.config["index"],
                    header=self.config["header"],
                    compression=self.config["compression"]
                )
            elif self.config["file_format"] == "parquet":
                data.to_parquet(
                    file_path,
                    index=self.config["index"],
                    compression=self.config["compression"]
                )
            elif self.config["file_format"] == "json":
                data.to_json(
                    file_path,
                    orient="records",
                    index=self.config["index"]
                )
            elif self.config["file_format"] == "excel":
                data.to_excel(
                    file_path,
                    index=self.config["index"],
                    header=self.config["header"]
                )
            else:
                # Custom format - save as CSV by default
                data.to_csv(
                    file_path,
                    index=self.config["index"],
                    header=self.config["header"]
                )
            
            # Save metadata if requested
            if self.config["save_metadata"]:
                self._save_metadata(data, file_path)
            
            # Update stats
            self.stats["records_loaded"] = len(data)
            self.stats["file_path"] = str(file_path)
            self.stats["file_format"] = self.config["file_format"]
            self.stats["columns"] = list(data.columns)
            self.stats["loading_successful"] = True
            
            self.logger.info(f"File loading completed: {len(data)} records to {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"File loading failed: {e}")
            self.stats["loading_successful"] = False
            self.stats["error"] = str(e)
            return False
    
    def _save_metadata(self, data: pd.DataFrame, file_path: Path) -> None:
        """
        Save file metadata.
        
        Args:
            data: DataFrame that was saved
            file_path: Path to the saved file
        """
        try:
            metadata = {
                "file_path": str(file_path),
                "file_format": self.config["file_format"],
                "records_count": len(data),
                "columns": list(data.columns),
                "dtypes": {col: str(dtype) for col, dtype in data.dtypes.items()},
                "file_size": file_path.stat().st_size if file_path.exists() else 0
            }
            
            metadata_file = file_path.with_suffix('.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.logger.info(f"Metadata saved to {metadata_file}")
            
        except Exception as e:
            self.logger.warning(f"Failed to save metadata: {e}")
    
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
            
            # Check for NaN values
            nan_count = data.isnull().sum().sum()
            if nan_count > 0:
                self.logger.warning(f"Found {nan_count} NaN values in data")
            
            # Check data types compatibility with file format
            if self.config["file_format"] == "excel":
                # Excel has limitations on data types
                for col, dtype in data.dtypes.items():
                    if dtype == 'object':
                        # Check for very long strings
                        max_length = data[col].astype(str).str.len().max()
                        if max_length > 32767:  # Excel cell limit
                            self.logger.warning(f"Column {col} has strings longer than Excel limit")
            
            self.logger.info("File loading validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False
    
    def get_supported_formats(self) -> list:
        """
        Get list of supported file formats.
        
        Returns:
            List of supported formats
        """
        return ["csv", "parquet", "json", "excel"]
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get information about a saved file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": "File not found"}
            
            # Try to load metadata
            metadata_file = path.with_suffix('.json')
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    return json.load(f)
            
            # Fallback to basic file info
            return {
                "file_path": str(path),
                "file_size": path.stat().st_size,
                "exists": True
            }
            
        except Exception as e:
            return {"error": str(e)}
