#!/usr/bin/env python3
"""
Steam Status Bar - A desktop widget showing Steam gaming statistics
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import threading
import time
from datetime import datetime
import webbrowser
import os
import configparser
from typing import Dict, List, Optional, Any


class SteamAPI:
    """Handles Steam Web API interactions"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.steampowered.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SteamStatusBar/1.0'
        })
    
    def get_owned_games(self, steam_id: str, include_appinfo: bool = True) -> Optional[Dict]:
        """Get all games owned by a user"""
        url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            'key': self.api_key,
            'steamid': steam_id,
            'format': 'json',
            'include_appinfo': include_appinfo,
            'include_played_free_games': 1
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting owned games: {e}")
            return None
    
    def get_recently_played_games(self, steam_id: str, count: int = 10) -> Optional[Dict]:
        """Get recently played games"""
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
            print(f"Error getting recently played games: {e}")
            return None
    
    def get_player_summaries(self, steam_id: str) -> Optional[Dict]:
        """Get player profile information"""
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
            print(f"Error getting player summaries: {e}")
            return None
    
    def get_player_achievements(self, steam_id: str, app_id: str) -> Optional[Dict]:
        """Get achievements for a specific game"""
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
            print(f"Error getting achievements for game {app_id}: {e}")
            return None


class SteamStatsCalculator:
    """Calculates various Steam statistics"""
    
    @staticmethod
    def calculate_total_playtime(games: List[Dict]) -> int:
        """Calculate total playtime in minutes"""
        return sum(game.get('playtime_forever', 0) for game in games)
    
    @staticmethod
    def find_most_played_game(games: List[Dict]) -> Optional[Dict]:
        """Find the most played game"""
        if not games:
            return None
        return max(games, key=lambda x: x.get('playtime_forever', 0))
    
    @staticmethod
    def count_achievements(achievements_data: Dict) -> tuple:
        """Count total and unlocked achievements"""
        if not achievements_data or 'playerstats' not in achievements_data:
            return 0, 0
        
        achievements = achievements_data['playerstats'].get('achievements', [])
        total = len(achievements)
        unlocked = sum(1 for ach in achievements if ach.get('achieved', 0) == 1)
        
        return total, unlocked
    
    @staticmethod
    def format_playtime(minutes: int) -> str:
        """Format playtime in a readable format"""
        if minutes < 60:
            return f"{minutes}m"
        elif minutes < 1440:  # Less than 24 hours
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}m"
        else:  # More than 24 hours
            hours = minutes // 60
            days = hours // 24
            remaining_hours = hours % 24
            if remaining_hours > 0:
                return f"{days}d {remaining_hours}h"
            else:
                return f"{days}d"


