"""
Pipeline statistics viewer for monitoring and analysis.
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

def load_pipeline_logs() -> dict:
    """Load pipeline logs from processed data directory."""
    try:
        log_dir = Path(config.processed_data_dir)
        log_files = list(log_dir.glob("*_pipeline_logs.json"))
        
        if not log_files:
            return {"error": "No pipeline logs found"}
        
        # Load the most recent log file
        latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
        
        with open(latest_log, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"Failed to load pipeline logs: {e}"}

def display_pipeline_stats(stats: dict) -> None:
    """Display pipeline statistics in a formatted way."""
    print("📊 Pipeline Statistics")
    print("=" * 50)
    
    if "error" in stats:
        print(f"❌ Error: {stats['error']}")
        return
    
    # Basic information
    print(f"Pipeline ID: {stats.get('pipeline_id', 'N/A')}")
    print(f"Status: {stats.get('status', 'N/A')}")
    print(f"Start Time: {stats.get('start_time', 'N/A')}")
    print(f"End Time: {stats.get('end_time', 'N/A')}")
    
    # Calculate duration if both times are available
    if 'start_time' in stats and 'end_time' in stats:
        try:
            start = datetime.fromisoformat(stats['start_time'])
            end = datetime.fromisoformat(stats['end_time'])
            duration = end - start
            print(f"Duration: {duration}")
        except:
            print("Duration: Unable to calculate")
    
    # Stage statistics
    if 'stages' in stats:
        print("\n📈 Stage Statistics:")
        for stage_name, stage_stats in stats['stages'].items():
            status_icon = "✅" if stage_stats.get('success', False) else "❌"
            print(f"\n{status_icon} {stage_name.upper()}:")
            
            if stage_stats.get('success'):
                print(f"   Status: SUCCESS")
                if 'input_records' in stage_stats:
                    print(f"   Input Records: {stage_stats['input_records']:,}")
                if 'output_records' in stage_stats:
                    print(f"   Output Records: {stage_stats['output_records']:,}")
                if 'records_loaded' in stage_stats:
                    print(f"   Records Loaded: {stage_stats['records_loaded']:,}")
                if 'processing_time' in stage_stats:
                    print(f"   Processing Time: {stage_stats['processing_time']:.2f}s")
            else:
                print(f"   Status: FAILED")
                if 'error' in stage_stats:
                    print(f"   Error: {stage_stats['error']}")

def display_performance_metrics(stats: dict) -> None:
    """Display performance metrics."""
    print("\n⚡ Performance Metrics")
    print("=" * 50)
    
    if 'stages' not in stats:
        print("No performance data available")
        return
    
    total_records = 0
    total_time = 0
    
    for stage_name, stage_stats in stats['stages'].items():
        if stage_stats.get('success'):
            records = stage_stats.get('output_records', 0)
            time = stage_stats.get('processing_time', 0)
            
            if records > 0 and time > 0:
                throughput = records / time
                print(f"{stage_name}: {throughput:.0f} records/second")
                
                total_records += records
                total_time += time
    
    if total_time > 0:
        overall_throughput = total_records / total_time
        print(f"\nOverall: {overall_throughput:.0f} records/second")

def main():
    """Main function for viewing pipeline statistics."""
    parser = argparse.ArgumentParser(description="View pipeline statistics")
    parser.add_argument(
        "--format",
        choices=["summary", "detailed", "json"],
        default="summary",
        help="Output format"
    )
    parser.add_argument(
        "--performance",
        action="store_true",
        help="Show performance metrics"
    )
    
    args = parser.parse_args()
    
    # Load pipeline statistics
    stats = load_pipeline_logs()
    
    if args.format == "json":
        print(json.dumps(stats, indent=2))
    elif args.format == "summary":
        display_pipeline_stats(stats)
    elif args.format == "detailed":
        display_pipeline_stats(stats)
        if args.performance:
            display_performance_metrics(stats)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())