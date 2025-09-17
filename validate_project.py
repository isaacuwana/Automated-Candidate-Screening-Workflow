"""
Comprehensive validation script for the Automated Candidate Screening Workflow.
This script validates the entire project structure, dependencies, and functionality.
"""

import os
import sys
import json
import importlib
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


class ProjectValidator:
    """Validates the complete project setup and functionality."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.validation_results = []
        self.errors = []
        self.warnings = []
        
    def log_result(self, test_name: str, status: str, message: str = "", details: Any = None):
        """Log validation result."""
        result = {
            'test': test_name,
            'status': status,  # 'PASS', 'FAIL', 'WARN'
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.validation_results.append(result)
        
        # Print result
        status_icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}.get(status, "❓")
        print(f"{status_icon} {test_name}: {message}")
        
        if status == "FAIL":
            self.errors.append(f"{test_name}: {message}")
        elif status == "WARN":
            self.warnings.append(f"{test_name}: {message}")
    
    def validate_python_version(self) -> bool:
        """Validate Python version compatibility."""
        try:
            if sys.version_info >= (3, 8):
                self.log_result("Python Version", "PASS", f"Python {sys.version.split()[0]} is compatible")
                return True
            else:
                self.log_result("Python Version", "FAIL", f"Python {sys.version.split()[0]} < 3.8 (required)")
                return False
        except Exception as e:
            self.log_result("Python Version", "FAIL", f"Error checking Python version: {e}")
            return False
    
    def validate_project_structure(self) -> bool:
        """Validate project directory structure."""
        required_files = [
            'main.py',
            'requirements.txt',
            'setup.py',
            '.env.example',
            'walkthrough.md',
            'workflow_export.json',
            'run_tests.py',
            '.gitignore'
        ]
        
        required_directories = [
            'config',
            'models', 
            'services',
            'workflow',
            'tests',
            'scripts',
            'docker'
        ]
        
        all_valid = True
        
        # Check required files
        for file_path in required_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                self.log_result(f"File: {file_path}", "PASS", "File exists")
            else:
                self.log_result(f"File: {file_path}", "FAIL", "File missing")
                all_valid = False
        
        # Check required directories
        for dir_path in required_directories:
            full_path = self.project_root / dir_path
            if full_path.exists() and full_path.is_dir():
                self.log_result(f"Directory: {dir_path}", "PASS", "Directory exists")
            else:
                self.log_result(f"Directory: {dir_path}", "FAIL", "Directory missing")
                all_valid = False
        
        return all_valid
    
    def validate_python_modules(self) -> bool:
        """Validate that all Python modules can be imported."""
        modules_to_test = [
            ('config.settings', 'Configuration module'),
            ('models.candidate', 'Data models'),
            ('services.email_processor', 'Email processing service'),
            ('services.keyword_screener', 'Keyword screening service'),
            ('services.sheets_manager', 'Google Sheets service'),
            ('services.email_templates', 'Email templates service'),
            ('workflow.orchestrator', 'Workflow orchestrator')
        ]
        
        all_valid = True
        
        # Add project root to Python path
        sys.path.insert(0, str(self.project_root))
        
        for module_name, description in modules_to_test:
            try:
                importlib.import_module(module_name)
                self.log_result(f"Import: {module_name}", "PASS", f"{description} imports successfully")
            except ImportError as e:
                self.log_result(f"Import: {module_name}", "FAIL", f"Import failed: {e}")
                all_valid = False
            except Exception as e:
                self.log_result(f"Import: {module_name}", "FAIL", f"Unexpected error: {e}")
                all_valid = False
        
        return all_valid
    
    def validate_dependencies(self) -> bool:
        """Validate that all required dependencies are available."""
        requirements_file = self.project_root / 'requirements.txt'
        
        if not requirements_file.exists():
            self.log_result("Dependencies", "FAIL", "requirements.txt not found")
            return False
        
        try:
            with open(requirements_file, 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            missing_packages = []
            
            for requirement in requirements:
                # Extract package name (handle version specifiers)
                package_name = requirement.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0].split('!=')[0]
                
                try:
                    importlib.import_module(package_name.replace('-', '_'))
                except ImportError:
                    try:
                        # Try alternative import names
                        if package_name == 'google-api-python-client':
                            importlib.import_module('googleapiclient')
                        elif package_name == 'google-auth-oauthlib':
                            importlib.import_module('google_auth_oauthlib')
                        elif package_name == 'google-auth-httplib2':
                            importlib.import_module('google_auth_httplib2')
                        elif package_name == 'google-auth':
                            importlib.import_module('google.auth')
                        elif package_name == 'python-dotenv':
                            importlib.import_module('dotenv')
                        elif package_name == 'pydantic-settings':
                            importlib.import_module('pydantic_settings')
                        else:
                            raise ImportError(f"Cannot import {package_name}")
                    except ImportError:
                        missing_packages.append(package_name)
            
            if missing_packages:
                self.log_result("Dependencies", "FAIL", f"Missing packages: {', '.join(missing_packages)}")
                return False
            else:
                self.log_result("Dependencies", "PASS", f"All {len(requirements)} dependencies available")
                return True
                
        except Exception as e:
            self.log_result("Dependencies", "FAIL", f"Error checking dependencies: {e}")
            return False
    
    def validate_configuration_files(self) -> bool:
        """Validate configuration files."""
        all_valid = True
        
        # Check .env.example
        env_example = self.project_root / '.env.example'
        if env_example.exists():
            try:
                content = env_example.read_text()
                required_vars = ['EMAIL_USERNAME', 'EMAIL_PASSWORD', 'CANDIDATE_TRACKER_SHEET_ID']
                
                missing_vars = [var for var in required_vars if var not in content]
                
                if missing_vars:
                    self.log_result("Config: .env.example", "WARN", f"Missing variables: {', '.join(missing_vars)}")
                else:
                    self.log_result("Config: .env.example", "PASS", "All required variables present")
                    
            except Exception as e:
                self.log_result("Config: .env.example", "FAIL", f"Error reading file: {e}")
                all_valid = False
        else:
            self.log_result("Config: .env.example", "FAIL", "File not found")
            all_valid = False
        
        # Check workflow_export.json
        workflow_export = self.project_root / 'workflow_export.json'
        if workflow_export.exists():
            try:
                with open(workflow_export, 'r') as f:
                    data = json.load(f)
                
                required_keys = ['workflow_name', 'workflow_steps', 'configuration']
                missing_keys = [key for key in required_keys if key not in data]
                
                if missing_keys:
                    self.log_result("Config: workflow_export.json", "WARN", f"Missing keys: {', '.join(missing_keys)}")
                else:
                    self.log_result("Config: workflow_export.json", "PASS", "Valid workflow specification")
                    
            except json.JSONDecodeError as e:
                self.log_result("Config: workflow_export.json", "FAIL", f"Invalid JSON: {e}")
                all_valid = False
            except Exception as e:
                self.log_result("Config: workflow_export.json", "FAIL", f"Error reading file: {e}")
                all_valid = False
        else:
            self.log_result("Config: workflow_export.json", "FAIL", "File not found")
            all_valid = False
        
        return all_valid
    
    def validate_docker_setup(self) -> bool:
        """Validate Docker configuration."""
        dockerfile = self.project_root / 'docker' / 'Dockerfile'
        compose_file = self.project_root / 'docker' / 'docker-compose.yml'
        
        all_valid = True
        
        if dockerfile.exists():
            try:
                content = dockerfile.read_text()
                if 'FROM python:' in content and 'COPY requirements.txt' in content:
                    self.log_result("Docker: Dockerfile", "PASS", "Valid Dockerfile structure")
                else:
                    self.log_result("Docker: Dockerfile", "WARN", "Dockerfile may be incomplete")
            except Exception as e:
                self.log_result("Docker: Dockerfile", "FAIL", f"Error reading Dockerfile: {e}")
                all_valid = False
        else:
            self.log_result("Docker: Dockerfile", "FAIL", "Dockerfile not found")
            all_valid = False
        
        if compose_file.exists():
            try:
                content = compose_file.read_text()
                if 'services:' in content and 'candidate-screening:' in content:
                    self.log_result("Docker: docker-compose.yml", "PASS", "Valid compose file structure")
                else:
                    self.log_result("Docker: docker-compose.yml", "WARN", "Compose file may be incomplete")
            except Exception as e:
                self.log_result("Docker: docker-compose.yml", "FAIL", f"Error reading compose file: {e}")
                all_valid = False
        else:
            self.log_result("Docker: docker-compose.yml", "FAIL", "docker-compose.yml not found")
            all_valid = False
        
        return all_valid
    
    def validate_test_suite(self) -> bool:
        """Validate test suite functionality."""
        test_runner = self.project_root / 'run_tests.py'
        
        if not test_runner.exists():
            self.log_result("Test Suite", "FAIL", "run_tests.py not found")
            return False
        
        # Check if test files exist
        test_files = list((self.project_root / 'tests').glob('test_*.py'))
        
        if not test_files:
            self.log_result("Test Suite", "WARN", "No test files found")
            return False
        
        self.log_result("Test Suite", "PASS", f"Found {len(test_files)} test files")
        
        # Try to run tests (with timeout)
        try:
            result = subprocess.run([
                sys.executable, str(test_runner)
            ], capture_output=True, text=True, timeout=60, cwd=self.project_root)
            
            if result.returncode == 0:
                self.log_result("Test Execution", "PASS", "All tests passed")
                return True
            else:
                self.log_result("Test Execution", "WARN", f"Some tests failed: {result.stdout}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_result("Test Execution", "WARN", "Tests timed out after 60 seconds")
            return False
        except Exception as e:
            self.log_result("Test Execution", "WARN", f"Could not run tests: {e}")
            return False
    
    def validate_scripts(self) -> bool:
        """Validate utility scripts."""
        scripts_to_check = [
            ('setup_environment.py', 'Environment setup script'),
            ('deploy.py', 'Deployment script'),
            ('monitor.py', 'Monitoring script')
        ]
        
        all_valid = True
        
        for script_name, description in scripts_to_check:
            script_path = self.project_root / 'scripts' / script_name
            
            if script_path.exists():
                try:
                    # Check if script has main function or can be executed
                    content = script_path.read_text()
                    if 'def main(' in content or 'if __name__ == \'__main__\':' in content:
                        self.log_result(f"Script: {script_name}", "PASS", f"{description} is executable")
                    else:
                        self.log_result(f"Script: {script_name}", "WARN", f"{description} may not be executable")
                except Exception as e:
                    self.log_result(f"Script: {script_name}", "FAIL", f"Error reading script: {e}")
                    all_valid = False
            else:
                self.log_result(f"Script: {script_name}", "FAIL", f"{description} not found")
                all_valid = False
        
        return all_valid
    
    def validate_main_entry_point(self) -> bool:
        """Validate main.py entry point."""
        main_file = self.project_root / 'main.py'
        
        if not main_file.exists():
            self.log_result("Main Entry Point", "FAIL", "main.py not found")
            return False
        
        try:
            content = main_file.read_text()
            
            # Check for required components
            required_components = [
                ('import argparse', 'Command line argument parsing'),
                ('def main(', 'Main function'),
                ('if __name__ == "__main__":', 'Script execution guard')
            ]
            
            all_present = True
            for component, description in required_components:
                if component in content:
                    self.log_result(f"Main: {description}", "PASS", "Component present")
                else:
                    self.log_result(f"Main: {description}", "WARN", "Component missing")
                    all_present = False
            
            return all_present
            
        except Exception as e:
            self.log_result("Main Entry Point", "FAIL", f"Error reading main.py: {e}")
            return False
    
    def validate_documentation(self) -> bool:
        """Validate documentation completeness."""
        docs_to_check = [
            ('README.md', 'Main project documentation'),
            ('walkthrough.md', 'Setup and usage guide'),
            ('PROJECT_SUMMARY.md', 'Project summary')
        ]
        
        all_valid = True
        
        for doc_name, description in docs_to_check:
            doc_path = self.project_root / doc_name
            
            if doc_path.exists():
                try:
                    content = doc_path.read_text()
                    word_count = len(content.split())
                    
                    if word_count > 100:  # Reasonable documentation should have substantial content
                        self.log_result(f"Docs: {doc_name}", "PASS", f"{description} ({word_count} words)")
                    else:
                        self.log_result(f"Docs: {doc_name}", "WARN", f"{description} seems incomplete ({word_count} words)")
                        
                except Exception as e:
                    self.log_result(f"Docs: {doc_name}", "FAIL", f"Error reading {doc_name}: {e}")
                    all_valid = False
            else:
                self.log_result(f"Docs: {doc_name}", "FAIL", f"{description} not found")
                all_valid = False
        
        return all_valid
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run all validation checks."""
        print("🔍 Starting Comprehensive Project Validation")
        print("=" * 60)
        
        validation_functions = [
            ("Python Version", self.validate_python_version),
            ("Project Structure", self.validate_project_structure),
            ("Python Modules", self.validate_python_modules),
            ("Dependencies", self.validate_dependencies),
            ("Configuration Files", self.validate_configuration_files),
            ("Docker Setup", self.validate_docker_setup),
            ("Test Suite", self.validate_test_suite),
            ("Utility Scripts", self.validate_scripts),
            ("Main Entry Point", self.validate_main_entry_point),
            ("Documentation", self.validate_documentation)
        ]
        
        passed_tests = 0
        total_tests = len(validation_functions)
        
        for test_name, test_function in validation_functions:
            print(f"\n📋 Validating: {test_name}")
            print("-" * 40)
            
            try:
                result = test_function()
                if result:
                    passed_tests += 1
            except Exception as e:
                self.log_result(test_name, "FAIL", f"Validation error: {e}")
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"✅ Passed: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print(f"❌ Errors: {len(self.errors)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        
        if self.errors:
            print("\n❌ CRITICAL ERRORS:")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        # Overall status
        if success_rate >= 90 and len(self.errors) == 0:
            status = "EXCELLENT"
            print(f"\n🎉 PROJECT STATUS: {status}")
            print("   The project is in excellent condition and ready for production!")
        elif success_rate >= 80 and len(self.errors) <= 2:
            status = "GOOD"
            print(f"\n✅ PROJECT STATUS: {status}")
            print("   The project is in good condition with minor issues to address.")
        elif success_rate >= 60:
            status = "NEEDS_IMPROVEMENT"
            print(f"\n⚠️  PROJECT STATUS: {status}")
            print("   The project needs some improvements before production deployment.")
        else:
            status = "CRITICAL_ISSUES"
            print(f"\n❌ PROJECT STATUS: {status}")
            print("   The project has critical issues that must be resolved.")
        
        # Save validation report
        report = {
            'validation_timestamp': datetime.now().isoformat(),
            'overall_status': status,
            'success_rate': success_rate,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'errors': self.errors,
            'warnings': self.warnings,
            'detailed_results': self.validation_results
        }
        
        report_file = self.project_root / 'validation_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed validation report saved to: {report_file}")
        
        return report


def main():
    """Main validation function."""
    validator = ProjectValidator()
    report = validator.run_comprehensive_validation()
    
    # Exit with appropriate code
    if report['overall_status'] in ['EXCELLENT', 'GOOD']:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()