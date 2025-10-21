"""
Generic file-based data extractor.
"""
import pandas as pd
from typing import Dict, Any, Optional
from pathlib import Path
from .base_extractor import BaseExtractor

class FileExtractor(BaseExtractor):
    """Generic extractor for file-based data sources."""
    
    def __init__(self, file_path: str, file_type: str = "csv", **kwargs):
        """
        Initialize file extractor.
        
        Args:
            file_path: Path to the file
            file_type: Type of file (csv, json, excel, parquet)
            **kwargs: Additional arguments for pandas readers
        """
        super().__init__(
            name=f"file_{Path(file_path).stem}",
            config={
                "file_path": file_path,
                "file_type": file_type,
                **kwargs
            }
        )
    
    def extract(self) -> pd.DataFrame:
        """
        Extract data from file.
        
        Returns:
            DataFrame with file data
        """
        file_path = Path(self.config['file_path'])
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        self.logger.info(f"Extracting data from {file_path}")
        
        try:
            # Read file based on type
            if self.config['file_type'] == 'csv':
                df = pd.read_csv(file_path, **{k: v for k, v in self.config.items() 
                                               if k not in ['file_path', 'file_type']})
            elif self.config['file_type'] == 'json':
                df = pd.read_json(file_path, **{k: v for k, v in self.config.items() 
                                               if k not in ['file_path', 'file_type']})
            elif self.config['file_type'] == 'excel':
                df = pd.read_excel(file_path, **{k: v for k, v in self.config.items() 
                                                 if k not in ['file_path', 'file_type']})
            elif self.config['file_type'] == 'parquet':
                df = pd.read_parquet(file_path, **{k: v for k, v in self.config.items() 
                                                  if k not in ['file_path', 'file_type']})
            else:
                raise ValueError(f"Unsupported file type: {self.config['file_type']}")
            
            # Save metadata
            metadata = {
                "source": "file",
                "file_path": str(file_path),
                "file_type": self.config['file_type'],
                "extraction_date": pd.Timestamp.now().isoformat(),
                "records_count": len(df),
                "columns": list(df.columns)
            }
            self.save_metadata(metadata)
            
            self.logger.info(f"Extraction successful: {len(df)} records")
            return df
            
        except Exception as e:
            self.logger.error(f"File extraction failed: {e}")
            raise
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate extracted data.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Basic validation
            if data.empty:
                self.logger.error("DataFrame is empty")
                return False
            
            # Check for excessive missing values
            missing_percentage = (data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100
            if missing_percentage > 50:
                self.logger.warning(f"High missing value percentage: {missing_percentage:.1f}%")
            
            self.logger.info("File data validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False