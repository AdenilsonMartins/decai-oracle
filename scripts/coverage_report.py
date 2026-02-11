#!/usr/bin/env python3
"""
DecAI Oracle - Test Coverage Report Generator
"""

import subprocess
import webbrowser
import os
from pathlib import Path

def generate_coverage():
    print("\n" + "="*60)
    print("📊 Generating Test Coverage Report")
    print("="*60)
    
    try:
        # Run pytest with coverage
        cmd = ["python", "-m", "pytest", "--cov=src", "--cov-report=html", "tests/"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n✅ Coverage report generated successfully!")
            report_path = Path("htmlcov/index.html").absolute()
            print(f"📄 Report: {report_path}")
            
            # Simple summary extraction
            for line in result.stdout.split('\n'):
                if "TOTAL" in line:
                    print(f"\n📈 {line}")
        else:
            print("\n❌ Error generating coverage report:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Execution failed: {str(e)}")

if __name__ == "__main__":
    generate_coverage()
