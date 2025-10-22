"""
Logging configuration for the ETL pipeline.
"""
import logging
import sys
from pathlib import Path
from .config import config

def setup_logging():
    """Set up logging configuration."""
    # Create logs directory if it doesn't exist
    log_file = Path(config.log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format=config.log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger
    logger = logging.getLogger("mushroom_etl")
    logger.info("Logging configured successfully")
    
    return logger

# Global logger instance
logger = setup_logging()