#!/usr/bin/env python3
"""
Quick demo runner for the Mushroom ETL Pipeline.
"""

import subprocess
import sys
from pathlib import Path

def run_demo():
    """Run the ETL pipeline demo."""
    print("🍄 Starting Mushroom ETL Pipeline Demo...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("src").exists():
        print("❌ Please run this from the project root directory")
        return
    
    try:
        # Run the demo script
        result = subprocess.run([
            sys.executable, "scripts/demo_pipeline.py"
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ Demo completed successfully!")
        else:
            print(f"\n⚠️  Demo completed with warnings (exit code: {result.returncode})")
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    run_demo()
