#!/usr/bin/env python3
"""
Launch script for the GamePedia website with Steam integration
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Main function"""
    print("🎮 GamePedia + Steam API Launcher")
    print("=" * 50)
    
    # Check if the steam proxy server exists
    steam_proxy_path = Path(__file__).parent / 'steam_proxy_server.py'
    
    if not steam_proxy_path.exists():
        print("❌ Error: steam_proxy_server.py not found!")
        print("Please make sure you're running this script from the project root directory.")
        sys.exit(1)
    
    try:
        print("🚀 Starting GamePedia with Steam API support...")
        print("� This includes a built-in Steam API proxy for real Steam data!")
        print("\n" + "⚡ Features:")
        print("✅ Real Steam API Integration")
        print("✅ Steam Profile Configuration")
        print("✅ Live Steam Data Updates")
        print("✅ Demo Mode Available")
        print("✅ Full CORS Support")
        print("\n" + "🌐 The browser will open automatically...")
        print("❌ Press Ctrl+C in the server window to stop\n")
        
        # Run the steam proxy server
        subprocess.run([sys.executable, str(steam_proxy_path)])
        
    except KeyboardInterrupt:
        print("\n🛑 Launcher stopped by user")
    except FileNotFoundError:
        print("❌ Error: Python not found. Please make sure Python is installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()