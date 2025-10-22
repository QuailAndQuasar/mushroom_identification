"""
Pipeline health checker for monitoring and validation.
"""
import sys
import argparse
from pathlib import Path
import json
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.config import config
from src.utils.logging import logger

def check_database_health() -> dict:
    """Check database health and connectivity."""
    try:
        from sqlalchemy import create_engine, text
        
        engine = create_engine(config.database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        
        return {
            "status": "healthy",
            "message": "Database connection successful",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {e}",
            "timestamp": datetime.now().isoformat()
        }

def check_file_system_health() -> dict:
    """Check file system health and permissions."""
    try:
        # Check data directories
        directories = [
            config.raw_data_dir,
            config.processed_data_dir,
            config.models_dir,
            "logs"
        ]
        
        results = {}
        for directory in directories:
            path = Path(directory)
            if path.exists():
                results[directory] = {
                    "exists": True,
                    "writable": path.is_dir() and path.stat().st_mode & 0o200
                }
            else:
                results[directory] = {"exists": False, "writable": False}
        
        all_healthy = all(result["exists"] and result["writable"] for result in results.values())
        
        return {
            "status": "healthy" if all_healthy else "unhealthy",
            "directories": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"File system check failed: {e}",
            "timestamp": datetime.now().isoformat()
        }

def check_dependencies() -> dict:
    """Check if all required dependencies are available."""
    try:
        required_modules = [
            "pandas", "numpy", "sklearn", "sqlalchemy", 
            "requests", "pydantic", "pytest"
        ]
        
        results = {}
        for module in required_modules:
            try:
                __import__(module)
                results[module] = {"available": True}
            except ImportError:
                results[module] = {"available": False}
        
        all_available = all(result["available"] for result in results.values())
        
        return {
            "status": "healthy" if all_available else "unhealthy",
            "modules": results,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Dependency check failed: {e}",
            "timestamp": datetime.now().isoformat()
        }

def check_pipeline_health() -> dict:
    """Check overall pipeline health."""
    logger.info("Checking pipeline health...")
    
    health_report = {
        "overall_status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {}
    }
    
    # Run health checks
    health_report["checks"]["database"] = check_database_health()
    health_report["checks"]["file_system"] = check_file_system_health()
    health_report["checks"]["dependencies"] = check_dependencies()
    
    # Determine overall status
    unhealthy_checks = [
        check for check in health_report["checks"].values() 
        if check["status"] == "unhealthy"
    ]
    
    if unhealthy_checks:
        health_report["overall_status"] = "unhealthy"
        health_report["issues"] = len(unhealthy_checks)
    
    return health_report

def main():
    """Main function for health checking."""
    parser = argparse.ArgumentParser(description="Check pipeline health")
    parser.add_argument(
        "--output",
        choices=["console", "json", "file"],
        default="console",
        help="Output format"
    )
    parser.add_argument(
        "--output-file",
        default="pipeline_health.json",
        help="Output file for JSON format"
    )
    
    args = parser.parse_args()
    
    print("🔍 Pipeline Health Check")
    print("=" * 50)
    
    # Run health check
    health_report = check_pipeline_health()
    
    if args.output == "console":
        print(f"Overall Status: {health_report['overall_status'].upper()}")
        print(f"Timestamp: {health_report['timestamp']}")
        
        for check_name, check_result in health_report["checks"].items():
            status_icon = "✅" if check_result["status"] == "healthy" else "❌"
            print(f"\n{status_icon} {check_name.upper()}: {check_result['status']}")
            if "message" in check_result:
                print(f"   {check_result['message']}")
    
    elif args.output == "json":
        print(json.dumps(health_report, indent=2))
    
    elif args.output == "file":
        with open(args.output_file, 'w') as f:
            json.dump(health_report, f, indent=2)
        print(f"Health report saved to {args.output_file}")
    
    # Exit with appropriate code
    if health_report["overall_status"] == "healthy":
        print("\n✅ All health checks passed!")
        return 0
    else:
        print(f"\n❌ {health_report.get('issues', 0)} health check(s) failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
