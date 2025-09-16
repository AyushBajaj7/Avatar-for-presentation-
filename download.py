#!/usr/bin/env python3
"""
Easy AI Speaker Avatar System - Dependency Installer
====================================================
This script installs all required dependencies for the Easy AI Speaker Avatar System.
Run this once to install all packages, then use run.py for normal operation.
"""

import subprocess
import sys
import os

def install_package(package_name, import_name=None):
    """Install a package and verify it can be imported."""
    if import_name is None:
        import_name = package_name
    
    try:
        # Try to import the package first
        __import__(import_name)
        print(f"  ✅ {package_name} already installed")
        return True
    except ImportError:
        pass
    
    print(f"  📦 Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"  ✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Failed to install {package_name}: {e}")
        return False

def main():
    """Install all required dependencies."""
    print("🔧 Easy AI Speaker Avatar System - Dependency Installer")
    print("=" * 60)
    print("Installing all required packages...")
    print()
    
    # List of required packages with their pip names and import names
    packages = [
        ("python-pptx", "pptx"),
        ("Pillow", "PIL"),
        ("opencv-python", "cv2"),
        ("pyttsx3", "pyttsx3"),
        ("tqdm", "tqdm"),
        ("numpy", "numpy"),
        ("flask", "flask"),
        ("flask-cors", "flask_cors"),
        ("google-generativeai", "google.generativeai"),
        ("PyPDF2", "PyPDF2"),
        ("pdf2image", "pdf2image"),
    ]
    
    success_count = 0
    total_packages = len(packages)
    
    for package_name, import_name in packages:
        if install_package(package_name, import_name):
            success_count += 1
    
    print()
    print("=" * 60)
    if success_count == total_packages:
        print("🎉 All dependencies installed successfully!")
        print("You can now run 'python run.py' to start the system.")
    else:
        print(f"⚠️  {success_count}/{total_packages} packages installed successfully.")
        print("Some packages failed to install. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
