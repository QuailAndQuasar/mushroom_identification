#!/usr/bin/env python3
"""
Tests for Dead Code Analyzer

This module tests the dead code detection functionality.
"""

import pytest
import json
import tempfile
import ast
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent.parent / "scripts"))

from dead_code_analyzer import DeadCodeAnalyzer


class TestDeadCodeAnalyzer:
    """Test cases for DeadCodeAnalyzer class"""
    
    @pytest.fixture
    def temp_project_dir(self):
        """Create a temporary project directory with test files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test Python files
            test_file1 = temp_path / "test_module1.py"
            test_file1.write_text("""
def used_function():
    return "used"

def unused_function():
    return "unused"

class UsedClass:
    def method(self):
        return "used"

class UnusedClass:
    def method(self):
        return "unused"

if __name__ == "__main__":
    used_function()
    obj = UsedClass()
""")
            
            test_file2 = temp_path / "test_module2.py"
            test_file2.write_text("""
import os
import sys
from pathlib import Path

def another_function():
    return "another"

# This function is never called
def dead_function():
    return "dead"
""")
            
            test_file3 = temp_path / "test_module3.py"
            test_file3.write_text("""
# This file imports from test_module1
from test_module1 import used_function, UsedClass

def main():
    used_function()
    obj = UsedClass()
""")
            
            yield temp_path
    
    def test_initialization(self, temp_project_dir):
        """Test DeadCodeAnalyzer initialization"""
        analyzer = DeadCodeAnalyzer(str(temp_project_dir))
        
        assert analyzer.project_root == temp_project_dir
        assert len(analyzer.all_python_files) == 3
        assert analyzer.all_functions == {}
        assert analyzer.all_classes == {}
        assert analyzer.all_imports == {}
    
    def test_parse_all_files(self, temp_project_dir):
        """Test parsing of all Python files"""
        analyzer = DeadCodeAnalyzer(str(temp_project_dir))
        analyzer._parse_all_files()
        
        # Check that files were parsed
        assert len(analyzer.all_functions) == 3
        assert len(analyzer.all_classes) == 3
        assert len(analyzer.all_imports) == 3
        
        # Check specific file contents
        module1_path = str(temp_project_dir / "test_module1.py")
        assert "used_function" in analyzer.all_functions[module1_path]
        assert "unused_function" in analyzer.all_functions[module1_path]
        assert "UsedClass" in analyzer.all_classes[module1_path]
        assert "UnusedClass" in analyzer.all_classes[module1_path]
    
    def test_analyze_usage(self, temp_project_dir):
        """Test usage analysis"""
        analyzer = DeadCodeAnalyzer(str(temp_project_dir))
        analyzer._parse_all_files()
        analyzer._analyze_usage()
        
        # Check that used functions are identified
        assert "used_function" in analyzer.used_functions
        assert "UsedClass" in analyzer.used_classes
        
        # Check that unused functions are not in used set
        assert "unused_function" not in analyzer.used_functions
        assert "UnusedClass" not in analyzer.used_classes
    
    def test_analyze_imports(self, temp_project_dir):
        """Test import analysis"""
        analyzer = DeadCodeAnalyzer(str(temp_project_dir))
        analyzer._parse_all_files()
        analyzer._analyze_imports()
        
        # Check that used variable names are identified (not import names)
        assert "used_function" in analyzer.used_imports
        assert "UsedClass" in analyzer.used_imports
    
    def test_generate_report(self, temp_project_dir):
        """Test report generation"""
        analyzer = DeadCodeAnalyzer(str(temp_project_dir))
        analyzer._parse_all_files()
        analyzer._analyze_usage()
        analyzer._analyze_imports()
        
        report = analyzer._generate_report()
        
        # Check report structure
        assert "summary" in report
        assert "unused_functions" in report
        assert "unused_classes" in report
        assert "unused_imports" in report
        assert "potentially_unused_files" in report
        assert "file_analysis" in report
        
        # Check summary
        assert report["summary"]["total_files"] == 3
        assert report["summary"]["total_functions"] > 0
        assert report["summary"]["total_classes"] > 0
        
        # Check that unused functions are identified
        unused_functions = report["unused_functions"]
        assert len(unused_functions) > 0
        
        # Find unused_function in the report
        unused_function_found = any(
            item["function"] == "unused_function" 
            for item in unused_functions
        )
        assert unused_function_found
    
    def test_is_file_imported(self, temp_project_dir):
        """Test file import detection"""
        analyzer = DeadCodeAnalyzer(str(temp_project_dir))
        analyzer._parse_all_files()
        
        # test_module1.py should be imported by test_module3.py
        module1_path = str(temp_project_dir / "test_module1.py")
        assert analyzer._is_file_imported(module1_path) is True
        
        # test_module2.py should not be imported
        module2_path = str(temp_project_dir / "test_module2.py")
        assert analyzer._is_file_imported(module2_path) is False
    
    def test_analyze_codebase(self, temp_project_dir):
        """Test complete codebase analysis"""
        analyzer = DeadCodeAnalyzer(str(temp_project_dir))
        report = analyzer.analyze_codebase()
        
        # Check that analysis completed successfully
        assert "summary" in report
        assert "unused_functions" in report
        assert "unused_classes" in report
        assert "unused_imports" in report
        
        # Check that unused code was found
        assert len(report["unused_functions"]) > 0
        assert len(report["unused_classes"]) > 0
    
    def test_print_report(self, temp_project_dir, capsys):
        """Test report printing"""
        analyzer = DeadCodeAnalyzer(str(temp_project_dir))
        report = analyzer.analyze_codebase()
        analyzer.print_report(report)
        
        captured = capsys.readouterr()
        output = captured.out
        
        # Check that report was printed
        assert "DEAD CODE ANALYSIS REPORT" in output
        assert "Total Files:" in output
        assert "Total Functions:" in output
        assert "Total Classes:" in output
        assert "UNUSED FUNCTIONS:" in output
        assert "UNUSED CLASSES:" in output
        assert "RECOMMENDATIONS:" in output


class TestDeadCodeAnalyzerEdgeCases:
    """Test edge cases for DeadCodeAnalyzer"""
    
    def test_empty_directory(self):
        """Test analysis of empty directory"""
        with tempfile.TemporaryDirectory() as temp_dir:
            analyzer = DeadCodeAnalyzer(temp_dir)
            report = analyzer.analyze_codebase()
            
            assert report["summary"]["total_files"] == 0
            assert len(report["unused_functions"]) == 0
            assert len(report["unused_classes"]) == 0
    
    def test_syntax_error_in_file(self):
        """Test handling of files with syntax errors"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create file with syntax error
            bad_file = temp_path / "bad_syntax.py"
            bad_file.write_text("def broken_function(\n    return 'missing colon'")
            
            analyzer = DeadCodeAnalyzer(str(temp_path))
            
            # Should not raise exception
            report = analyzer.analyze_codebase()
            assert "summary" in report
    
    def test_non_python_files(self):
        """Test handling of non-Python files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create non-Python files
            text_file = temp_path / "readme.txt"
            text_file.write_text("This is a text file")
            
            json_file = temp_path / "config.json"
            json_file.write_text('{"key": "value"}')
            
            # Create one Python file
            py_file = temp_path / "test.py"
            py_file.write_text("def test_function():\n    return 'test'")
            
            analyzer = DeadCodeAnalyzer(str(temp_path))
            report = analyzer.analyze_codebase()
            
            # Should only find the Python file
            assert report["summary"]["total_files"] == 1
    
    def test_import_with_alias(self):
        """Test handling of imports with aliases"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create file with aliased imports
            test_file = temp_path / "test_imports.py"
            test_file.write_text("""
import pandas as pd
import numpy as np
from pathlib import Path as P

def test_function():
    df = pd.DataFrame()
    arr = np.array([1, 2, 3])
    path = P("test")
""")
            
            analyzer = DeadCodeAnalyzer(str(temp_path))
            analyzer._parse_all_files()
            analyzer._analyze_imports()
            
            # Check that aliased imports are recognized as variable names
            assert "pd" in analyzer.used_imports
            assert "np" in analyzer.used_imports
            assert "P" in analyzer.used_imports


