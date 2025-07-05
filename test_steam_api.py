#!/usr/bin/env python3
"""
Test script for Steam Status Bar functionality
Tests the core Steam API integration without GUI dependencies
"""

import sys
import json
from steam_status_bar import SteamAPI, SteamStatsCalculator

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
    methods = ['get_owned_games', 'get_recently_played_games', 'get_player_summaries', 'get_player_achievements']
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

def show_demo_data():
    """Display what the demo data looks like"""
    print("\nDemo Data Preview:")
    print("=" * 50)
    
    # Import demo data
    from demo_mode import MockSteamAPI
    
    mock_api = MockSteamAPI()
    
    # Show player summary
    player_data = mock_api.get_player_summaries("demo")
    player = player_data['response']['players'][0]
    print(f"Player: {player['personaname']}")
    print(f"Steam ID: {player['steamid']}")
    print(f"Status: {player['personastate']}")
    
    # Show games summary
    games_data = mock_api.get_owned_games("demo")
    games = games_data['response']['games']
    print(f"\nTotal Games: {len(games)}")
    
    total_time = sum(game['playtime_forever'] for game in games)
    print(f"Total Playtime: {SteamStatsCalculator.format_playtime(total_time)}")
    
    most_played = max(games, key=lambda x: x['playtime_forever'])
    print(f"Most Played: {most_played['name']} ({SteamStatsCalculator.format_playtime(most_played['playtime_forever'])})")
    
    # Show recent games
    recent_data = mock_api.get_recently_played_games("demo", 3)
    recent_games = recent_data['response']['games']
    print(f"\nRecent Games:")
    for game in recent_games[:3]:
        print(f"  - {game['name']}: {SteamStatsCalculator.format_playtime(game['playtime_forever'])}")

def main():
    """Run all tests"""
    print("🎮 Steam Status Bar - Core Functionality Tests")
    print("=" * 50)
    
    try:
        test_steam_stats_calculator()
        test_steam_api_structure()
        test_achievement_counting()
        show_demo_data()
        
        print("\n🎉 All tests passed successfully!")
        print("\nTo run the full application:")
        print("  • Demo mode: python demo_mode.py")
        print("  • Full app:  python steam_status_bar.py")
        print("  • Launcher:  python launch.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()