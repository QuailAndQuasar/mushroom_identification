"""
UCI Mushroom dataset extractor.
"""
import pandas as pd
import requests
from typing import Dict, Any, Optional
from pathlib import Path
from io import StringIO
from .base_extractor import BaseExtractor
from ..utils.config import config

class UCIMushroomExtractor(BaseExtractor):
    """Extractor for UCI Mushroom dataset."""
    
    def __init__(self):
        super().__init__(
            name="uci_mushroom",
            config={
                "url": config.uci_mushroom_url,
                "output_file": "mushrooms.csv"
            }
        )
        
        # Column names as specified in UCI dataset description
        self.column_names = [
            'class', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
            'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color',
            'stalk-shape', 'stalk-root', 'stalk-surface-above-ring',
            'stalk-surface-below-ring', 'stalk-color-above-ring',
            'stalk-color-below-ring', 'veil-type', 'veil-color', 'ring-number',
            'ring-type', 'spore-print-color', 'habitat', 'season'
        ]
    
    def extract(self) -> pd.DataFrame:
        """
        Extract UCI Mushroom dataset.
        
        Returns:
            DataFrame with mushroom data
        """
        self.logger.info(f"Extracting UCI Mushroom dataset from {self.config['url']}")
        
        try:
            # Download the data
            response = requests.get(self.config['url'], timeout=30)
            response.raise_for_status()
            
            # Create DataFrame
            df = pd.read_csv(
                StringIO(response.text),
                header=None,
                names=self.column_names
            )
            
            # Save raw data
            output_path = Path(config.raw_data_dir) / self.config['output_file']
            df.to_csv(output_path, index=False)
            
            # Save metadata
            metadata = {
                "source": "UCI ML Repository",
                "url": self.config['url'],
                "extraction_date": pd.Timestamp.now().isoformat(),
                "records_count": len(df),
                "columns": list(df.columns),
                "output_file": str(output_path)
            }
            self.save_metadata(metadata)
            
            self.logger.info(f"Extraction successful: {len(df)} records saved to {output_path}")
            return df
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to download data: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Extraction failed: {e}")
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
            # Check if DataFrame is not empty
            if data.empty:
                self.logger.error("DataFrame is empty")
                return False
            
            # Check required columns
            required_columns = ['class', 'cap-shape', 'cap-surface', 'cap-color']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                self.logger.error(f"Missing required columns: {missing_columns}")
                return False
            
            # Check for missing values
            missing_count = data.isnull().sum().sum()
            if missing_count > 0:
                self.logger.warning(f"Found {missing_count} missing values")
            
            # Check data types
            if data['class'].dtype != 'object':
                self.logger.error("Class column should be categorical")
                return False
            
            self.logger.info("Data validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            return False