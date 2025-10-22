"""
Extraction orchestrator for managing multiple data extractors.
"""
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path

from .base_extractor import BaseExtractor
from ..utils.config import config
from ..utils.logging import logger


class ExtractionOrchestrator:
    """
    Orchestrates multiple data extractors.
    
    This class manages the execution of multiple extractors, collects their results,
    and provides a unified interface for data extraction operations.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the extraction orchestrator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.extractors: List[BaseExtractor] = []
        self.results: Dict[str, pd.DataFrame] = {}
        self.stats = {
            "total_extractors": 0,
            "successful_extractions": 0,
            "failed_extractions": 0,
            "start_time": None,
            "end_time": None,
            "duration": None
        }
    
    def add_extractor(self, extractor: BaseExtractor) -> None:
        """
        Add an extractor to the orchestrator.
        
        Args:
            extractor: The extractor to add
        """
        self.extractors.append(extractor)
        self.stats["total_extractors"] = len(self.extractors)
        logger.info(f"Added extractor: {extractor.name}")
    
    def run_all_extractions(self) -> Dict[str, pd.DataFrame]:
        """
        Run all configured extractors.
        
        Returns:
            Dictionary mapping extractor names to their extracted DataFrames
        """
        logger.info(f"Starting extraction with {len(self.extractors)} extractors")
        self.stats["start_time"] = datetime.now().isoformat()
        
        self.results = {}
        
        for extractor in self.extractors:
            try:
                logger.info(f"Running extractor: {extractor.name}")
                
                # Extract data
                data = extractor.extract()
                
                # Validate data
                if extractor.validate(data):
                    self.results[extractor.name] = data
                    self.stats["successful_extractions"] += 1
                    logger.info(f"Extraction successful: {extractor.name} - {len(data)} records")
                else:
                    logger.error(f"Data validation failed: {extractor.name}")
                    self.stats["failed_extractions"] += 1
                    
            except Exception as e:
                logger.error(f"Extraction failed for {extractor.name}: {e}")
                self.stats["failed_extractions"] += 1
        
        self.stats["end_time"] = datetime.now().isoformat()
        
        # Calculate duration
        if self.stats["start_time"] and self.stats["end_time"]:
            start = datetime.fromisoformat(self.stats["start_time"])
            end = datetime.fromisoformat(self.stats["end_time"])
            self.stats["duration"] = (end - start).total_seconds()
        
        logger.info(f"Extraction completed: {self.stats['successful_extractions']} successful, {self.stats['failed_extractions']} failed")
        
        return self.results
    
    def combine_results(self) -> pd.DataFrame:
        """
        Combine all extraction results into a single DataFrame.
        
        Returns:
            Combined DataFrame from all successful extractions
        """
        if not self.results:
            logger.warning("No extraction results to combine")
            return pd.DataFrame()
        
        try:
            # Combine all DataFrames
            combined_data = pd.concat(self.results.values(), ignore_index=True)
            logger.info(f"Combined {len(self.results)} datasets into {len(combined_data)} records")
            return combined_data
            
        except Exception as e:
            logger.error(f"Failed to combine results: {e}")
            return pd.DataFrame()
    
    def get_extraction_summary(self) -> Dict:
        """
        Get summary statistics for the extraction process.
        
        Returns:
            Dictionary containing extraction statistics
        """
        summary = self.stats.copy()
        summary["results_count"] = len(self.results)
        summary["total_records"] = sum(len(df) for df in self.results.values())
        
        # Add per-extractor statistics
        summary["extractors"] = {}
        for name, data in self.results.items():
            summary["extractors"][name] = {
                "records": len(data),
                "columns": len(data.columns),
                "success": True
            }
        
        return summary
    
    def save_extraction_logs(self) -> None:
        """Save extraction logs to file."""
        try:
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "summary": self.get_extraction_summary(),
                "config": self.config
            }
            
            log_file = Path(config.processed_data_dir) / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_extraction_logs.json"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
            
            logger.info(f"Extraction logs saved to: {log_file}")
            
        except Exception as e:
            logger.error(f"Failed to save extraction logs: {e}")
    
    def clear_results(self) -> None:
        """Clear all extraction results and reset statistics."""
        self.results = {}
        self.stats = {
            "total_extractors": len(self.extractors),
            "successful_extractions": 0,
            "failed_extractions": 0,
            "start_time": None,
            "end_time": None,
            "duration": None
        }
        logger.info("Extraction results cleared")
