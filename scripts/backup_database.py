"""
Database backup script for production maintenance.
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime
import shutil

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.config import config
from src.utils.logging import logger

def backup_database(backup_dir: str = "backups") -> bool:
    """
    Backup the database to a specified directory.
    
    Args:
        backup_dir: Directory to store backup files
        
    Returns:
        True if backup successful, False otherwise
    """
    try:
        # Create backup directory if it doesn't exist
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"mushroom_etl_backup_{timestamp}.db"
        backup_file = backup_path / backup_filename
        
        # Extract database file path from URL
        db_url = config.database_url
        if db_url.startswith("sqlite:///"):
            db_file = db_url.replace("sqlite:///", "")
            db_path = Path(db_file)
            
            if db_path.exists():
                # Copy database file
                shutil.copy2(db_path, backup_file)
                logger.info(f"Database backed up to: {backup_file}")
                return True
            else:
                logger.error(f"Database file not found: {db_path}")
                return False
        else:
            logger.error("Backup only supported for SQLite databases")
            return False
            
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return False

def main():
    """Main function for database backup."""
    parser = argparse.ArgumentParser(description="Backup database")
    parser.add_argument(
        "--backup-dir",
        default="backups",
        help="Directory to store backup files"
    )
    
    args = parser.parse_args()
    
    print("💾 Database Backup")
    print("=" * 50)
    
    success = backup_database(args.backup_dir)
    
    if success:
        print("✅ Database backup completed successfully!")
        return 0
    else:
        print("❌ Database backup failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
