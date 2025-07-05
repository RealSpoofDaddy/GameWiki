#!/usr/bin/env python3
"""
Steam API Proxy Server
Handles Steam Web API calls and serves the GamePedia frontend
"""

import asyncio
import json
import os
import sys
import time
import webbrowser
import threading
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import requests

class SteamAPIProxy:
    """Handles Steam Web API calls"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.steampowered.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GamePedia-SteamProxy/1.0'
        })
        
    def set_api_key(self, api_key):
        """Set the Steam API key"""
        self.api_key = api_key
        
    def get_player_summaries(self, steam_id):
        """Get player profile information"""
        if not self.api_key:
            return {"error": "Steam API key not configured"}
            
        url = f"{self.base_url}/ISteamUser/GetPlayerSummaries/v0002/"
        params = {
            'key': self.api_key,
            'steamids': steam_id,
            'format': 'json'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get player summaries: {str(e)}"}
    
    def get_owned_games(self, steam_id):
        """Get all games owned by a user"""
        if not self.api_key:
            return {"error": "Steam API key not configured"}
            
        url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            'key': self.api_key,
            'steamid': steam_id,
            'format': 'json',
            'include_appinfo': 1,
            'include_played_free_games': 1
        }
        
        try:
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get owned games: {str(e)}"}
    
    def get_recently_played_games(self, steam_id, count=5):
        """Get recently played games"""
        if not self.api_key:
            return {"error": "Steam API key not configured"}
            
        url = f"{self.base_url}/IPlayerService/GetRecentlyPlayedGames/v0001/"
        params = {
            'key': self.api_key,
            'steamid': steam_id,
            'format': 'json',
            'count': count
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get recent games: {str(e)}"}
    
    def get_player_achievements(self, steam_id, app_id):
        """Get achievements for a specific game"""
        if not self.api_key:
            return {"error": "Steam API key not configured"}
            
        url = f"{self.base_url}/ISteamUserStats/GetPlayerAchievements/v0001/"
        params = {
            'key': self.api_key,
            'steamid': steam_id,
            'appid': app_id,
            'format': 'json'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Failed to get achievements: {str(e)}"}

class GamePediaServer(SimpleHTTPRequestHandler):
    """Custom HTTP server that handles both static files and Steam API proxy"""
    
    def __init__(self, *args, steam_proxy=None, **kwargs):
        self.steam_proxy = steam_proxy
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Handle Steam API proxy requests
        if parsed_path.path.startswith('/api/steam/'):
            self.handle_steam_api(parsed_path)
        else:
            # Handle static files
            self.handle_static_files()
    
    def do_POST(self):
        """Handle POST requests for Steam API configuration"""
        if self.path == '/api/steam/config':
            self.handle_steam_config()
        else:
            self.send_error(404)
    
    def handle_steam_api(self, parsed_path):
        """Handle Steam API proxy requests"""
        try:
            if not self.steam_proxy:
                self.send_json_response({"error": "Steam proxy not initialized"}, 500)
                return
                
            path_parts = parsed_path.path.split('/')
            query_params = parse_qs(parsed_path.query)
            
            # Extract Steam ID from URL
            steam_id = query_params.get('steamid', [None])[0]
            if not steam_id:
                self.send_json_response({"error": "Steam ID required"}, 400)
                return
            
            # Route to appropriate Steam API endpoint
            if '/player' in parsed_path.path:
                data = self.steam_proxy.get_player_summaries(steam_id)
            elif '/games' in parsed_path.path:
                data = self.steam_proxy.get_owned_games(steam_id)
            elif '/recent' in parsed_path.path:
                count = int(query_params.get('count', ['5'])[0])
                data = self.steam_proxy.get_recently_played_games(steam_id, count)
            elif '/achievements' in parsed_path.path:
                app_id = query_params.get('appid', [None])[0]
                if not app_id:
                    self.send_json_response({"error": "App ID required for achievements"}, 400)
                    return
                data = self.steam_proxy.get_player_achievements(steam_id, app_id)
            else:
                self.send_json_response({"error": "Unknown Steam API endpoint"}, 404)
                return
            
            # Add CORS headers and send response
            self.send_json_response(data)
            
        except Exception as e:
            self.send_json_response({"error": f"Steam API error: {str(e)}"}, 500)
    
    def handle_steam_config(self):
        """Handle Steam API configuration"""
        try:
            if not self.steam_proxy:
                self.send_json_response({"error": "Steam proxy not initialized"}, 500)
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            config = json.loads(post_data.decode('utf-8'))
            
            api_key = config.get('api_key')
            if api_key:
                self.steam_proxy.set_api_key(api_key)
                self.send_json_response({"success": True, "message": "Steam API key configured"})
            else:
                self.send_json_response({"error": "API key required"}, 400)
                
        except Exception as e:
            self.send_json_response({"error": f"Configuration error: {str(e)}"}, 500)
    
    def handle_static_files(self):
        """Handle static file requests"""
        # Add CORS headers for all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().do_GET()
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response with CORS headers"""
        response = json.dumps(data, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def get_free_port():
    """Find a free port to use for the server"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def create_server_handler(steam_proxy):
    """Create a server handler with Steam proxy"""
    def handler(*args, **kwargs):
        return GamePediaServer(*args, steam_proxy=steam_proxy, **kwargs)
    return handler

def main():
    """Main server function"""
    # Initialize Steam API proxy
    steam_proxy = SteamAPIProxy()
    
    # Change to gamepedia directory
    gamepedia_dir = Path(__file__).parent / 'gamepedia'
    if not gamepedia_dir.exists():
        print("❌ Error: gamepedia directory not found!")
        print("Please make sure you're running this script from the project root directory.")
        return False
    
    os.chdir(gamepedia_dir)
    
    # Find free port and start server
    port = get_free_port()
    server_handler = create_server_handler(steam_proxy)
    
    try:
        with HTTPServer(("", port), server_handler) as httpd:
            url = f"http://localhost:{port}"
            
            print("🎮 GamePedia + Steam API Server")
            print("=" * 50)
            print(f"🚀 Server URL: {url}")
            print(f"🔧 Port: {port}")
            print(f"📁 Serving from: {gamepedia_dir}")
            print("🔗 Steam API Proxy: Active")
            print("\n" + "🎯 FEATURES:")
            print("✅ Real Steam API Integration")
            print("✅ CORS Proxy for Steam API")
            print("✅ Steam ID and API Key Configuration")
            print("✅ Live Steam Data Updates")
            print("✅ Player Profile & Statistics")
            print("✅ Recently Played Games")
            print("✅ Achievement Progress")
            print("\n" + "⚙️ SETUP:")
            print("1. Get Steam API Key: https://steamcommunity.com/dev/apikey")
            print("2. Find Steam ID: https://steamidfinder.com/")
            print("3. Configure in the Steam widget settings")
            print("\n" + "=" * 50)
            print(f"🌐 Opening browser to {url}")
            print("❌ Press Ctrl+C to stop the server")
            
            # Open browser after delay
            def open_browser():
                time.sleep(1.5)
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

if __name__ == "__main__":
    if not main():
        sys.exit(1)