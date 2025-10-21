"""
Automated setup script for the ETL pipeline project.
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_project():
    """Set up the project environment."""
    print("🚀 Setting up ETL Pipeline Project...")
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not in a virtual environment. Consider creating one first.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return False
    
    # Install core dependencies
    if not run_command("pip install -r requirements.txt", "Installing core dependencies"):
        print("⚠️  Some dependencies failed to install. Trying individual packages...")
        
        # Try installing key packages individually
        key_packages = [
            "pandas>=2.0.0",
            "numpy>=1.24.0", 
            "scikit-learn>=1.3.0",
            "sqlalchemy>=2.0.0",
            "pydantic>=2.0.0",
            "pytest>=7.4.0"
        ]
        
        for package in key_packages:
            if not run_command(f"pip install {package}", f"Installing {package}"):
                print(f"⚠️  Failed to install {package}")
    
    # Verify installation with a more robust test
    print("🔍 Verifying installation...")
    try:
        import pandas, numpy, sklearn, sqlalchemy, pydantic, pytest
        print("✅ All packages imported successfully!")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("Please check your requirements.txt and try again.")
        return False
    
    print("🎉 Project setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate your virtual environment")
    print("2. Run: python scripts/validate_setup.py")
    print("3. Start developing your ETL pipeline!")
    print("\nNote: PyArrow is temporarily skipped due to build issues")
    
    return True

if __name__ == "__main__":
    setup_project()