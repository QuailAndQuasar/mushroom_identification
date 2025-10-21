"""
Base extractor interface for all data sources.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pathlib import Path
import logging
from ..utils.config import config
from ..utils.logging import logger

class BaseExtractor(ABC):
    """Abstract base class for all data extractors."""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the extractor.
        
        Args:
            name: Name of the extractor
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = logger.getChild(f"extractor.{name}")
        
    @abstractmethod
    def extract(self) -> Any:
        """
        Extract data from the source.
        
        Returns:
            Extracted data
        """
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """
        Validate extracted data.
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def save_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Save extraction metadata.
        
        Args:
            metadata: Metadata to save
        """
        metadata_file = Path(config.raw_data_dir) / f"{self.name}_metadata.json"
        import json
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        self.logger.info(f"Metadata saved to {metadata_file}")
    
    def log_extraction(self, success: bool, records_count: int = None, error: str = None) -> None:
        """
        Log extraction results.
        
        Args:
            success: Whether extraction was successful
            records_count: Number of records extracted
            error: Error message if failed
        """
        if success:
            self.logger.info(f"Extraction successful: {records_count} records")
        else:
            self.logger.error(f"Extraction failed: {error}")