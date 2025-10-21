"""
Transformation pipeline orchestrator for coordinating multiple transformers.
"""
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path
from .base_transformer import BaseTransformer
from .data_cleaner import DataCleaner
from .feature_engineer import FeatureEngineer
from ..utils.config import config
from ..utils.logging import logger

class TransformationPipeline:
    """Orchestrator for managing multiple data transformers."""
    
    def __init__(self):
        self.logger = logger.getChild("pipeline")
        self.transformers: List[BaseTransformer] = []
        self.results: Dict[str, pd.DataFrame] = {}
        self.stats: Dict[str, Any] = {}
    
    def add_transformer(self, transformer: BaseTransformer) -> None:
        """
        Add a transformer to the pipeline.
        
        Args:
            transformer: Transformer to add
        """
        self.transformers.append(transformer)
        self.logger.info(f"Added transformer: {transformer.name}")
    
    def run_transformations(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Run all transformers and return final result.
        
        Args:
            data: Input DataFrame
            
        Returns:
            Final transformed DataFrame
        """
        self.logger.info(f"Starting transformation pipeline for {len(data)} records")
        
        current_data = data.copy()
        
        for transformer in self.transformers:
            try:
                self.logger.info(f"Running transformer: {transformer.name}")
                
                # Transform data
                transformed_data = transformer.transform(current_data)
                
                # Validate transformation
                if transformer.validate(transformed_data):
                    self.results[transformer.name] = transformed_data
                    current_data = transformed_data
                    self.logger.info(f"Transformation successful: {transformer.name}")
                else:
                    self.logger.error(f"Validation failed: {transformer.name}")
                    continue
                    
            except Exception as e:
                self.logger.error(f"Transformation failed for {transformer.name}: {e}")
                continue
        
        self.logger.info(f"Transformation pipeline completed: {len(self.results)} successful, {len(self.transformers) - len(self.results)} failed")
        return current_data
    
    def get_transformation_summary(self) -> Dict[str, Any]:
        """
        Get summary of all transformations.
        
        Returns:
            Summary dictionary
        """
        summary = {
            "total_transformers": len(self.transformers),
            "successful_transformations": len(self.results),
            "failed_transformations": len(self.transformers) - len(self.results),
            "total_records": sum(len(df) for df in self.results.values()) if self.results else 0,
            "transformers": {}
        }
        
        for name, df in self.results.items():
            summary["transformers"][name] = {
                "records": len(df),
                "columns": list(df.columns),
                "memory_usage": df.memory_usage(deep=True).sum()
            }
        
        return summary
    
    def save_combined_data(self, output_file: str = "transformed_data.csv") -> None:
        """
        Save all transformation results to files.
        
        Args:
            output_file: Output filename for final result
        """
        if not self.results:
            self.logger.warning("No transformation results to save")
            return
        
        # Save final result
        if self.results:
            final_data = list(self.results.values())[-1]  # Get last transformation result
            output_path = Path(config.processed_data_dir) / output_file
            final_data.to_csv(output_path, index=False)
            self.logger.info(f"Final transformed data saved to {output_path}")
        
        # Save individual transformation results
        for name, df in self.results.items():
            individual_path = Path(config.processed_data_dir) / f"{name}_output.csv"
            df.to_csv(individual_path, index=False)
            self.logger.info(f"Transformation {name} saved to {individual_path}")
    
    def get_transformer_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics from all transformers.
        
        Returns:
            Dictionary of transformer statistics
        """
        stats = {}
        for transformer in self.transformers:
            if hasattr(transformer, 'get_stats'):
                stats[transformer.name] = transformer.get_stats()
        return stats
