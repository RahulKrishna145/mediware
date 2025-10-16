#!/usr/bin/env python3
"""
Setup verification script for hrisk.py dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependency(name, cmd, expected_output=None):
    """Check if a dependency is installed and accessible"""
    print(f"🔍 Checking {name}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            output = result.stdout.strip()
            if expected_output and expected_output not in output:
                print(f"   ❌ {name}: Unexpected output")
                return False
            print(f"   ✅ {name}: OK")
            if output:
                print(f"      Version: {output.split()[0] if output.split() else 'Unknown'}")
            return True
        else:
            print(f"   ❌ {name}: Command failed")
            print(f"      Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"   ❌ {name}: Command timed out")
        return False
    except Exception as e:
        print(f"   ❌ {name}: Error - {e}")
        return False

def check_python_packages():
    """Check if required Python packages are installed"""
    packages = [
        "requests", "pdf2image", "PIL", "pytesseract", 
        "pathlib", "json", "logging"
    ]
    
    print("🐍 Checking Python packages...")
    failed = []
    
    for package in packages:
        try:
            if package == "PIL":
                import PIL
            elif package == "pathlib":
                from pathlib import Path
            else:
                __import__(package)
            print(f"   ✅ {package}: OK")
        except ImportError:
            print(f"   ❌ {package}: Not installed")
            failed.append(package)
    
    return len(failed) == 0

def check_environment_variables():
    """Check if required environment variables are set"""
    print("🌍 Checking environment variables...")
    
    variables = {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "TESSERACT_CMD": os.getenv("TESSERACT_CMD")
    }
    
    all_ok = True
    for var, value in variables.items():
        if value:
            print(f"   ✅ {var}: Set")
            if var == "TESSERACT_CMD" and not Path(value).exists():
                print(f"      ⚠️ Warning: Path doesn't exist: {value}")
        else:
            print(f"   ❌ {var}: Not set")
            all_ok = False
    
    return all_ok

def main():
    """Main setup verification"""
    print("🔧 HRISK.PY DEPENDENCY VERIFICATION")
    print("=" * 50)
    
    checks = []
    
    # Check Python packages
    checks.append(check_python_packages())
    
    # Check system dependencies
    checks.append(check_dependency("Tesseract", "tesseract --version", "tesseract"))
    checks.append(check_dependency("poppler (pdftoppm)", "pdftoppm -h", "pdftoppm"))
    
    # Check environment variables
    checks.append(check_environment_variables())
    
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 ALL DEPENDENCIES OK!")
        print("\nYou can now run:")
        print("   python hrisk.py your_lab_report.pdf")
        print("   python hrisk.py your_lab_report.png")
        return 0
    else:
        print("❌ SOME DEPENDENCIES MISSING!")
        print("\nSetup instructions:")
        print("1. Install missing Python packages: pip install <package_name>")
        print("2. Install Tesseract: https://github.com/tesseract-ocr/tesseract")
        print("3. Install Poppler: Download from https://github.com/oschwartz10612/poppler-windows")
        print("4. Set environment variables using PowerShell commands")
        return 1

if __name__ == "__main__":
    sys.exit(main())