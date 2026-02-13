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
        # Detect if we are in the root or in the contracts directory
        contract_path = Path("contracts/src/PredictionOracle.sol")
        current_dir = "."
        
        if not contract_path.exists():
            # Try if we are already inside contracts
            if Path("src/PredictionOracle.sol").exists():
                contract_path = Path("src/PredictionOracle.sol")
            else:
                print("❌ Contract not found. Please run from the project root.")
                return False

        # Run slither
        # We use --solc-remaps to ensure OpenZeppelin is found correctly
        # Assuming node_modules is in the same folder as the contract's parent 'src' folder (i.e. inside 'contracts/')
        cmd = ["slither", str(contract_path), "--print", "human-summary"]
        
        # If running from root, help slither find node_modules
        if "contracts/" in str(contract_path):
             cmd.extend(["--solc-remaps", f"@openzeppelin/contracts=contracts/node_modules/@openzeppelin/contracts"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Output Details:")
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
        # Detect contract path
        contract_path = Path("contracts/src/PredictionOracle.sol")
        remap = ""
        
        if not contract_path.exists():
            if Path("src/PredictionOracle.sol").exists():
                contract_path = Path("src/PredictionOracle.sol")
                remap = "@openzeppelin/contracts=node_modules/@openzeppelin/contracts"
            else:
                return False
        else:
            remap = "@openzeppelin/contracts=contracts/node_modules/@openzeppelin/contracts"

        # Run mythril
        cmd = ["myth", "analyze", str(contract_path), "--solc-args", f"--allow-paths . --map-remapping {remap}"]
        
        # Use simple execution for mythril as it can be long
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
                
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running Mythril: {e}")
        return False

def main():
    print("🔒 DecAI Oracle Security Audit Tool")
    
    # Slither is the priority
    slither_ok = run_slither()
    
    # Check if Mythril exists before running
    myth_exists = check_tool("myth")
    mythril_ok = False
    if myth_exists:
        mythril_ok = run_mythril()
    else:
        print("\n" + "="*60)
        print("🛡️  Skipping Mythril Analysis (Not installed in this environment)")
        print("="*60)
    
    print("\n" + "="*60)
    print("📊 Audit Summary")
    print(f"Slither: {'✅ Success' if slither_ok else '❌ Failed'}")
    print(f"Mythril: {'✅ Success' if mythril_ok else '⚪ Skipped'}")
    print("="*60)

if __name__ == "__main__":
    main()
