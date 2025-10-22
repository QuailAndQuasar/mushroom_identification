"""
Data cleanup script for maintenance and storage management.
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.config import config
from src.utils.logging import logger

def cleanup_old_logs(days_to_keep: int = 30) -> int:
    """
    Clean up old log files.
    
    Args:
        days_to_keep: Number of days of logs to keep
        
    Returns:
        Number of files deleted
    """
    try:
        log_dir = Path("logs")
        if not log_dir.exists():
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        for log_file in log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink()
                deleted_count += 1
                logger.info(f"Deleted old log file: {log_file}")
        
        return deleted_count
    except Exception as e:
        logger.error(f"Log cleanup failed: {e}")
        return 0

def cleanup_temp_files() -> int:
    """
    Clean up temporary files.
    
    Returns:
        Number of files deleted
    """
    try:
        temp_patterns = ["*.tmp", "*.temp", "*_temp_*"]
        deleted_count = 0
        
        # Check data directories
        data_dirs = [
            Path(config.raw_data_dir),
            Path(config.processed_data_dir),
            Path("logs")
        ]
        
        for data_dir in data_dirs:
            if data_dir.exists():
                for pattern in temp_patterns:
                    for temp_file in data_dir.glob(pattern):
                        temp_file.unlink()
                        deleted_count += 1
                        logger.info(f"Deleted temp file: {temp_file}")
        
        return deleted_count
    except Exception as e:
        logger.error(f"Temp file cleanup failed: {e}")
        return 0

def cleanup_old_data(days_to_keep: int = 90) -> int:
    """
    Clean up old processed data files.
    
    Args:
        days_to_keep: Number of days of data to keep
        
    Returns:
        Number of files deleted
    """
    try:
        processed_dir = Path(config.processed_data_dir)
        if not processed_dir.exists():
            return 0
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        # Clean up old parquet files
        for data_file in processed_dir.glob("*.parquet"):
            if data_file.stat().st_mtime < cutoff_date.timestamp():
                data_file.unlink()
                deleted_count += 1
                logger.info(f"Deleted old data file: {data_file}")
        
        return deleted_count
    except Exception as e:
        logger.error(f"Data cleanup failed: {e}")
        return 0

def main():
    """Main function for data cleanup."""
    parser = argparse.ArgumentParser(description="Clean up old data and files")
    parser.add_argument(
        "--logs-days",
        type=int,
        default=30,
        help="Number of days of logs to keep"
    )
    parser.add_argument(
        "--data-days",
        type=int,
        default=90,
        help="Number of days of data to keep"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting"
    )
    
    args = parser.parse_args()
    
    print("🧹 Data Cleanup")
    print("=" * 50)
    
    if args.dry_run:
        print("DRY RUN MODE - No files will be deleted")
        print("=" * 50)
    
    # Clean up old logs
    print(f"Cleaning up logs older than {args.logs_days} days...")
    if not args.dry_run:
        log_count = cleanup_old_logs(args.logs_days)
        print(f"Deleted {log_count} log files")
    else:
        print("Would clean up old log files")
    
    # Clean up temp files
    print("Cleaning up temporary files...")
    if not args.dry_run:
        temp_count = cleanup_temp_files()
        print(f"Deleted {temp_count} temporary files")
    else:
        print("Would clean up temporary files")
    
    # Clean up old data
    print(f"Cleaning up data older than {args.data_days} days...")
    if not args.dry_run:
        data_count = cleanup_old_data(args.data_days)
        print(f"Deleted {data_count} data files")
    else:
        print("Would clean up old data files")
    
    print("\n✅ Cleanup completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
