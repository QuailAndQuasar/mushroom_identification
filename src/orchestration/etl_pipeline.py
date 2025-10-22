"""
ETL Pipeline orchestrator for coordinating extraction, transformation, and loading.
"""
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import json

from ..extract.extraction_orchestrator import ExtractionOrchestrator
from ..transform.transformation_pipeline import TransformationPipeline
from ..load.loading_pipeline import LoadingPipeline
from ..utils.config import config
from ..utils.logging import logger

class ETLPipeline:
    """Main ETL pipeline orchestrator."""
    
    def __init__(self, pipeline_config: Dict[str, Any] = None):
        """
        Initialize ETL pipeline.
        
        Args:
            pipeline_config: Pipeline configuration dictionary
        """
        self.logger = logger.getChild("etl_pipeline")
        self.config = pipeline_config or {}
        
        # Initialize pipeline components
        self.extraction_orchestrator = ExtractionOrchestrator()
        self.transformation_pipeline = TransformationPipeline()
        self.loading_pipeline = LoadingPipeline()
        
        # Pipeline state
        self.pipeline_id = f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.stats = {
            "pipeline_id": self.pipeline_id,
            "start_time": None,
            "end_time": None,
            "status": "initialized",
            "stages": {}
        }
    
    def configure_extraction(self, extractors: List[Any]) -> None:
        """
        Configure extraction stage.
        
        Args:
            extractors: List of extractor instances
        """
        for extractor in extractors:
            self.extraction_orchestrator.add_extractor(extractor)
        self.logger.info(f"Configured {len(extractors)} extractors")
    
    def configure_transformation(self, transformers: List[Any]) -> None:
        """
        Configure transformation stage.
        
        Args:
            transformers: List of transformer instances
        """
        for transformer in transformers:
            self.transformation_pipeline.add_transformer(transformer)
        self.logger.info(f"Configured {len(transformers)} transformers")
    
    def configure_loading(self, loaders: List[Any]) -> None:
        """
        Configure loading stage.
        
        Args:
            loaders: List of loader instances
        """
        for loader in loaders:
            self.loading_pipeline.add_loader(loader)
        self.logger.info(f"Configured {len(loaders)} loaders")
    
    def run_pipeline(self, extraction_config: Dict[str, Any] = None) -> bool:
        """
        Run the complete ETL pipeline.
        
        Args:
            extraction_config: Configuration for extraction stage
            
        Returns:
            True if pipeline completed successfully, False otherwise
        """
        self.logger.info(f"Starting ETL pipeline: {self.pipeline_id}")
        self.stats["start_time"] = datetime.now().isoformat()
        self.stats["status"] = "running"
        
        try:
            # Stage 1: Extraction
            self.logger.info("Starting extraction stage")
            extraction_success = self._run_extraction_stage(extraction_config)
            
            if not extraction_success:
                self.logger.error("Extraction stage failed")
                self.stats["status"] = "failed"
                self.stats["end_time"] = datetime.now().isoformat()
                return False
            
            # Stage 2: Transformation
            self.logger.info("Starting transformation stage")
            transformation_success = self._run_transformation_stage()
            
            if not transformation_success:
                self.logger.error("Transformation stage failed")
                self.stats["status"] = "failed"
                self.stats["end_time"] = datetime.now().isoformat()
                return False
            
            # Stage 3: Loading
            self.logger.info("Starting loading stage")
            loading_success = self._run_loading_stage()
            
            if not loading_success:
                self.logger.error("Loading stage failed")
                self.stats["status"] = "failed"
                self.stats["end_time"] = datetime.now().isoformat()
                return False
            
            # Pipeline completed successfully
            self.stats["status"] = "completed"
            self.stats["end_time"] = datetime.now().isoformat()
            self.logger.info("ETL pipeline completed successfully")
            
            return True
            
        except Exception as e:
            self.logger.error(f"ETL pipeline failed with unexpected error: {e}")
            self.stats["status"] = "failed"
            self.stats["end_time"] = datetime.now().isoformat()
            self.stats["error"] = str(e)
            return False
    
    def _run_extraction_stage(self, extraction_config: Dict[str, Any] = None) -> bool:
        """Run the extraction stage."""
        try:
            # Run extraction
            extraction_results = self.extraction_orchestrator.run_all_extractions()
            
            if not extraction_results:
                self.logger.error("No data extracted")
                return False
            
            # Store extraction results
            self.stats["stages"]["extraction"] = {
                "success": True,
                "extractors_run": len(extraction_results),
                "total_records": sum(len(df) for df in extraction_results.values()),
                "extraction_summary": self.extraction_orchestrator.get_extraction_summary()
            }
            
            self.logger.info(f"Extraction stage completed: {len(extraction_results)} data sources")
            return True
            
        except Exception as e:
            self.logger.error(f"Extraction stage failed: {e}")
            self.stats["stages"]["extraction"] = {
                "success": False,
                "error": str(e)
            }
            return False
    
    def _run_transformation_stage(self) -> bool:
        """Run the transformation stage."""
        try:
            # Get data from extraction stage
            extraction_results = self.extraction_orchestrator.results
            
            if not extraction_results:
                self.logger.error("No data available for transformation")
                return False
            
            # Combine all extracted data
            combined_data = pd.concat(extraction_results.values(), ignore_index=True)
            
            # Run transformation
            transformed_data = self.transformation_pipeline.run_transformations(combined_data)
            
            if transformed_data.empty:
                self.logger.error("Transformation produced empty data")
                return False
            
            # Store transformation results
            self.stats["stages"]["transformation"] = {
                "success": True,
                "input_records": len(combined_data),
                "output_records": len(transformed_data),
                "transformation_summary": self.transformation_pipeline.get_transformation_summary()
            }
            
            self.logger.info(f"Transformation stage completed: {len(transformed_data)} records")
            return True
            
        except Exception as e:
            self.logger.error(f"Transformation stage failed: {e}")
            self.stats["stages"]["transformation"] = {
                "success": False,
                "error": str(e)
            }
            return False
    
    def _run_loading_stage(self) -> bool:
        """Run the loading stage."""
        try:
            # Get transformed data
            transformed_data = self.transformation_pipeline.results.get("feature_engineer")
            
            if transformed_data is None or transformed_data.empty:
                self.logger.error("No transformed data available for loading")
                return False
            
            # Run loading
            loading_success = self.loading_pipeline.run_loadings(transformed_data)
            
            if not loading_success:
                self.logger.error("Loading stage failed")
                return False
            
            # Store loading results
            self.stats["stages"]["loading"] = {
                "success": True,
                "records_loaded": len(transformed_data),
                "loading_summary": self.loading_pipeline.get_loading_summary()
            }
            
            self.logger.info(f"Loading stage completed: {len(transformed_data)} records loaded")
            return True
            
        except Exception as e:
            self.logger.error(f"Loading stage failed: {e}")
            self.stats["stages"]["loading"] = {
                "success": False,
                "error": str(e)
            }
            return False
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive pipeline statistics.
        
        Returns:
            Dictionary of pipeline statistics
        """
        return self.stats
    
    def save_pipeline_logs(self, output_dir: Path = None) -> None:
        """
        Save pipeline logs and statistics.
        
        Args:
            output_dir: Directory to save logs
        """
        if output_dir is None:
            output_dir = Path(config.processed_data_dir)
        
        # Save pipeline logs
        log_file = output_dir / f"{self.pipeline_id}_pipeline_logs.json"
        with open(log_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        
        self.logger.info(f"Pipeline logs saved to {log_file}")
    
    def get_pipeline_health(self) -> Dict[str, Any]:
        """
        Get pipeline health status.
        
        Returns:
            Dictionary of pipeline health information
        """
        health = {
            "pipeline_id": self.pipeline_id,
            "status": self.stats["status"],
            "stages_completed": len([stage for stage in self.stats["stages"].values() if stage.get("success", False)]),
            "total_stages": 3,
            "overall_health": "healthy" if self.stats["status"] == "completed" else "unhealthy"
        }
        
        return health