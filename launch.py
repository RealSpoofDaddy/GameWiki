#!/usr/bin/env python3
"""
Launch script for the GamePedia website with Steam integration
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time
from pathlib import Path

def get_free_port():
    """Find a free port to use for the server"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def serve_website():
    """Serve the GamePedia website locally"""
    # Change to the gamepedia directory
    gamepedia_dir = Path(__file__).parent / 'gamepedia'
    
    if not gamepedia_dir.exists():
        print("Error: gamepedia directory not found!")
        print("Please make sure you're running this script from the project root directory.")
        return False
    
    os.chdir(gamepedia_dir)
    
    # Find a free port
    port = get_free_port()
    
    # Create HTTP server
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers for local development
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            url = f"http://localhost:{port}"
            print(f"� GamePedia Server Starting...")
            print(f"📱 Website URL: {url}")
            print(f"🎮 Steam Integration: Active (Demo Mode)")
            print(f"📁 Serving from: {gamepedia_dir}")
            print(f"🔧 Port: {port}")
            print("\n" + "="*50)
            print("🎯 FEATURES INCLUDED:")
            print("✅ Game Database with Search")
            print("✅ Steam Status Bar Widget")
            print("✅ Player Profile & Statistics")
            print("✅ Recently Played Games")
            print("✅ Achievement Progress")
            print("✅ Responsive Design")
            print("="*50)
            print(f"\n🌐 Opening browser to {url}")
            print("❌ Press Ctrl+C to stop the server")
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(1)
                webbrowser.open(url)
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main function"""
    print("🎮 GamePedia Launcher")
    print("=" * 40)
    
    if not serve_website():
        print("❌ Failed to start the website")
        sys.exit(1)

if __name__ == "__main__":
    main()