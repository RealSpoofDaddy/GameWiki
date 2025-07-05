#!/usr/bin/env python3
"""
Steam Status Bar Demo Mode
Demonstrates the application with mock Steam data for testing
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import threading
import time
from datetime import datetime, timedelta
import random
from typing import Dict, List, Optional, Any


class MockSteamAPI:
    """Mock Steam API for demo purposes"""
    
    def __init__(self):
        self.mock_data = self._generate_mock_data()
    
    def _generate_mock_data(self):
        """Generate realistic mock Steam data"""
        mock_games = [
            {"appid": 730, "name": "Counter-Strike: Global Offensive", "playtime_forever": 1247, "playtime_2weeks": 45},
            {"appid": 440, "name": "Team Fortress 2", "playtime_forever": 892, "playtime_2weeks": 23},
            {"appid": 570, "name": "Dota 2", "playtime_forever": 2156, "playtime_2weeks": 89},
            {"appid": 4000, "name": "Garry's Mod", "playtime_forever": 567, "playtime_2weeks": 0},
            {"appid": 292030, "name": "The Witcher 3: Wild Hunt", "playtime_forever": 145, "playtime_2weeks": 12},
            {"appid": 271590, "name": "Grand Theft Auto V", "playtime_forever": 234, "playtime_2weeks": 34},
            {"appid": 431960, "name": "Wallpaper Engine", "playtime_forever": 56, "playtime_2weeks": 0},
            {"appid": 362890, "name": "Black Mesa", "playtime_forever": 89, "playtime_2weeks": 0},
            {"appid": 1245620, "name": "ELDEN RING", "playtime_forever": 67, "playtime_2weeks": 67},
            {"appid": 1086940, "name": "Baldur's Gate 3", "playtime_forever": 123, "playtime_2weeks": 15},
        ]
        
        # Add timestamps for recently played games
        base_time = int(time.time())
        for i, game in enumerate(mock_games[:5]):  # Only first 5 are "recently played"
            game['rtime_last_played'] = base_time - (i * 86400)  # Each game 1 day apart
        
        return {
            'player_summary': {
                'response': {
                    'players': [{
                        'steamid': '76561198000000000',
                        'personaname': 'Demo Player',
                        'personastate': 1,  # Online
                        'avatar': '',
                        'avatarmedium': '',
                        'avatarfull': '',
                        'lastlogoff': base_time - 3600,  # 1 hour ago
                        'timecreated': base_time - (365 * 24 * 3600 * 5)  # 5 years ago
                    }]
                }
            },
            'owned_games': {
                'response': {
                    'game_count': len(mock_games),
                    'games': mock_games
                }
            },
            'recent_games': {
                'response': {
                    'total_count': 5,
                    'games': mock_games[:5]
                }
            }
        }
    
    def get_player_summaries(self, steam_id: str) -> Dict:
        """Mock player summaries"""
        return self.mock_data['player_summary']
    
    def get_owned_games(self, steam_id: str, include_appinfo: bool = True) -> Dict:
        """Mock owned games"""
        return self.mock_data['owned_games']
    
    def get_recently_played_games(self, steam_id: str, count: int = 10) -> Dict:
        """Mock recently played games"""
        return self.mock_data['recent_games']
    
    def get_player_achievements(self, steam_id: str, app_id: str) -> Dict:
        """Mock achievements"""
        return {
            'playerstats': {
                'steamID': steam_id,
                'gameName': 'Demo Game',
                'achievements': [
                    {'apiname': 'FIRST_KILL', 'achieved': 1, 'unlocktime': int(time.time()) - 86400},
                    {'apiname': 'WIN_ROUND', 'achieved': 1, 'unlocktime': int(time.time()) - 3600},
                    {'apiname': 'MASTER_LEVEL', 'achieved': 0, 'unlocktime': 0},
                    {'apiname': 'COLLECT_ALL', 'achieved': 1, 'unlocktime': int(time.time()) - 7200},
                    {'apiname': 'SPEEDRUN', 'achieved': 0, 'unlocktime': 0},
                ]
            }
        }


class DemoSteamStatusBar:
    """Demo version of the Steam Status Bar"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        self.steam_api = MockSteamAPI()
        self.player_data = {}
        self.update_thread = None
        self.running = True
        self.demo_mode = True
        
        # Start demo data updates
        self.start_demo_updates()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Steam Status Bar - DEMO MODE")
        self.root.geometry("500x400")
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set a different background color to indicate demo mode
        self.root.configure(bg='#2c3e50')
    
    def setup_ui(self):
        """Setup the user interface"""
        # Demo mode banner
        demo_banner = tk.Label(self.root, text="🎮 DEMO MODE - Mock Steam Data", 
                              bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'))
        demo_banner.pack(fill='x', pady=2)
        
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
        
        # Demo info tab
        self.demo_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.demo_frame, text='Demo Info')
        self.setup_demo_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Demo Mode - Using Mock Data", relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')
    
    def setup_status_tab(self):
        """Setup the main status display tab"""
        # Player info frame
        player_frame = ttk.LabelFrame(self.status_frame, text="Player Info")
        player_frame.pack(fill='x', padx=5, pady=5)
        
        self.player_name_label = ttk.Label(player_frame, text="Player: Demo Player")
        self.player_name_label.pack(anchor='w', padx=5, pady=2)
        
        self.player_status_label = ttk.Label(player_frame, text="Status: Online")
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
        
        # Demo controls
        controls_frame = ttk.Frame(stats_frame)
        controls_frame.pack(fill='x', pady=5)
        
        self.update_button = ttk.Button(controls_frame, text="Update Demo Data", 
                                       command=self.update_demo_data)
        self.update_button.pack(side='left', padx=5)
        
        self.randomize_button = ttk.Button(controls_frame, text="Randomize Stats", 
                                          command=self.randomize_stats)
        self.randomize_button.pack(side='left', padx=5)
    
    def setup_games_tab(self):
        """Setup the games display tab"""
        # Recent games frame
        recent_frame = ttk.LabelFrame(self.games_frame, text="Recently Played (Demo)")
        recent_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for recent games
        self.recent_tree = ttk.Treeview(recent_frame, columns=('playtime', 'last_played'), show='tree headings')
        self.recent_tree.heading('#0', text='Game')
        self.recent_tree.heading('playtime', text='Playtime')
        self.recent_tree.heading('last_played', text='Last Played')
        
        # Configure column widths
        self.recent_tree.column('#0', width=250)
        self.recent_tree.column('playtime', width=100)
        self.recent_tree.column('last_played', width=100)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(recent_frame, orient='vertical', command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.recent_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Demo note
        note_label = ttk.Label(recent_frame, text="💡 In demo mode, double-clicking won't launch actual games", 
                              foreground='blue')
        note_label.pack(pady=5)
    
    def setup_demo_tab(self):
        """Setup the demo information tab"""
        info_frame = ttk.LabelFrame(self.demo_frame, text="Demo Information")
        info_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        demo_text = """🎮 Steam Status Bar Demo Mode

This is a demonstration of the Steam Status Bar application using mock data.

Features being demonstrated:
✅ Player profile information
✅ Gaming statistics calculation
✅ Recently played games display
✅ Automatic data updates
✅ Game playtime formatting
✅ User interface components

To use with real Steam data:
1. Get a Steam Web API key from:
   https://steamcommunity.com/dev/apikey

2. Find your Steam ID using:
   https://steamidfinder.com/

3. Run the full application:
   python steam_status_bar.py

4. Enter your credentials in the Settings tab

Demo Controls:
• Update Demo Data - Refresh the mock data
• Randomize Stats - Generate new random statistics
• All data shown is simulated for demonstration

The actual application connects to Steam's official API
to show your real gaming statistics and achievements!"""
        
        demo_label = tk.Text(info_frame, wrap='word', height=20, width=60)
        demo_label.insert('1.0', demo_text)
        demo_label.config(state='disabled')
        
        # Add scrollbar to text widget
        text_scroll = ttk.Scrollbar(info_frame, orient='vertical', command=demo_label.yview)
        demo_label.configure(yscrollcommand=text_scroll.set)
        
        demo_label.pack(side='left', fill='both', expand=True)
        text_scroll.pack(side='right', fill='y')
    
    def start_demo_updates(self):
        """Start the demo data update thread"""
        self.update_thread = threading.Thread(target=self.demo_update_loop, daemon=True)
        self.update_thread.start()
        
        # Initial update
        self.update_demo_data()
    
    def demo_update_loop(self):
        """Demo update loop - simulates periodic updates"""
        while self.running:
            time.sleep(30)  # Update every 30 seconds in demo mode
            if self.running:
                self.root.after(0, self.update_demo_data)
    
    def update_demo_data(self):
        """Update the demo data"""
        # Simulate fetching data
        self.status_bar.config(text="Fetching demo data...")
        
        # Get mock data
        self.player_data = {
            'summary': self.steam_api.get_player_summaries('demo_id'),
            'owned_games': self.steam_api.get_owned_games('demo_id'),
            'recent_games': self.steam_api.get_recently_played_games('demo_id', 5)
        }
        
        # Update UI
        self.update_ui()
        
        # Update status
        self.status_bar.config(text=f"Demo updated: {datetime.now().strftime('%H:%M:%S')}")
    
    def randomize_stats(self):
        """Randomize the demo statistics"""
        # Randomize playtime for games
        games = self.steam_api.mock_data['owned_games']['response']['games']
        for game in games:
            game['playtime_forever'] = random.randint(10, 3000)
            if random.random() < 0.3:  # 30% chance of recent play
                game['playtime_2weeks'] = random.randint(0, 120)
            else:
                game['playtime_2weeks'] = 0
        
        # Update recent games
        recent_games = sorted(games, key=lambda x: x.get('playtime_2weeks', 0), reverse=True)[:5]
        self.steam_api.mock_data['recent_games']['response']['games'] = recent_games
        
        # Update the display
        self.update_demo_data()
        messagebox.showinfo("Demo", "Statistics randomized!")
    
    def update_ui(self):
        """Update the UI with current demo data"""
        # Update player info
        if 'summary' in self.player_data:
            players = self.player_data['summary'].get('response', {}).get('players', [])
            if players:
                player = players[0]
                self.player_name_label.config(text=f"Player: {player.get('personaname', 'Demo Player')}")
                
                # Status mapping
                status_map = {0: "Offline", 1: "Online", 2: "Busy", 3: "Away", 4: "Snooze", 5: "Looking to trade", 6: "Looking to play"}
                status = status_map.get(player.get('personastate', 1), "Online")
                self.player_status_label.config(text=f"Status: {status}")
        
        # Update gaming stats
        if 'owned_games' in self.player_data:
            games_data = self.player_data['owned_games'].get('response', {})
            games = games_data.get('games', [])
            
            total_games = len(games)
            total_playtime = sum(game.get('playtime_forever', 0) for game in games)
            most_played = max(games, key=lambda x: x.get('playtime_forever', 0)) if games else None
            
            self.total_games_label.config(text=f"Total Games: {total_games}")
            self.total_playtime_label.config(text=f"Total Playtime: {self.format_playtime(total_playtime)}")
            
            if most_played:
                playtime = self.format_playtime(most_played.get('playtime_forever', 0))
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
                playtime = self.format_playtime(game.get('playtime_forever', 0))
                
                # Convert last played timestamp
                last_played = game.get('rtime_last_played', 0)
                if last_played:
                    last_played_str = datetime.fromtimestamp(last_played).strftime('%Y-%m-%d')
                else:
                    last_played_str = 'Never'
                
                self.recent_tree.insert('', 'end', text=name, values=(playtime, last_played_str))
    
    def format_playtime(self, minutes: int) -> str:
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
    
    def on_closing(self):
        """Handle application closing"""
        self.running = False
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Start the demo application"""
        self.root.mainloop()


def main():
    """Main entry point for demo mode"""
    print("🎮 Starting Steam Status Bar Demo Mode")
    print("This will show the application with mock Steam data")
    print("=" * 50)
    
    app = DemoSteamStatusBar()
    app.run()


if __name__ == "__main__":
    main()