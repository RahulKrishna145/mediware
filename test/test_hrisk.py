#!/usr/bin/env python3
"""
Quick test script for hrisk.py functionality
"""

import os
import sys
from pathlib import Path

# Set environment variables for this session
os.environ['GEMINI_API_KEY'] = 'AIzaSyC_kAvA09PcJmp2a5kEM7E4I9WRpYPt7SA'
os.environ['TESSERACT_CMD'] = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def test_imports():
    """Test if all required imports work"""
    print("🧪 Testing imports...")
    try:
        import os
        import sys
        import json
        import logging
        from pathlib import Path
        import requests
        from requests.exceptions import RequestException
        from pdf2image import convert_from_path
        from PIL import Image
        import pytesseract
        import shutil
        import re
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_tesseract():
    """Test Tesseract OCR functionality"""
    print("🔍 Testing Tesseract...")
    try:
        import pytesseract
        from PIL import Image
        
        # Set Tesseract path
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Create a simple test image with text
        img = Image.new('RGB', (300, 100), color='white')
        
        # Try OCR (will return empty or minimal text for blank image)
        text = pytesseract.image_to_string(img)
        print("✅ Tesseract working!")
        return True
    except Exception as e:
        print(f"❌ Tesseract test failed: {e}")
        return False

def test_gemini_connection():
    """Test Gemini API connection using hrisk.py configuration"""
    print("🤖 Testing Gemini API...")
    try:
        import requests
        
        # Use same configuration as hrisk.py
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        
        if not GEMINI_API_KEY:
            print("❌ GEMINI_API_KEY not set")
            return False
        
        # Use exact same API call pattern as hrisk.py
        corrected_url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": "Hello, respond with just 'OK'"}]}]
        }
        
        # Use same timeout as hrisk.py (120 seconds)
        response = requests.post(
            corrected_url, 
            headers=headers,
            json=payload,
            timeout=120 
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Extract text response like hrisk.py does
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"✅ Gemini API working! Response: {text.strip()}")
            return True
        except Exception as e:
            print(f"❌ Gemini response format error: {e}")
            print(f"Raw response: {data}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 HRISK.PY FUNCTIONALITY TEST")
    print("=" * 40)
    
    tests = [
        test_imports(),
        test_tesseract(),
        test_gemini_connection()
    ]
    
    print("\n" + "=" * 40)
    
    if all(tests):
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ hrisk.py is ready to use!")
        print("\nUsage examples:")
        print("   python hrisk.py sample_lab_report.pdf")
        print("   python hrisk.py lab_image.png")
        print("\nMake sure you have a lab report file to test with.")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        print("\nPlease check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())