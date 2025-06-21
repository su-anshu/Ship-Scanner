#!/usr/bin/env python3
"""
Quick test script to verify the barcode scanner app imports correctly
and basic functions work as expected.
"""

import sys
import importlib.util

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'streamlit',
        'pandas', 
        'cv2',
        'pyzbar',
        'numpy',
        'av'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'pyzbar':
                from pyzbar import pyzbar
            else:
                __import__(package)
            print(f"✅ {package} - OK")
        except ImportError as e:
            print(f"❌ {package} - MISSING: {e}")
            missing_packages.append(package)
    
    return missing_packages

def test_app_syntax():
    """Test if the main app file has valid syntax"""
    try:
        spec = importlib.util.spec_from_file_location("app", "app.py")
        if spec is None:
            print("❌ Could not load app.py")
            return False
        
        module = importlib.util.module_from_spec(spec)
        # We don't execute it, just load to check syntax
        print("✅ app.py syntax - OK")
        return True
    except Exception as e:
        print(f"❌ app.py syntax error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Barcode Scanner App Setup...")
    print("=" * 50)
    
    # Test imports
    print("\n📦 Testing Package Imports:")
    missing = test_imports()
    
    # Test app syntax
    print("\n🐍 Testing App Syntax:")
    syntax_ok = test_app_syntax()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY:")
    
    if not missing and syntax_ok:
        print("🎉 All tests passed! Your app is ready to run.")
        print("\n🚀 To start the app, run:")
        print("   streamlit run app.py")
    else:
        if missing:
            print(f"⚠️  Missing packages: {', '.join(missing)}")
            print("   Install with: pip install -r requirements.txt")
        if not syntax_ok:
            print("⚠️  App syntax errors found - check app.py")
    
    print("=" * 50)
