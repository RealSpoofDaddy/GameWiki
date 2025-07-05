#!/usr/bin/env python3
"""
Simple test script for Steam Status Bar core functionality
Tests only the core statistics calculations without external dependencies
"""

import sys
from typing import Dict, List, Optional


class SteamStatsCalculator:
    """Calculates various Steam statistics - core functionality only"""
    
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


def test_playtime_formatting():
    """Test playtime formatting functionality"""
    print("Testing playtime formatting...")
    
    test_cases = [
        (0, "0m"),
        (30, "30m"),
        (59, "59m"),
        (60, "1h 0m"),
        (90, "1h 30m"),
        (120, "2h 0m"),
        (1439, "23h 59m"),
        (1440, "1d"),
        (1500, "1d 1h"),
        (2880, "2d"),
        (4320, "3d"),
        (5760, "4d"),
        (10080, "7d"),
    ]
    
    for minutes, expected in test_cases:
        result = SteamStatsCalculator.format_playtime(minutes)
        assert result == expected, f"For {minutes} minutes, expected '{expected}', got '{result}'"
        print(f"✅ {minutes} minutes → {result}")
    
    print("✅ All playtime formatting tests passed!")


def test_statistics_calculations():
    """Test game statistics calculations"""
    print("\nTesting statistics calculations...")
    
    # Test with realistic Steam game data
    mock_games = [
        {"name": "Counter-Strike: Global Offensive", "playtime_forever": 1247, "appid": 730},
        {"name": "Team Fortress 2", "playtime_forever": 892, "appid": 440},
        {"name": "Dota 2", "playtime_forever": 2156, "appid": 570},
        {"name": "Garry's Mod", "playtime_forever": 567, "appid": 4000},
        {"name": "The Witcher 3", "playtime_forever": 145, "appid": 292030},
    ]
    
    # Test total playtime
    total_time = SteamStatsCalculator.calculate_total_playtime(mock_games)
    expected_total = 1247 + 892 + 2156 + 567 + 145
    assert total_time == expected_total, f"Expected {expected_total}, got {total_time}"
    print(f"✅ Total playtime: {total_time} minutes ({SteamStatsCalculator.format_playtime(total_time)})")
    
    # Test most played game
    most_played = SteamStatsCalculator.find_most_played_game(mock_games)
    assert most_played is not None, "Most played game should not be None"
    assert most_played["name"] == "Dota 2", f"Expected Dota 2, got {most_played['name']}"
    print(f"✅ Most played game: {most_played['name']} ({most_played['playtime_forever']} minutes)")
    
    # Test with empty games list
    empty_total = SteamStatsCalculator.calculate_total_playtime([])
    assert empty_total == 0, "Empty games list should return 0 total time"
    
    empty_most_played = SteamStatsCalculator.find_most_played_game([])
    assert empty_most_played is None, "Empty games list should return None for most played"
    print("✅ Empty games list handling works")
    
    print("✅ All statistics calculation tests passed!")


def test_achievement_counting():
    """Test achievement counting functionality"""
    print("\nTesting achievement counting...")
    
    # Test with typical achievement data
    mock_achievements = {
        'playerstats': {
            'steamID': '76561198000000000',
            'gameName': 'Counter-Strike: Global Offensive',
            'achievements': [
                {'apiname': 'KILL_ENEMY', 'achieved': 1, 'unlocktime': 1609459200},
                {'apiname': 'WIN_ROUND', 'achieved': 1, 'unlocktime': 1609459300},
                {'apiname': 'PLANT_BOMB', 'achieved': 1, 'unlocktime': 1609459400},
                {'apiname': 'DEFUSE_BOMB', 'achieved': 0, 'unlocktime': 0},
                {'apiname': 'HEADSHOT_KILL', 'achieved': 1, 'unlocktime': 1609459500},
                {'apiname': 'ACE_ROUND', 'achieved': 0, 'unlocktime': 0},
                {'apiname': 'CLUTCH_WIN', 'achieved': 0, 'unlocktime': 0},
            ]
        }
    }
    
    total, unlocked = SteamStatsCalculator.count_achievements(mock_achievements)
    assert total == 7, f"Expected 7 total achievements, got {total}"
    assert unlocked == 4, f"Expected 4 unlocked achievements, got {unlocked}"
    print(f"✅ Achievement counting: {unlocked}/{total} achievements ({unlocked/total*100:.1f}%)")
    
    # Test with no achievements
    empty_achievements = {'playerstats': {'achievements': []}}
    total, unlocked = SteamStatsCalculator.count_achievements(empty_achievements)
    assert total == 0 and unlocked == 0, "Empty achievements should return 0, 0"
    
    # Test with malformed data
    bad_data = {}
    total, unlocked = SteamStatsCalculator.count_achievements(bad_data)
    assert total == 0 and unlocked == 0, "Bad data should return 0, 0"
    print("✅ Edge cases handled correctly")
    
    print("✅ All achievement counting tests passed!")


