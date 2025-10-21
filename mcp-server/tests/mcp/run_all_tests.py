#!/usr/bin/env python3
"""
Run All MCP Tests
Runs all MCP-related tests in sequence.
"""

import sys
import subprocess
from pathlib import Path

def run_test(test_file):
    """Run a test file and return success status."""
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    """Run all MCP tests."""
    print("Running All MCP Tests")
    print("=" * 25)
    
    tests = [
        ("Database Connections", "test_database_connections.py"),
        ("MCP Server Verification", "verify_mcp_server.py"),
        ("MCP Tools", "test_mcp_tools.py"),
        ("MCP Resources", "test_mcp_resources.py")
    ]
    
    results = []
    
    for test_name, test_file in tests:
        print(f"\n{'='*50}")
        print(f"Running {test_name} Test")
        print(f"{'='*50}")
        
        success, stdout, stderr = run_test(test_file)
        results.append((test_name, success))
        
        if success:
            print(f"OK {test_name} PASSED")
            if stdout:
                print(stdout)
        else:
            print(f"ERROR {test_name} FAILED")
            if stderr:
                print(f"Error: {stderr}")
            if stdout:
                print(f"Output: {stdout}")
    
    # Summary
    print(f"\n{'='*50}")
    print("Test Summary")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! MCP server is ready for use.")
        return True
    else:
        print("Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