class SteamStatusBar:
    """Main Steam Status Bar application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.load_config()
        self.setup_ui()
        self.steam_api = None
        self.player_data = {}
        self.update_thread = None
        self.running = True
        
        # Initialize Steam API if config is complete
        if self.config.get('steam_api_key') and self.config.get('steam_id'):
            self.steam_api = SteamAPI(self.config['steam_api_key'])
            self.start_data_updates()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Steam Status Bar")
        self.root.geometry("400x300")
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Set window icon if available
        try:
            # Create a simple icon using tkinter
            pass
        except:
            pass
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_config(self):
        """Load configuration from file"""
        self.config_file = 'steam_status_config.ini'
        self.config = {}
        
        if os.path.exists(self.config_file):
            try:
                config_parser = configparser.ConfigParser()
                config_parser.read(self.config_file)
                
                if 'Steam' in config_parser:
                    self.config = dict(config_parser['Steam'])
            except Exception as e:
                print(f"Error loading config: {e}")
        
        # Set defaults
        self.config.setdefault('steam_api_key', '')
        self.config.setdefault('steam_id', '')
        self.config.setdefault('update_interval', '300')  # 5 minutes
        self.config.setdefault('show_achievements', 'True')
        self.config.setdefault('max_recent_games', '5')
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config_parser = configparser.ConfigParser()
            config_parser['Steam'] = self.config
            
            with open(self.config_file, 'w') as f:
                config_parser.write(f)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def setup_ui(self):
        """Setup the user interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status tab
        self.status_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.status_frame, text='Status')
        self.setup_status_tab()
        
        # Games tab
        self.games_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.games_frame, text='Games')
        self.setup_games_tab()
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text='Settings')
        self.setup_settings_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')
    
    def setup_status_tab(self):
        """Setup the main status display tab"""
        # Player info frame
        player_frame = ttk.LabelFrame(self.status_frame, text="Player Info")
        player_frame.pack(fill='x', padx=5, pady=5)
        
        self.player_name_label = ttk.Label(player_frame, text="Player: Not loaded")
        self.player_name_label.pack(anchor='w', padx=5, pady=2)
        
        self.player_status_label = ttk.Label(player_frame, text="Status: Unknown")
        self.player_status_label.pack(anchor='w', padx=5, pady=2)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(self.status_frame, text="Gaming Stats")
        stats_frame.pack(fill='x', padx=5, pady=5)
        
        self.total_games_label = ttk.Label(stats_frame, text="Total Games: 0")
        self.total_games_label.pack(anchor='w', padx=5, pady=2)
        
        self.total_playtime_label = ttk.Label(stats_frame, text="Total Playtime: 0h")
        self.total_playtime_label.pack(anchor='w', padx=5, pady=2)
        
        self.most_played_label = ttk.Label(stats_frame, text="Most Played: None")
        self.most_played_label.pack(anchor='w', padx=5, pady=2)
        
        # Update button
        self.update_button = ttk.Button(stats_frame, text="Update Now", command=self.force_update)
        self.update_button.pack(pady=5)
    
    def setup_games_tab(self):
        """Setup the games display tab"""
        # Recent games frame
        recent_frame = ttk.LabelFrame(self.games_frame, text="Recently Played")
        recent_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for recent games
        self.recent_tree = ttk.Treeview(recent_frame, columns=('playtime', 'last_played'), show='tree headings')
        self.recent_tree.heading('#0', text='Game')
        self.recent_tree.heading('playtime', text='Playtime')
        self.recent_tree.heading('last_played', text='Last Played')
        
        # Configure column widths
        self.recent_tree.column('#0', width=200)
        self.recent_tree.column('playtime', width=100)
        self.recent_tree.column('last_played', width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(recent_frame, orient='vertical', command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.recent_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Double-click to open game in Steam
        self.recent_tree.bind('<Double-1>', self.open_game_in_steam)
    
    def setup_settings_tab(self):
        """Setup the settings tab"""
        # API Configuration
        api_frame = ttk.LabelFrame(self.settings_frame, text="Steam API Configuration")
        api_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(api_frame, text="Steam API Key:").pack(anchor='w', padx=5, pady=2)
        self.api_key_entry = ttk.Entry(api_frame, width=50, show='*')
        self.api_key_entry.pack(fill='x', padx=5, pady=2)
        self.api_key_entry.insert(0, self.config.get('steam_api_key', ''))
        
        ttk.Label(api_frame, text="Steam ID:").pack(anchor='w', padx=5, pady=2)
        self.steam_id_entry = ttk.Entry(api_frame, width=50)
        self.steam_id_entry.pack(fill='x', padx=5, pady=2)
        self.steam_id_entry.insert(0, self.config.get('steam_id', ''))
        
        # Help links
        help_frame = ttk.Frame(api_frame)
        help_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(help_frame, text="Get API Key", 
                  command=lambda: webbrowser.open("https://steamcommunity.com/dev/apikey")).pack(side='left', padx=5)
        ttk.Button(help_frame, text="Find Steam ID", 
                  command=lambda: webbrowser.open("https://steamidfinder.com/")).pack(side='left', padx=5)
        
        # Settings
        settings_frame = ttk.LabelFrame(self.settings_frame, text="Display Settings")
        settings_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Update Interval (seconds):").pack(anchor='w', padx=5, pady=2)
        self.update_interval_entry = ttk.Entry(settings_frame, width=10)
        self.update_interval_entry.pack(anchor='w', padx=5, pady=2)
        self.update_interval_entry.insert(0, self.config.get('update_interval', '300'))
        
        ttk.Label(settings_frame, text="Max Recent Games:").pack(anchor='w', padx=5, pady=2)
        self.max_games_entry = ttk.Entry(settings_frame, width=10)
        self.max_games_entry.pack(anchor='w', padx=5, pady=2)
        self.max_games_entry.insert(0, self.config.get('max_recent_games', '5'))
        
        # Save button
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).pack(pady=10)
    
    def save_settings(self):
        """Save settings from the UI"""
        self.config['steam_api_key'] = self.api_key_entry.get()
        self.config['steam_id'] = self.steam_id_entry.get()
        self.config['update_interval'] = self.update_interval_entry.get()
        self.config['max_recent_games'] = self.max_games_entry.get()
        
        self.save_config()
        
        # Reinitialize Steam API if needed
        if self.config.get('steam_api_key') and self.config.get('steam_id'):
            self.steam_api = SteamAPI(self.config['steam_api_key'])
            if not self.update_thread or not self.update_thread.is_alive():
                self.start_data_updates()
        
        messagebox.showinfo("Settings", "Settings saved successfully!")
    
    def start_data_updates(self):
        """Start the background data update thread"""
        if self.update_thread and self.update_thread.is_alive():
            return
        
        self.update_thread = threading.Thread(target=self.update_data_loop, daemon=True)
        self.update_thread.start()
    
    def update_data_loop(self):
        """Background thread for updating Steam data"""
        while self.running:
            try:
                self.fetch_steam_data()
                self.root.after(0, self.update_ui)
                
                # Wait for next update
                interval = int(self.config.get('update_interval', '300'))
                time.sleep(interval)
            except Exception as e:
                print(f"Error in update loop: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def fetch_steam_data(self):
        """Fetch data from Steam API"""
        if not self.steam_api:
            return
        
        steam_id = self.config.get('steam_id')
        if not steam_id:
            return
        
        try:
            # Update status
            self.root.after(0, lambda: self.status_bar.config(text="Fetching Steam data..."))
            
            # Get player summary
            player_summary = self.steam_api.get_player_summaries(steam_id)
            if player_summary:
                self.player_data['summary'] = player_summary
            
            # Get owned games
            owned_games = self.steam_api.get_owned_games(steam_id)
            if owned_games:
                self.player_data['owned_games'] = owned_games
            
            # Get recent games
            max_recent = int(self.config.get('max_recent_games', '5'))
            recent_games = self.steam_api.get_recently_played_games(steam_id, max_recent)
            if recent_games:
                self.player_data['recent_games'] = recent_games
            
            # Update status
            self.root.after(0, lambda: self.status_bar.config(text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}"))
            
        except Exception as e:
            print(f"Error fetching Steam data: {e}")
            self.root.after(0, lambda: self.status_bar.config(text=f"Error: {str(e)}"))
    
    def force_update(self):
        """Force an immediate update"""
        if self.steam_api:
            threading.Thread(target=self.fetch_steam_data, daemon=True).start()
    
    def update_ui(self):
        """Update the UI with current data"""
        # Update player info
        if 'summary' in self.player_data:
            players = self.player_data['summary'].get('response', {}).get('players', [])
            if players:
                player = players[0]
                self.player_name_label.config(text=f"Player: {player.get('personaname', 'Unknown')}")
                
                # Status mapping
                status_map = {
                    0: "Offline",
                    1: "Online",
                    2: "Busy",
                    3: "Away",
                    4: "Snooze",
                    5: "Looking to trade",
                    6: "Looking to play"
                }
                status = status_map.get(player.get('personastate', 0), "Unknown")
                self.player_status_label.config(text=f"Status: {status}")
        
        # Update gaming stats
        if 'owned_games' in self.player_data:
            games_data = self.player_data['owned_games'].get('response', {})
            games = games_data.get('games', [])
            
            total_games = len(games)
            total_playtime = SteamStatsCalculator.calculate_total_playtime(games)
            most_played = SteamStatsCalculator.find_most_played_game(games)
            
            self.total_games_label.config(text=f"Total Games: {total_games}")
            self.total_playtime_label.config(text=f"Total Playtime: {SteamStatsCalculator.format_playtime(total_playtime)}")
            
            if most_played:
                playtime = SteamStatsCalculator.format_playtime(most_played.get('playtime_forever', 0))
                self.most_played_label.config(text=f"Most Played: {most_played.get('name', 'Unknown')} ({playtime})")
        
        # Update recent games
        if 'recent_games' in self.player_data:
            # Clear existing items
            for item in self.recent_tree.get_children():
                self.recent_tree.delete(item)
            
            recent_data = self.player_data['recent_games'].get('response', {})
            recent_games = recent_data.get('games', [])
            
            for game in recent_games:
                name = game.get('name', 'Unknown')
                playtime = SteamStatsCalculator.format_playtime(game.get('playtime_forever', 0))
                
                # Convert last played timestamp
                last_played = game.get('rtime_last_played', 0)
                if last_played:
                    last_played_str = datetime.fromtimestamp(last_played).strftime('%Y-%m-%d')
                else:
                    last_played_str = 'Never'
                
                self.recent_tree.insert('', 'end', text=name, values=(playtime, last_played_str), 
                                       tags=(str(game.get('appid', '')),))
    
    def open_game_in_steam(self, event):
        """Open selected game in Steam"""
        selection = self.recent_tree.selection()
        if selection:
            item = self.recent_tree.item(selection[0])
            tags = item.get('tags', [])
            if tags:
                app_id = tags[0]
                webbrowser.open(f"steam://rungameid/{app_id}")
    
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    """Main entry point"""
    app = SteamStatusBar()
    app.run()


if __name__ == "__main__":
    main()