"""
Base loader interface for all data loading operations.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from pathlib import Path
from ..utils.config import config
from ..utils.logging import logger

class BaseLoader(ABC):
    """Abstract base class for all data loaders."""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the loader.
        
        Args:
            name: Name of the loader
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = logger.getChild(f"loader.{name}")
        self.stats = {}
        
    @abstractmethod
    def load(self, data: pd.DataFrame, destination: str) -> bool:
        """
        Load data to destination.
        
        Args:
            data: DataFrame to load
            destination: Destination path or identifier
            
        Returns:
            True if successful, False otherwise
        """
        pass
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate data before loading.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get loading statistics.
        
        Returns:
            Dictionary of loading statistics
        """
        return self.stats
    
    def save_stats(self, output_dir: Path = None) -> None:
        """
        Save loading statistics.
        
        Args:
            output_dir: Directory to save stats
        """
        if output_dir is None:
            output_dir = Path(config.processed_data_dir)
        
        stats_file = output_dir / f"{self.name}_loading_stats.json"
        import json
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        self.logger.info(f"Loading stats saved to {stats_file}")
    
    def log_loading(self, success: bool, records_count: int, destination: str, error: str = None) -> None:
        """
        Log loading results.
        
        Args:
            success: Whether loading was successful
            records_count: Number of records loaded
            destination: Destination path or identifier
            error: Error message if failed
        """
        if success:
            self.logger.info(f"Loading successful: {records_count} records to {destination}")
        else:
            self.logger.error(f"Loading failed to {destination}: {error}")