#!/usr/bin/env python3
"""Validate n8n workflow files."""

import json
import os
from pathlib import Path

def validate_n8n_workflow():
    """Validate the n8n workflow export file."""
    project_root = Path(__file__).parent
    n8n_file = project_root / "n8n_workflow_export.json"
    
    print("🔍 Validating n8n Workflow Files")
    print("=" * 50)
    
    # Check if n8n files exist
    n8n_files = [
        "n8n_workflow_export.json",
        "n8n_workflow_documentation.md", 
        "n8n_workflow_canvas_description.md",
        "n8n_setup_guide.md",
        "implementation_comparison.md"
    ]
    
    for file_name in n8n_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"✅ {file_name}: File exists")
        else:
            print(f"❌ {file_name}: File missing")
    
    # Validate JSON structure
    try:
        with open(n8n_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"\n📊 n8n Workflow Validation:")
        print(f"✅ JSON is valid")
        print(f"📋 Workflow Name: {data.get('name', 'Unknown')}")
        print(f"🔧 Total Nodes: {len(data.get('nodes', []))}")
        print(f"🔗 Total Connections: {len(data.get('connections', {}))}")
        print(f"🏷️ Tags: {len(data.get('tags', []))}")
        
        # Validate node types
        nodes = data.get('nodes', [])
        node_types = {}
        for node in nodes:
            node_type = node.get('type', 'unknown')
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        print(f"\n🔧 Node Types:")
        for node_type, count in node_types.items():
            print(f"   • {node_type}: {count}")
        
        # Check for required node types
        required_types = [
            'n8n-nodes-base.emailReadImap',
            'n8n-nodes-base.googleSheets', 
            'n8n-nodes-base.emailSend',
            'n8n-nodes-base.code',
            'n8n-nodes-base.if'
        ]
        
        print(f"\n✅ Required Node Types:")
        for req_type in required_types:
            if req_type in node_types:
                print(f"   ✅ {req_type}: Present")
            else:
                print(f"   ❌ {req_type}: Missing")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON validation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def validate_documentation():
    """Validate documentation files."""
    project_root = Path(__file__).parent
    
    print(f"\n📚 Documentation Validation:")
    
    docs = {
        "README.md": "Main project documentation",
        "walkthrough.md": "Python implementation guide", 
        "n8n_workflow_documentation.md": "n8n workflow guide",
        "n8n_setup_guide.md": "n8n setup instructions",
        "implementation_comparison.md": "Implementation comparison",
        "PROJECT_SUMMARY.md": "Executive summary",
        "DELIVERABLES_SUMMARY.md": "Deliverables overview"
    }
    
    for doc_file, description in docs.items():
        file_path = project_root / doc_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                word_count = len(content.split())
                print(f"✅ {doc_file}: {description} ({word_count} words)")
            except UnicodeDecodeError:
                print(f"⚠️ {doc_file}: Encoding issue detected")
        else:
            print(f"❌ {doc_file}: Missing")

if __name__ == "__main__":
    print("🚀 Starting n8n and Documentation Validation\n")
    
    workflow_valid = validate_n8n_workflow()
    validate_documentation()
    
    print(f"\n{'='*50}")
    if workflow_valid:
        print("✅ n8n Workflow Validation: PASSED")
    else:
        print("❌ n8n Workflow Validation: FAILED")
    
    print("🎉 Validation Complete!")