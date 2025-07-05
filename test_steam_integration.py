#!/usr/bin/env python3
"""
Steam API Integration Test Script
Helps debug Steam API connectivity and configuration issues
"""

import requests
import json
import sys

def test_steam_api(api_key, steam_id):
    """Test Steam API connectivity"""
    base_url = "https://api.steampowered.com"
    session = requests.Session()
    session.headers.update({'User-Agent': 'SteamAPITest/1.0'})
    
    print(f"🔧 Testing Steam API with:")
    print(f"   API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else 'SHORT'}")
    print(f"   Steam ID: {steam_id}")
    print("-" * 50)
    
    # Test 1: Player Summary
    print("1️⃣ Testing Player Summary...")
    try:
        url = f"{base_url}/ISteamUser/GetPlayerSummaries/v0002/"
        params = {
            'key': api_key,
            'steamids': steam_id,
            'format': 'json'
        }
        
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'response' in data and 'players' in data['response'] and data['response']['players']:
            player = data['response']['players'][0]
            print(f"   ✅ Success! Player: {player.get('personaname', 'Unknown')}")
            print(f"   📊 Status: {get_status_text(player.get('personastate', 0))}")
            print(f"   🔗 Profile: {player.get('profileurl', 'N/A')}")
        else:
            print(f"   ❌ No player data found. Response: {json.dumps(data, indent=2)}")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 2: Owned Games
    print("\n2️⃣ Testing Owned Games...")
    try:
        url = f"{base_url}/IPlayerService/GetOwnedGames/v0001/"
        params = {
            'key': api_key,
            'steamid': steam_id,
            'format': 'json',
            'include_appinfo': 1,
            'include_played_free_games': 1
        }
        
        response = session.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            game_count = data['response'].get('game_count', 0)
            total_playtime = sum(game.get('playtime_forever', 0) for game in games)
            
            print(f"   ✅ Success! Found {game_count} games")
            print(f"   ⏱️  Total playtime: {format_playtime(total_playtime)}")
            
            if games:
                most_played = max(games, key=lambda x: x.get('playtime_forever', 0))
                print(f"   🎮 Most played: {most_played.get('name', 'Unknown')} ({format_playtime(most_played.get('playtime_forever', 0))})")
            
        else:
            print(f"   ❌ No games data found. Response: {json.dumps(data, indent=2)}")
            return False
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return False
    
    # Test 3: Recent Games
    print("\n3️⃣ Testing Recent Games...")
    try:
        url = f"{base_url}/IPlayerService/GetRecentlyPlayedGames/v0001/"
        params = {
            'key': api_key,
            'steamid': steam_id,
            'format': 'json',
            'count': 5
        }
        
        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'response' in data and 'games' in data['response']:
            recent_games = data['response']['games']
            print(f"   ✅ Success! Found {len(recent_games)} recent games")
            
            for game in recent_games[:3]:
                print(f"   🎯 {game.get('name', 'Unknown')}: {format_playtime(game.get('playtime_forever', 0))}")
            
        else:
            print(f"   ⚠️  No recent games data (this is OK if player hasn't played recently)")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        # Don't return False for recent games as it's not critical
    
    print("\n" + "=" * 50)
    print("🎉 Steam API Integration Test Complete!")
    print("✅ All critical tests passed. Your Steam API integration should work.")
    return True

def get_status_text(personastate):
    """Convert persona state to readable text"""
    status_map = {
        0: "Offline",
        1: "Online", 
        2: "Busy",
        3: "Away",
        4: "Snooze",
        5: "Looking to trade",
        6: "Looking to play"
    }
    return status_map.get(personastate, "Unknown")

def format_playtime(minutes):
    """Format playtime in a readable format"""
    if minutes < 60:
        return f"{minutes}m"
    elif minutes < 1440:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m" if mins > 0 else f"{hours}h"
    else:
        hours = minutes // 60
        days = hours // 24
        remaining_hours = hours % 24
        return f"{days}d {remaining_hours}h" if remaining_hours > 0 else f"{days}d"

def main():
    """Main test function"""
    print("🎮 Steam API Integration Test")
    print("=" * 50)
    
    if len(sys.argv) != 3:
        print("Usage: python3 test_steam_integration.py <API_KEY> <STEAM_ID>")
        print("\nExample:")
        print("python3 test_steam_integration.py YOUR_API_KEY 76561198123456789")
        print("\n📚 How to get these:")
        print("🔑 API Key: https://steamcommunity.com/dev/apikey")
        print("🆔 Steam ID: https://steamidfinder.com/")
        print("\n⚠️  Make sure your Steam profile is public!")
        sys.exit(1)
    
    api_key = sys.argv[1]
    steam_id = sys.argv[2]
    
    # Validate inputs
    if len(api_key) != 32:
        print("❌ Error: Steam API key should be 32 characters long")
        sys.exit(1)
    
    if not steam_id.isdigit() or len(steam_id) != 17:
        print("❌ Error: Steam ID should be a 17-digit number")
        sys.exit(1)
    
    # Run tests
    success = test_steam_api(api_key, steam_id)
    
    if success:
        print("\n🔧 Next Steps:")
        print("1. Run: python3 launch.py")
        print("2. Open the GamePedia website")
        print("3. Configure Steam API in the widget")
        print("4. Enjoy real Steam data!")
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check your API key is correct")
        print("2. Verify your Steam ID is correct")
        print("3. Make sure your Steam profile is public")
        print("4. Check your internet connection")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()