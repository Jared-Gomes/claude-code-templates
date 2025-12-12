#!/usr/bin/env python3
"""
Test script to verify all paths in marketplace.json are valid.
This ensures no "Path not found" errors when installing plugins.
"""

import json
import os
import sys
from pathlib import Path

def test_marketplace_paths():
    """Verify all paths in marketplace.json point to existing files."""
    
    # Load marketplace.json
    marketplace_path = Path('.claude-plugin/marketplace.json')
    if not marketplace_path.exists():
        print(f"❌ Error: {marketplace_path} not found")
        return False
    
    with open(marketplace_path, 'r') as f:
        data = json.load(f)
    
    print("🔍 Testing marketplace.json paths...\n")
    
    all_valid = True
    plugin_results = []
    
    for plugin in data['plugins']:
        plugin_name = plugin['name']
        plugin_valid = True
        missing = []
        valid = []
        
        # Check commands
        if 'commands' in plugin:
            for cmd_path in plugin['commands']:
                if os.path.exists(cmd_path):
                    valid.append(('command', cmd_path))
                else:
                    missing.append(('command', cmd_path))
                    plugin_valid = False
                    all_valid = False
        
        # Check agents
        if 'agents' in plugin:
            for agent_path in plugin['agents']:
                if os.path.exists(agent_path):
                    valid.append(('agent', agent_path))
                else:
                    missing.append(('agent', agent_path))
                    plugin_valid = False
                    all_valid = False
        
        # Check mcpServers
        if 'mcpServers' in plugin:
            for mcp_path in plugin['mcpServers']:
                if os.path.exists(mcp_path):
                    valid.append(('mcp', mcp_path))
                else:
                    missing.append(('mcp', mcp_path))
                    plugin_valid = False
                    all_valid = False
        
        plugin_results.append({
            'name': plugin_name,
            'valid': plugin_valid,
            'missing': missing,
            'valid_count': len(valid),
            'total_count': len(valid) + len(missing)
        })
    
    # Print results
    print("=" * 80)
    print("RESULTS BY PLUGIN")
    print("=" * 80)
    
    for result in plugin_results:
        status = "✅" if result['valid'] else "❌"
        print(f"\n{status} {result['name']}")
        print(f"   Valid paths: {result['valid_count']}/{result['total_count']}")
        
        if result['missing']:
            print(f"   Missing files:")
            for file_type, path in result['missing']:
                print(f"      • [{file_type}] {path}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    total_plugins = len(plugin_results)
    valid_plugins = sum(1 for r in plugin_results if r['valid'])
    total_files = sum(r['total_count'] for r in plugin_results)
    valid_files = sum(r['valid_count'] for r in plugin_results)
    
    print(f"Plugins: {valid_plugins}/{total_plugins} valid")
    print(f"Files: {valid_files}/{total_files} valid")
    
    if all_valid:
        print("\n✅ SUCCESS: All paths in marketplace.json are valid!")
        return True
    else:
        print("\n❌ FAILURE: Some paths are invalid and need to be fixed")
        return False

if __name__ == '__main__':
    success = test_marketplace_paths()
    sys.exit(0 if success else 1)