def demonstrate_features():
    """Demonstrate key features of the Steam Status Bar"""
    print("\nDemonstrating Steam Status Bar features:")
    print("=" * 50)
    
    # Sample data that would come from Steam API
    sample_player = {
        'personaname': 'Demo Gamer',
        'personastate': 1,  # Online
        'steamid': '76561198000000000'
    }
    
    sample_games = [
        {"name": "Counter-Strike: Global Offensive", "playtime_forever": 2847, "playtime_2weeks": 156},
        {"name": "Dota 2", "playtime_forever": 1923, "playtime_2weeks": 89},
        {"name": "Team Fortress 2", "playtime_forever": 876, "playtime_2weeks": 0},
        {"name": "Half-Life 2", "playtime_forever": 234, "playtime_2weeks": 0},
        {"name": "Portal 2", "playtime_forever": 156, "playtime_2weeks": 0},
    ]
    
    print(f"👤 Player: {sample_player['personaname']}")
    print(f"🔗 Steam ID: {sample_player['steamid']}")
    print(f"🟢 Status: {'Online' if sample_player['personastate'] == 1 else 'Offline'}")
    print()
    
    total_games = len(sample_games)
    total_time = SteamStatsCalculator.calculate_total_playtime(sample_games)
    most_played = SteamStatsCalculator.find_most_played_game(sample_games)
    
    print(f"🎮 Total Games: {total_games}")
    print(f"⏱️  Total Playtime: {SteamStatsCalculator.format_playtime(total_time)}")
    if most_played:
        print(f"🏆 Most Played: {most_played['name']} ({SteamStatsCalculator.format_playtime(most_played['playtime_forever'])})")
    else:
        print("🏆 Most Played: None")
    print()
    
    print("📋 Recently Played Games:")
    recent_games = [g for g in sample_games if g.get('playtime_2weeks', 0) > 0]
    for game in recent_games:
        recent_time = SteamStatsCalculator.format_playtime(game['playtime_2weeks'])
        total_time_game = SteamStatsCalculator.format_playtime(game['playtime_forever'])
        print(f"  • {game['name']}: {recent_time} (Total: {total_time_game})")
    
    print("\n✨ This is what the Steam Status Bar shows you about your Steam gaming!")


def main():
    """Run all tests and demonstrations"""
    print("🎮 Steam Status Bar - Core Functionality Tests")
    print("=" * 60)
    
    try:
        test_playtime_formatting()
        test_statistics_calculations()
        test_achievement_counting()
        demonstrate_features()
        
        print("\n🎉 All tests passed successfully!")
        print("\n📦 Next steps to use the Steam Status Bar:")
        print("  1. Get your Steam Web API key: https://steamcommunity.com/dev/apikey")
        print("  2. Find your Steam ID: https://steamidfinder.com/")
        print("  3. Install tkinter: sudo apt-get install python3-tk")
        print("  4. Install requests: pip install requests")
        print("  5. Run: python3 steam_status_bar.py")
        print("\n🎯 Or try the demo first: python3 demo_mode.py")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()