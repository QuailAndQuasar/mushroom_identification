"""
Script to run all tests.
"""
import subprocess
import sys

def run_tests():
    """Run all tests with pytest."""
    try:
        # Run tests with coverage
        result = subprocess.run([
            "python", "-m", "pytest", 
            "tests/", 
            "-v", 
            "--cov=src", 
            "--cov-report=html",
            "--cov-report=term"
        ], check=True)
        
        print("✅ All tests passed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
