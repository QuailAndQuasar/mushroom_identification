#!/usr/bin/env python3
"""
Comprehensive Dead Code Detection Agent

This script analyzes the entire codebase to identify unused code, functions, imports, and files.
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
import json
import importlib.util

class DeadCodeAnalyzer:
    """Comprehensive dead code detection agent"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.all_python_files = list(self.project_root.rglob("*.py"))
        self.all_functions = {}  # file -> functions
        self.all_classes = {}    # file -> classes
        self.all_imports = {}    # file -> imports
        self.used_functions = set()
        self.used_classes = set()
        self.used_imports = set()
        
    def analyze_codebase(self) -> Dict[str, Any]:
        """Perform comprehensive dead code analysis"""
        print("🔍 DEAD CODE ANALYSIS")
        print("=" * 60)
        
        # Step 1: Parse all Python files
        print("📁 Step 1: Parsing Python files...")
        self._parse_all_files()
        
        # Step 2: Find function/class usage
        print("🔍 Step 2: Analyzing function and class usage...")
        self._analyze_usage()
        
        # Step 3: Find unused imports
        print("📦 Step 3: Analyzing import usage...")
        self._analyze_imports()
        
        # Step 4: Generate report
        print("📊 Step 4: Generating analysis report...")
        report = self._generate_report()
        
        return report
    
    def _parse_all_files(self):
        """Parse all Python files to extract functions, classes, and imports"""
        for file_path in self.all_python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Extract functions
                functions = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append(node.name)
                
                # Extract classes
                classes = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        classes.append(node.name)
                
                # Extract imports
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                imports.append(alias.name)
                        else:  # ImportFrom
                            if node.module:
                                imports.append(node.module)
                            for alias in node.names:
                                imports.append(alias.name)
                
                self.all_functions[str(file_path)] = functions
                self.all_classes[str(file_path)] = classes
                self.all_imports[str(file_path)] = imports
                
            except Exception as e:
                print(f"⚠️  Error parsing {file_path}: {e}")
    
    def _analyze_usage(self):
        """Analyze which functions and classes are actually used"""
        for file_path in self.all_python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find function calls
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            self.used_functions.add(node.func.id)
                        elif isinstance(node.func, ast.Attribute):
                            self.used_functions.add(node.func.attr)
                
                # Find class instantiations
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name):
                            self.used_classes.add(node.func.id)
                
            except Exception as e:
                print(f"⚠️  Error analyzing usage in {file_path}: {e}")
    
    def _analyze_imports(self):
        """Analyze which imports are actually used"""
        for file_path in self.all_python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                tree = ast.parse(content)
                
                # Find all name references
                for node in ast.walk(tree):
                    if isinstance(node, ast.Name):
                        self.used_imports.add(node.id)
                    elif isinstance(node, ast.Attribute):
                        # Extract the base name from attribute access
                        if isinstance(node.value, ast.Name):
                            self.used_imports.add(node.value.id)
                
            except Exception as e:
                print(f"⚠️  Error analyzing imports in {file_path}: {e}")
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive dead code report"""
        report = {
            "summary": {
                "total_files": len(self.all_python_files),
                "total_functions": sum(len(funcs) for funcs in self.all_functions.values()),
                "total_classes": sum(len(classes) for classes in self.all_classes.values()),
                "total_imports": sum(len(imports) for imports in self.all_imports.values())
            },
            "unused_functions": [],
            "unused_classes": [],
            "unused_imports": [],
            "potentially_unused_files": [],
            "file_analysis": {}
        }
        
        # Analyze each file
        for file_path in self.all_python_files:
            file_str = str(file_path)
            functions = self.all_functions.get(file_str, [])
            classes = self.all_classes.get(file_str, [])
            imports = self.all_imports.get(file_str, [])
            
            file_analysis = {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "unused_functions": [],
                "unused_classes": [],
                "unused_imports": []
            }
            
            # Find unused functions in this file
            for func in functions:
                if func not in self.used_functions and not func.startswith('_'):
                    file_analysis["unused_functions"].append(func)
                    report["unused_functions"].append({
                        "file": file_str,
                        "function": func
                    })
            
            # Find unused classes in this file
            for cls in classes:
                if cls not in self.used_classes and not cls.startswith('_'):
                    file_analysis["unused_classes"].append(cls)
                    report["unused_classes"].append({
                        "file": file_str,
                        "class": cls
                    })
            
            # Find unused imports in this file
            for imp in imports:
                if imp not in self.used_imports and not imp.startswith('_'):
                    file_analysis["unused_imports"].append(imp)
                    report["unused_imports"].append({
                        "file": file_str,
                        "import": imp
                    })
            
            report["file_analysis"][file_str] = file_analysis
            
            # Check if file might be unused
            if (not file_analysis["unused_functions"] and 
                not file_analysis["unused_classes"] and 
                len(functions) + len(classes) > 0):
                # File has code but might not be imported/used
                if not self._is_file_imported(file_str):
                    report["potentially_unused_files"].append(file_str)
        
        return report
    
    def _is_file_imported(self, file_path: str) -> bool:
        """Check if a file is imported by other files"""
        file_name = Path(file_path).stem
        
        for other_file in self.all_python_files:
            if str(other_file) == file_path:
                continue
                
            try:
                with open(other_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for imports of this module
                if f"import {file_name}" in content or f"from {file_name}" in content:
                    return True
                    
            except Exception:
                continue
        
        return False
    
    def print_report(self, report: Dict[str, Any]):
        """Print formatted analysis report"""
        print("\n📊 DEAD CODE ANALYSIS REPORT")
        print("=" * 60)
        
        # Summary
        summary = report["summary"]
        print(f"📁 Total Files: {summary['total_files']}")
        print(f"🔧 Total Functions: {summary['total_functions']}")
        print(f"🏗️  Total Classes: {summary['total_classes']}")
        print(f"📦 Total Imports: {summary['total_imports']}")
        print()
        
        # Unused functions
        if report["unused_functions"]:
            print("❌ UNUSED FUNCTIONS:")
            for item in report["unused_functions"][:10]:  # Show first 10
                print(f"  - {Path(item['file']).name}: {item['function']}")
            if len(report["unused_functions"]) > 10:
                print(f"  ... and {len(report['unused_functions']) - 10} more")
            print()
        
        # Unused classes
        if report["unused_classes"]:
            print("❌ UNUSED CLASSES:")
            for item in report["unused_classes"][:10]:  # Show first 10
                print(f"  - {Path(item['file']).name}: {item['class']}")
            if len(report["unused_classes"]) > 10:
                print(f"  ... and {len(report['unused_classes']) - 10} more")
            print()
        
        # Unused imports
        if report["unused_imports"]:
            print("❌ UNUSED IMPORTS:")
            for item in report["unused_imports"][:10]:  # Show first 10
                print(f"  - {Path(item['file']).name}: {item['import']}")
            if len(report["unused_imports"]) > 10:
                print(f"  ... and {len(report['unused_imports']) - 10} more")
            print()
        
        # Potentially unused files
        if report["potentially_unused_files"]:
            print("⚠️  POTENTIALLY UNUSED FILES:")
            for file_path in report["potentially_unused_files"][:5]:  # Show first 5
                print(f"  - {Path(file_path).name}")
            if len(report["potentially_unused_files"]) > 5:
                print(f"  ... and {len(report['potentially_unused_files']) - 5} more")
            print()
        
        # Recommendations
        print("💡 RECOMMENDATIONS:")
        total_unused = (len(report["unused_functions"]) + 
                       len(report["unused_classes"]) + 
                       len(report["unused_imports"]))
        
        if total_unused == 0:
            print("  ✅ No significant dead code found! Your codebase is clean.")
        elif total_unused < 10:
            print("  🟡 Minor cleanup recommended. Consider removing unused code.")
        else:
            print("  🔴 Significant cleanup needed. Many unused functions/imports found.")
        
        print()

def main():
    """Run dead code analysis"""
    print("🔍 Starting Dead Code Analysis...")
    
    analyzer = DeadCodeAnalyzer()
    report = analyzer.analyze_codebase()
    analyzer.print_report(report)
    
    # Save detailed report
    report_file = "dead_code_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Detailed report saved to: {report_file}")

if __name__ == "__main__":
    main()
