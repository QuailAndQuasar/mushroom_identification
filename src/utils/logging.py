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
    log_file = Path(config.logging.file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.logging.level.upper()),
        format=config.logging.format,
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