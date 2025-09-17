#!/usr/bin/env python3
"""Final comprehensive validation of the entire project."""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_command(command):
    """Run a command and return success status."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def validate_python_implementation():
    """Validate Python implementation."""
    print("🐍 PYTHON IMPLEMENTATION VALIDATION")
    print("=" * 50)
    
    results = {}
    
    # Test imports
    try:
        from config.settings import settings
        from models.candidate import Candidate
        from services.email_processor import EmailProcessor
        from services.keyword_screener import KeywordScreener
        from services.sheets_manager import SheetsManager
        from services.email_templates import EmailTemplates
        from workflow.orchestrator import WorkflowOrchestrator
        
        print("✅ All Python modules import successfully")
        results['imports'] = True
    except Exception as e:
        print(f"❌ Import error: {e}")
        results['imports'] = False
    
    # Test service instantiation
    try:
        orchestrator = WorkflowOrchestrator()
        print("✅ WorkflowOrchestrator instantiates successfully")
        print(f"📊 Initial stats: {orchestrator.stats}")
        results['services'] = True
    except Exception as e:
        print(f"❌ Service instantiation error: {e}")
        results['services'] = False
    
    # Run unit tests
    success, stdout, stderr = run_command("python run_tests.py")
    if success:
        # Count tests from output
        lines = stdout.split('\n')
        test_count = 0
        for line in lines:
            if 'ok' in line and 'test_' in line:
                test_count += 1
        print(f"✅ Unit tests: {test_count} tests passed")
        results['tests'] = True
        results['test_count'] = test_count
    else:
        print(f"❌ Unit tests failed: {stderr}")
        results['tests'] = False
        results['test_count'] = 0
    
    # Test main.py functionality
    success, stdout, stderr = run_command("python main.py test")
    if success:
        print("✅ Main workflow test passed")
        results['workflow_test'] = True
    else:
        print(f"❌ Main workflow test failed: {stderr}")
        results['workflow_test'] = False
    
    return results

def validate_n8n_implementation():
    """Validate n8n implementation."""
    print("\n🎨 N8N IMPLEMENTATION VALIDATION")
    print("=" * 50)
    
    results = {}
    
    # Check n8n files exist
    n8n_files = [
        "n8n_workflow_export.json",
        "n8n_workflow_documentation.md",
        "n8n_workflow_canvas_description.md", 
        "n8n_setup_guide.md",
        "implementation_comparison.md"
    ]
    
    missing_files = []
    for file_name in n8n_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}: Present")
        else:
            print(f"❌ {file_name}: Missing")
            missing_files.append(file_name)
    
    results['files_present'] = len(missing_files) == 0
    results['missing_files'] = missing_files
    
    # Validate JSON structure
    try:
        with open("n8n_workflow_export.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        nodes = data.get('nodes', [])
        connections = data.get('connections', {})
        
        print(f"✅ n8n JSON is valid")
        print(f"📋 Workflow: {data.get('name', 'Unknown')}")
        print(f"🔧 Nodes: {len(nodes)}")
        print(f"🔗 Connections: {len(connections)}")
        
        # Check for required node types
        node_types = [node.get('type', '') for node in nodes]
        required_types = [
            'n8n-nodes-base.emailReadImap',
            'n8n-nodes-base.googleSheets',
            'n8n-nodes-base.emailSend',
            'n8n-nodes-base.code',
            'n8n-nodes-base.if'
        ]
        
        missing_types = [t for t in required_types if t not in node_types]
        if not missing_types:
            print("✅ All required node types present")
            results['node_types'] = True
        else:
            print(f"❌ Missing node types: {missing_types}")
            results['node_types'] = False
        
        results['json_valid'] = True
        results['node_count'] = len(nodes)
        results['connection_count'] = len(connections)
        
    except Exception as e:
        print(f"❌ n8n JSON validation failed: {e}")
        results['json_valid'] = False
        results['node_count'] = 0
        results['connection_count'] = 0
    
    return results

def validate_documentation():
    """Validate documentation."""
    print("\n📚 DOCUMENTATION VALIDATION")
    print("=" * 50)
    
    results = {}
    
    docs = {
        "README.md": "Main project documentation",
        "walkthrough.md": "Python implementation guide",
        "n8n_workflow_documentation.md": "n8n workflow guide", 
        "n8n_setup_guide.md": "n8n setup instructions",
        "implementation_comparison.md": "Implementation comparison",
        "PROJECT_SUMMARY.md": "Executive summary",
        "DELIVERABLES_SUMMARY.md": "Deliverables overview"
    }
    
    total_words = 0
    missing_docs = []
    
    for doc_file, description in docs.items():
        if Path(doc_file).exists():
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                word_count = len(content.split())
                total_words += word_count
                print(f"✅ {doc_file}: {word_count} words")
            except UnicodeDecodeError:
                print(f"⚠️ {doc_file}: Encoding issue")
        else:
            print(f"❌ {doc_file}: Missing")
            missing_docs.append(doc_file)
    
    results['total_words'] = total_words
    results['missing_docs'] = missing_docs
    results['docs_complete'] = len(missing_docs) == 0
    
    return results

def validate_project_structure():
    """Validate project structure."""
    print("\n📁 PROJECT STRUCTURE VALIDATION")
    print("=" * 50)
    
    required_structure = {
        'files': [
            'main.py', 'requirements.txt', 'setup.py', '.env.example',
            'run_tests.py', '.gitignore'
        ],
        'directories': [
            'config', 'models', 'services', 'workflow', 'tests', 'scripts', 'docker'
        ]
    }
    
    results = {'missing_files': [], 'missing_dirs': []}
    
    # Check files
    for file_name in required_structure['files']:
        if Path(file_name).exists():
            print(f"✅ {file_name}: Present")
        else:
            print(f"❌ {file_name}: Missing")
            results['missing_files'].append(file_name)
    
    # Check directories
    for dir_name in required_structure['directories']:
        if Path(dir_name).is_dir():
            print(f"✅ {dir_name}/: Present")
        else:
            print(f"❌ {dir_name}/: Missing")
            results['missing_dirs'].append(dir_name)
    
    results['structure_complete'] = (
        len(results['missing_files']) == 0 and 
        len(results['missing_dirs']) == 0
    )
    
    return results

def generate_final_report(python_results, n8n_results, doc_results, structure_results):
    """Generate final validation report."""
    print("\n" + "=" * 60)
    print("🎯 FINAL VALIDATION REPORT")
    print("=" * 60)
    
    # Calculate overall scores
    python_score = sum([
        python_results.get('imports', False),
        python_results.get('services', False), 
        python_results.get('tests', False),
        python_results.get('workflow_test', False)
    ])
    
    n8n_score = sum([
        n8n_results.get('files_present', False),
        n8n_results.get('json_valid', False),
        n8n_results.get('node_types', False)
    ])
    
    doc_score = doc_results.get('docs_complete', False)
    structure_score = structure_results.get('structure_complete', False)
    
    total_score = python_score + n8n_score + doc_score + structure_score
    max_score = 9  # 4 + 3 + 1 + 1
    
    print(f"📊 OVERALL SCORE: {total_score}/{max_score} ({total_score/max_score*100:.1f}%)")
    print()
    
    # Python Implementation
    print(f"🐍 Python Implementation: {python_score}/4")
    print(f"   ✅ Module Imports: {'✓' if python_results.get('imports') else '✗'}")
    print(f"   ✅ Service Instantiation: {'✓' if python_results.get('services') else '✗'}")
    print(f"   ✅ Unit Tests ({python_results.get('test_count', 0)} tests): {'✓' if python_results.get('tests') else '✗'}")
    print(f"   ✅ Workflow Test: {'✓' if python_results.get('workflow_test') else '✗'}")
    print()
    
    # n8n Implementation  
    print(f"🎨 n8n Implementation: {n8n_score}/3")
    print(f"   ✅ All Files Present: {'✓' if n8n_results.get('files_present') else '✗'}")
    print(f"   ✅ JSON Valid ({n8n_results.get('node_count', 0)} nodes): {'✓' if n8n_results.get('json_valid') else '✗'}")
    print(f"   ✅ Required Node Types: {'✓' if n8n_results.get('node_types') else '✗'}")
    print()
    
    # Documentation
    print(f"📚 Documentation: {1 if doc_score else 0}/1")
    print(f"   ✅ All Docs Present ({doc_results.get('total_words', 0)} words): {'✓' if doc_score else '✗'}")
    print()
    
    # Project Structure
    print(f"📁 Project Structure: {1 if structure_score else 0}/1")
    print(f"   ✅ Complete Structure: {'✓' if structure_score else '✗'}")
    print()
    
    # Final Status
    if total_score == max_score:
        status = "🎉 EXCELLENT"
        color = "✅"
    elif total_score >= max_score * 0.8:
        status = "👍 GOOD"  
        color = "✅"
    elif total_score >= max_score * 0.6:
        status = "⚠️ FAIR"
        color = "⚠️"
    else:
        status = "❌ NEEDS WORK"
        color = "❌"
    
    print(f"{color} PROJECT STATUS: {status}")
    print(f"📅 Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return {
        'overall_score': total_score,
        'max_score': max_score,
        'percentage': total_score/max_score*100,
        'status': status,
        'python_results': python_results,
        'n8n_results': n8n_results,
        'doc_results': doc_results,
        'structure_results': structure_results
    }

if __name__ == "__main__":
    print("🚀 COMPREHENSIVE PROJECT VALIDATION")
    print("=" * 60)
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all validations
    python_results = validate_python_implementation()
    n8n_results = validate_n8n_implementation()
    doc_results = validate_documentation()
    structure_results = validate_project_structure()
    
    # Generate final report
    final_report = generate_final_report(
        python_results, n8n_results, doc_results, structure_results
    )
    
    # Save report to file
    with open("final_validation_report.json", 'w') as f:
        json.dump(final_report, f, indent=2, default=str)
    
    print(f"\n📄 Detailed report saved to: final_validation_report.json")
    print("🎉 Validation Complete!")