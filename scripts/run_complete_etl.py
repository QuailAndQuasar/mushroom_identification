"""
Complete ETL pipeline runner for end-to-end validation.
"""
import sys
import argparse
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.orchestration.etl_pipeline import ETLPipeline
from src.extract.uci_mushroom_extractor import UCIMushroomExtractor
from src.transform.data_cleaner import DataCleaner
from src.transform.feature_engineer import FeatureEngineer
from src.load.database_loader import DatabaseLoader
from src.load.file_loader import FileLoader
from src.utils.config import config
from src.utils.logging import logger

def run_complete_etl(mode: str = "development") -> bool:
    """
    Run the complete ETL pipeline.
    
    Args:
        mode: Pipeline mode (development, production)
        
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"Starting complete ETL pipeline in {mode} mode")
    
    try:
        # Initialize ETL pipeline
        pipeline = ETLPipeline()
        
        # Configure extraction
        logger.info("Configuring extraction stage")
        extractor = UCIMushroomExtractor()
        pipeline.configure_extraction([extractor])
        
        # Configure transformation
        logger.info("Configuring transformation stage")
        cleaner = DataCleaner({
            "handle_missing": "drop",
            "remove_duplicates": True,
            "standardize_text": True
        })
        engineer = FeatureEngineer({
            "categorical_encoding": "onehot",
            "feature_scaling": True,
            "feature_selection": True,
            "n_features": 20
        })
        pipeline.configure_transformation([cleaner, engineer])
        
        # Configure loading
        logger.info("Configuring loading stage")
        db_loader = DatabaseLoader({
            "table_name": "mushroom_data",
            "if_exists": "replace"
        })
        file_loader = FileLoader({
            "file_format": "csv",
            "output_dir": str(config.processed_data_dir)
        })
        pipeline.configure_loading([db_loader, file_loader])
        
        # Run pipeline
        logger.info("Running complete ETL pipeline")
        success = pipeline.run_pipeline()
        
        if success:
            logger.info("ETL pipeline completed successfully!")
            
            # Print pipeline statistics
            stats = pipeline.get_pipeline_stats()
            print("\n" + "="*50)
            print("ETL PIPELINE STATISTICS")
            print("="*50)
            print(f"Pipeline ID: {stats['pipeline_id']}")
            print(f"Status: {stats['status']}")
            print(f"Start Time: {stats['start_time']}")
            print(f"End Time: {stats['end_time']}")
            
            # Print stage statistics
            for stage_name, stage_stats in stats['stages'].items():
                print(f"\n{stage_name.upper()} STAGE:")
                if stage_stats.get('success'):
                    print(f"  Status: SUCCESS")
                    if 'input_records' in stage_stats:
                        print(f"  Input Records: {stage_stats['input_records']}")
                    if 'output_records' in stage_stats:
                        print(f"  Output Records: {stage_stats['output_records']}")
                    if 'records_loaded' in stage_stats:
                        print(f"  Records Loaded: {stage_stats['records_loaded']}")
                else:
                    print(f"  Status: FAILED")
                    if 'error' in stage_stats:
                        print(f"  Error: {stage_stats['error']}")
            
            # Save pipeline logs
            pipeline.save_pipeline_logs()
            print(f"\nPipeline logs saved to {config.processed_data_dir}")
            
            return True
        else:
            logger.error("ETL pipeline failed!")
            return False
            
    except Exception as e:
        logger.error(f"ETL pipeline failed with error: {e}")
        return False

def validate_pipeline_output() -> bool:
    """
    Validate pipeline output data.
    
    Returns:
        True if validation passed, False otherwise
    """
    logger.info("Validating pipeline output")
    
    try:
        # Check if output files exist
        output_dir = Path(config.processed_data_dir)
        
        # Check for database
        db_file = Path("data/mushroom_etl.db")
        if db_file.exists():
            logger.info(f"Database file found: {db_file}")
        else:
            logger.warning("Database file not found")
        
        # Check for output files
        parquet_files = list(output_dir.glob("*.parquet"))
        if parquet_files:
            logger.info(f"Parquet files found: {len(parquet_files)}")
        else:
            logger.warning("No parquet files found")
        
        # Check for log files
        log_files = list(output_dir.glob("*_pipeline_logs.json"))
        if log_files:
            logger.info(f"Log files found: {len(log_files)}")
        else:
            logger.warning("No log files found")
        
        return True
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return False

def main():
    """Main function for running complete ETL pipeline."""
    parser = argparse.ArgumentParser(description="Run complete ETL pipeline")
    parser.add_argument(
        "--mode",
        choices=["development", "production"],
        default="development",
        help="Pipeline mode"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate pipeline output"
    )
    
    args = parser.parse_args()
    
    print("🍄 Mushroom ETL Pipeline")
    print("=" * 50)
    print(f"Mode: {args.mode}")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Run pipeline
    success = run_complete_etl(args.mode)
    
    if success:
        print("\n✅ ETL Pipeline completed successfully!")
        
        # Validate output if requested
        if args.validate:
            print("\n🔍 Validating pipeline output...")
            validation_success = validate_pipeline_output()
            if validation_success:
                print("✅ Pipeline output validation passed!")
            else:
                print("❌ Pipeline output validation failed!")
                return 1
    else:
        print("\n❌ ETL Pipeline failed!")
        return 1
    
    print(f"\nEnd Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())