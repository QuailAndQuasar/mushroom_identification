"""
Configuration loader for the ETL pipeline.
"""
import yaml
from pathlib import Path
from typing import Dict, Any
from .config import ETLConfig

def load_yaml_config(config_file: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def merge_configs(base_config: ETLConfig, yaml_config: Dict[str, Any]) -> ETLConfig:
    """Merge YAML configuration with base configuration."""
    # This is a simplified merge - in production you'd want more sophisticated merging
    for key, value in yaml_config.items():
        if hasattr(base_config, key):
            setattr(base_config, key, value)
    
    return base_config

def get_config(config_file: str = None) -> ETLConfig:
    """Get configuration instance."""
    if config_file:
        config_path = Path(config_file)
        yaml_config = load_yaml_config(config_path)
        return merge_configs(ETLConfig(), yaml_config)
    
    return ETLConfig()