#!/usr/bin/env python3
"""
DecAI Oracle - Security Audit Script
Automates basic security checks using Slither and Mythril (if installed)
"""

import subprocess
import sys
import shutil
from pathlib import Path

def check_tool(name):
    """Check if a tool is installed"""
    return shutil.which(name) is not None

def run_slither():
    """Run Slither analysis"""
    print("\n" + "="*60)
    print("🛡️  Running Slither Analysis...")
    print("="*60)
    
    if not check_tool("slither"):
        print("❌ Slither not found. Install with: pip3 install slither-analyzer")
        return False
        
    try:
        # Run slither on the contracts directory
        cmd = ["slither", "contracts/src/PredictionOracle.sol", "--print", "human-summary"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running Slither: {e}")
        return False

def run_mythril():
    """Run Mythril analysis"""
    print("\n" + "="*60)
    print("🛡️  Running Mythril Analysis...")
    print("="*60)
    
    if not check_tool("myth"):
        print("❌ Mythril not found. Install with: pip3 install mythril")
        return False
        
    try:
        # Run mythril on the contract
        cmd = ["myth", "analyze", "contracts/src/PredictionOracle.sol"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Stream output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
        return process.returncode == 0
    except Exception as e:
        print(f"❌ Error running Mythril: {e}")
        return False

def main():
    print("🔒 DecAI Oracle Security Audit Tool")
    
    slither_ok = run_slither()
    mythril_ok = run_mythril()
    
    print("\n" + "="*60)
    print("📊 Audit Summary")
    print(f"Slither: {'✅ Ran' if slither_ok else '❌ Skipped/Failed'}")
    print(f"Mythril: {'✅ Ran' if mythril_ok else '❌ Skipped/Failed'}")
    print("="*60)

if __name__ == "__main__":
    main()
