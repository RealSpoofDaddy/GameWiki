#!/usr/bin/env python3
"""
Steam Status Bar Launcher
Simple launcher script that handles dependencies and starts the application
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found. Please make sure it exists in the same directory.")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import requests
        return True
    except ImportError:
        print("📦 Missing dependencies detected.")
        response = input("Install dependencies now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            return install_dependencies()
        else:
            print("❌ Cannot run without dependencies.")
            return False

def launch_application():
    """Launch the Steam Status Bar application"""
    print("🚀 Starting Steam Status Bar...")
    try:
        # Import and run the main application
        from steam_status_bar import main
        main()
    except ImportError as e:
        print(f"❌ Failed to import application: {e}")
        print("   Make sure steam_status_bar.py is in the same directory.")
        return False
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🎮 Steam Status Bar Launcher")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check and install dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Launch the application
    if not launch_application():
        sys.exit(1)
    
    print("👋 Steam Status Bar closed.")

if __name__ == "__main__":
    main()