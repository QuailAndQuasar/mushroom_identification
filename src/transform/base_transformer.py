"""
Base transformer interface for all data transformations.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from pathlib import Path
from ..utils.config import config
from ..utils.logging import logger

class BaseTransformer(ABC):
    """Abstract base class for all data transformers."""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        """
        Initialize the transformer.
        
        Args:
            name: Name of the transformer
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = logger.getChild(f"transformer.{name}")
        self.stats = {}
        
    @abstractmethod
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform the input data.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Transformed DataFrame
        """
        pass
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate transformed data.
        
        Args:
            data: Transformed DataFrame
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get transformation statistics.
        
        Returns:
            Dictionary of transformation statistics
        """
        return self.stats
    
    def save_stats(self, output_dir: Path = None) -> None:
        """
        Save transformation statistics.
        
        Args:
            output_dir: Directory to save stats
        """
        if output_dir is None:
            output_dir = Path(config.processed_data_dir)
        
        stats_file = output_dir / f"{self.name}_stats.json"
        import json
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        self.logger.info(f"Stats saved to {stats_file}")
    
    def log_transformation(self, success: bool, input_shape: Tuple[int, int], 
                          output_shape: Tuple[int, int], error: str = None) -> None:
        """
        Log transformation results.
        
        Args:
            success: Whether transformation was successful
            input_shape: Input data shape
            output_shape: Output data shape
            error: Error message if failed
        """
        if success:
            self.logger.info(f"Transformation successful: {input_shape} -> {output_shape}")
        else:
            self.logger.error(f"Transformation failed: {error}")