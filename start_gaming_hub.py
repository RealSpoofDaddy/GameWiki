#!/usr/bin/env python3
"""
GamePedia Ultimate Gaming Hub - Startup Script
Modern Gaming Platform with Steam Integration
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print the modern gaming hub banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🎮 GAMEPEDIA - ULTIMATE GAMING HUB 🎮                   ║
    ║                                                              ║
    ║     • Modern Gaming UI with Dark Theme & Neon Accents       ║
    ║     • Enhanced Steam Integration & Authentication            ║
    ║     • Military-Grade Security & Encryption                  ║
    ║     • Smooth Animations & Gaming Aesthetics                 ║
    ║     • Comprehensive Game Statistics & Analytics             ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print("\033[96m" + banner + "\033[0m")

def check_requirements():
    """Check if all required dependencies are installed"""
    print("\033[93m[INFO]\033[0m Checking requirements...")
    
    required_packages = [
        'requests',
        'cryptography',
        'bcrypt'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\033[91m[ERROR]\033[0m Missing required packages: {', '.join(missing_packages)}")
        print("\033[93m[INFO]\033[0m Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"\033[92m[SUCCESS]\033[0m Installed {package}")
            except subprocess.CalledProcessError:
                print(f"\033[91m[ERROR]\033[0m Failed to install {package}")
                return False
    
    print("\033[92m[SUCCESS]\033[0m All requirements satisfied!")
    return True

def check_server_file():
    """Check if the Steam proxy server file exists"""
    server_file = Path('steam_proxy_server.py')
    if not server_file.exists():
        print(f"\033[91m[ERROR]\033[0m Steam proxy server not found: {server_file}")
        print("\033[93m[INFO]\033[0m Please ensure steam_proxy_server.py is in the current directory")
        return False
    
    print("\033[92m[SUCCESS]\033[0m Steam proxy server found!")
    return True

def start_server():
    """Start the enhanced gaming hub server"""
    print("\033[93m[INFO]\033[0m Starting GamePedia Ultimate Gaming Hub server...")
    
    try:
        # Start the server process
        process = subprocess.Popen([
            sys.executable, 
            'steam_proxy_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Check if the process is still running
        if process.poll() is None:
            print("\033[92m[SUCCESS]\033[0m Gaming Hub server started successfully!")
            
            # Try to open browser
            try:
                webbrowser.open('http://localhost:8080')
                print("\033[92m[INFO]\033[0m Browser opened automatically")
            except Exception as e:
                print(f"\033[93m[WARNING]\033[0m Could not open browser automatically: {e}")
                print("\033[93m[INFO]\033[0m Please manually navigate to: http://localhost:8080")
            
            print("\n\033[96m" + "="*60 + "\033[0m")
            print("\033[96m🎮 GAMEPEDIA ULTIMATE GAMING HUB IS RUNNING! 🎮\033[0m")
            print("\033[96m" + "="*60 + "\033[0m")
            print("\033[92mServer URL:\033[0m http://localhost:8080")
            print("\033[92mFeatures:\033[0m")
            print("  • Modern Gaming UI with Dark Theme")
            print("  • Enhanced Steam Integration") 
            print("  • Military-Grade Security")
            print("  • Smooth Animations & Effects")
            print("  • Real-time Gaming Statistics")
            print("\033[93mPress Ctrl+C to stop the server\033[0m")
            print("\033[96m" + "="*60 + "\033[0m\n")
            
            # Wait for the server process and show output
            try:
                if process.stdout:
                    for line in process.stdout:
                        print(line.rstrip())
                else:
                    process.wait()
            except KeyboardInterrupt:
                print("\n\033[93m[INFO]\033[0m Shutting down Gaming Hub server...")
                process.terminate()
                process.wait()
                print("\033[92m[SUCCESS]\033[0m Gaming Hub server stopped successfully!")
        else:
            print("\033[91m[ERROR]\033[0m Failed to start the server")
            return False
            
    except FileNotFoundError:
        print("\033[91m[ERROR]\033[0m Python not found in PATH")
        return False
    except Exception as e:
        print(f"\033[91m[ERROR]\033[0m Unexpected error: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check server file
    if not check_server_file():
        sys.exit(1)
    
    # Start the server
    if not start_server():
        sys.exit(1)

if __name__ == "__main__":
    main()