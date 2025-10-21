"""
Dependency validation script for the ETL pipeline.
"""
import importlib
import sys
from pathlib import Path

def validate_dependencies():
    """Validate that all required dependencies are installed and working."""
    print("🔍 Validating project dependencies...")
    
    # Required packages with their import names (PyArrow temporarily removed)
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'scikit-learn': 'sklearn',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'sqlalchemy': 'sqlalchemy',
        'pydantic': 'pydantic',
        'requests': 'requests',
        'pytest': 'pytest',
        'jupyter': 'jupyter'
    }
    
    missing_packages = []
    version_issues = []
    
    for package_name, import_name in required_packages.items():
        try:
            # Try to import the package
            module = importlib.import_module(import_name)
            
            # Check version if available
            if hasattr(module, '__version__'):
                version = module.__version__
                print(f"✅ {package_name}: {version}")
            else:
                print(f"✅ {package_name}: installed")
                
        except ImportError:
            missing_packages.append(package_name)
            print(f"❌ {package_name}: not installed")
    
    # Check for version conflicts
    try:
        import pandas as pd
        import numpy as np
        import sklearn
        
        # Test basic functionality
        df = pd.DataFrame({'test': [1, 2, 3]})
        arr = np.array([1, 2, 3])
        
        print("✅ Basic functionality test passed")
        
    except Exception as e:
        version_issues.append(f"Functionality test failed: {e}")
        print(f"❌ Functionality test failed: {e}")
    
    # Summary
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    if version_issues:
        print(f"\n⚠️  Version issues: {', '.join(version_issues)}")
        return False
    
    print("\n🎉 All dependencies validated successfully!")
    print("Note: PyArrow is temporarily skipped due to build issues")
    return True

if __name__ == "__main__":
    validate_dependencies()