class TestDeadCodeAnalyzerIntegration:
    """Integration tests for DeadCodeAnalyzer"""
    
    def test_end_to_end_analysis(self):
        """Test complete end-to-end analysis workflow"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a realistic project structure
            main_file = temp_path / "main.py"
            main_file.write_text("""
from utils import helper_function
from models import Model

def main():
    helper_function()
    model = Model()
    model.train()

if __name__ == "__main__":
    main()
""")
            
            utils_file = temp_path / "utils.py"
            utils_file.write_text("""
def helper_function():
    return "help"

def unused_helper():
    return "unused"
""")
            
            models_file = temp_path / "models.py"
            models_file.write_text("""
class Model:
    def train(self):
        return "training"
    
    def predict(self):
        return "prediction"

class UnusedModel:
    def method(self):
        return "unused"
""")
            
            analyzer = DeadCodeAnalyzer(str(temp_path))
            report = analyzer.analyze_codebase()
            
            # Verify analysis results
            assert report["summary"]["total_files"] == 3
            
            # Check that unused code is identified
            unused_functions = [item["function"] for item in report["unused_functions"]]
            assert "unused_helper" in unused_functions
            
            unused_classes = [item["class"] for item in report["unused_classes"]]
            assert "UnusedModel" in unused_classes
            
            # Check that used code is not flagged as unused
            assert "helper_function" not in unused_functions
            assert "Model" not in unused_classes


if __name__ == "__main__":
    pytest.main([__file__])
