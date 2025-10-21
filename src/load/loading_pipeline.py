"""
Loading pipeline orchestrator for coordinating multiple data loaders.
"""
import pandas as pd
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from .base_loader import BaseLoader
from .database_loader import DatabaseLoader
from .file_loader import FileLoader
from ..utils.config import config
from ..utils.logging import logger

class LoadingPipeline:
    """Orchestrator for managing multiple data loaders."""
    
    def __init__(self):
        self.logger = logger.getChild("pipeline")
        self.loaders: List[BaseLoader] = []
        self.results: Dict[str, bool] = {}
        self.stats: Dict[str, Any] = {}
    
    def add_loader(self, loader: BaseLoader) -> None:
        """
        Add a loader to the pipeline.
        
        Args:
            loader: Loader to add
        """
        self.loaders.append(loader)
        self.logger.info(f"Added loader: {loader.name}")
    
    def run_loadings(self, data: pd.DataFrame, destinations: Dict[str, str] = None) -> bool:
        """
        Run all loaders and return success status.
        
        Args:
            data: DataFrame to load
            destinations: Dictionary mapping loader names to destinations
            
        Returns:
            True if at least one loading succeeded, False otherwise
        """
        self.logger.info(f"Starting loading pipeline for {len(data)} records")
        
        successful_loadings = 0
        failed_loadings = 0
        
        for loader in self.loaders:
            try:
                self.logger.info(f"Running loader: {loader.name}")
                
                # Get destination for this loader
                destination = None
                if destinations and loader.name in destinations:
                    destination = destinations[loader.name]
                
                # Validate data
                if not loader.validate(data):
                    self.logger.error(f"Validation failed: {loader.name}")
                    failed_loadings += 1
                    continue
                
                # Load data
                success = loader.load(data, destination)
                
                if success:
                    self.results[loader.name] = True
                    successful_loadings += 1
                    self.logger.info(f"Loading successful: {loader.name}")
                else:
                    self.results[loader.name] = False
                    failed_loadings += 1
                    self.logger.error(f"Loading failed: {loader.name}")
                    
            except Exception as e:
                self.logger.error(f"Loading failed for {loader.name}: {e}")
                self.results[loader.name] = False
                failed_loadings += 1
                continue
        
        # Update stats
        self.stats["successful_loadings"] = successful_loadings
        self.stats["failed_loadings"] = failed_loadings
        self.stats["total_loaders"] = len(self.loaders)
        
        success = successful_loadings > 0
        self.logger.info(f"Loading pipeline completed: {successful_loadings} successful, {failed_loadings} failed")
        return success
    
    def get_loading_summary(self) -> Dict[str, Any]:
        """
        Get summary of all loadings.
        
        Returns:
            Summary dictionary
        """
        summary = {
            "total_loaders": len(self.loaders),
            "successful_loadings": sum(1 for success in self.results.values() if success),
            "failed_loadings": sum(1 for success in self.results.values() if not success),
            "loaders": {}
        }
        
        for name, success in self.results.items():
            summary["loaders"][name] = {
                "success": success,
                "status": "successful" if success else "failed"
            }
        
        return summary
    
    def save_loading_logs(self, output_dir: Path = None) -> None:
        """
        Save loading logs to file.
        
        Args:
            output_dir: Directory to save logs
        """
        if output_dir is None:
            output_dir = Path(config.processed_data_dir)
        
        log_data = {
            "summary": self.get_loading_summary(),
            "results": self.results,
            "stats": self.stats
        }
        
        log_file = output_dir / "loading_logs.json"
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        self.logger.info(f"Loading logs saved to {log_file}")
    
    def get_loader_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics from all loaders.
        
        Returns:
            Dictionary of loader statistics
        """
        stats = {}
        for loader in self.loaders:
            if hasattr(loader, 'get_stats'):
                stats[loader.name] = loader.get_stats()
        return stats
    
    def test_all_connections(self) -> Dict[str, bool]:
        """
        Test connections for all loaders.
        
        Returns:
            Dictionary mapping loader names to connection status
        """
        connection_results = {}
        
        for loader in self.loaders:
            try:
                if hasattr(loader, 'test_connection'):
                    connection_results[loader.name] = loader.test_connection()
                else:
                    connection_results[loader.name] = True  # Assume OK if no test method
            except Exception as e:
                self.logger.error(f"Connection test failed for {loader.name}: {e}")
                connection_results[loader.name] = False
        
        return connection_results
