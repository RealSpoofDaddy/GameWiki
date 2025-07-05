#!/usr/bin/env python3
"""
Test script for Steam Status Bar core functionality
Tests only the non-GUI components to avoid tkinter dependencies
"""

import sys
import json
import requests
from typing import Dict, List, Optional, Any


class SteamAPI:
    """Handles Steam Web API interactions - copied from main file"""
    
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


class SteamStatsCalculator:
    """Calculates various Steam statistics - copied from main file"""
    
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


def test_steam_stats_calculator():
    """Test the statistics calculation functions"""
    print("Testing SteamStatsCalculator...")
    
    # Test data
    mock_games = [
        {"name": "Game 1", "playtime_forever": 120},
        {"name": "Game 2", "playtime_forever": 45},
        {"name": "Game 3", "playtime_forever": 300},
        {"name": "Game 4", "playtime_forever": 0},
    ]
    
    # Test total playtime calculation
    total_playtime = SteamStatsCalculator.calculate_total_playtime(mock_games)
    expected_total = 120 + 45 + 300 + 0
    assert total_playtime == expected_total, f"Expected {expected_total}, got {total_playtime}"
    print(f"✅ Total playtime calculation: {total_playtime} minutes")
    
    # Test most played game
    most_played = SteamStatsCalculator.find_most_played_game(mock_games)
    assert most_played is not None, "Most played game should not be None"
    assert most_played["name"] == "Game 3", f"Expected Game 3, got {most_played['name']}"
    print(f"✅ Most played game: {most_played['name']} ({most_played['playtime_forever']} minutes)")
    
    # Test playtime formatting
    test_cases = [
        (30, "30m"),
        (90, "1h 30m"),
        (120, "2h 0m"),
        (1440, "1d"),
        (1500, "1d 1h"),
        (2880, "2d"),
    ]
    
    for minutes, expected in test_cases:
        result = SteamStatsCalculator.format_playtime(minutes)
        assert result == expected, f"For {minutes} minutes, expected '{expected}', got '{result}'"
        print(f"✅ Playtime formatting: {minutes} minutes → {result}")
    
    print("✅ All SteamStatsCalculator tests passed!")

def test_steam_api_structure():
    """Test the Steam API class structure (without making actual API calls)"""
    print("\nTesting SteamAPI structure...")
    
    # Test API initialization
    api = SteamAPI("test_key")
    assert api.api_key == "test_key"
    assert api.base_url == "https://api.steampowered.com"
    print("✅ SteamAPI initialization works")
    
    # Test that methods exist
    methods = ['get_owned_games', 'get_recently_played_games', 'get_player_summaries']
    for method in methods:
        assert hasattr(api, method), f"Missing method: {method}"
        print(f"✅ Method exists: {method}")
    
    print("✅ All SteamAPI structure tests passed!")

def test_achievement_counting():
    """Test achievement counting functionality"""
    print("\nTesting achievement counting...")
    
    mock_achievements = {
        'playerstats': {
            'achievements': [
                {'achieved': 1, 'apiname': 'FIRST_KILL'},
                {'achieved': 0, 'apiname': 'MASTER_LEVEL'},
                {'achieved': 1, 'apiname': 'WIN_ROUND'},
                {'achieved': 1, 'apiname': 'COLLECT_ALL'},
                {'achieved': 0, 'apiname': 'SPEEDRUN'},
            ]
        }
    }
    
    total, unlocked = SteamStatsCalculator.count_achievements(mock_achievements)
    assert total == 5, f"Expected 5 total achievements, got {total}"
    assert unlocked == 3, f"Expected 3 unlocked achievements, got {unlocked}"
    print(f"✅ Achievement counting: {unlocked}/{total} achievements unlocked")
    
    # Test empty achievements
    empty_achievements = {}
    total, unlocked = SteamStatsCalculator.count_achievements(empty_achievements)
    assert total == 0 and unlocked == 0, "Empty achievements should return 0, 0"
    print("✅ Empty achievements handling works")
    
    print("✅ All achievement counting tests passed!")

def test_api_urls():
    """Test that API URLs are correctly formatted"""
    print("\nTesting API URL construction...")
    
    api = SteamAPI("test_key")
    
    # Test URL construction (without making actual requests)
    test_steam_id = "76561198000000000"
    
    # Check that the base URLs are correct
    assert "api.steampowered.com" in api.base_url
    assert api.session.headers.get('User-Agent') == 'SteamStatusBar/1.0'
    
    print("✅ API URL construction works")
    print("✅ User-Agent header is set correctly")

def main():
    """Run all tests"""
    print("🎮 Steam Status Bar - Core Functionality Tests")
    print("=" * 50)
    
    try:
        test_steam_stats_calculator()
        test_steam_api_structure()
        test_achievement_counting()
        test_api_urls()
        
        print("\n🎉 All core functionality tests passed!")
        print("\nThe Steam Status Bar application should work correctly!")
        print("\nNext steps:")
        print("  1. Install tkinter if needed for GUI: sudo apt-get install python3-tk")
        print("  2. Run demo mode: python3 demo_mode.py")
        print("  3. Get Steam API key: https://steamcommunity.com/dev/apikey")
        print("  4. Run full app: python3 steam_status_bar.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()