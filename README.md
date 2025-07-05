# Steam Status Bar

A cross-platform desktop application that displays your Steam gaming statistics in a convenient status bar widget.

## Features

### 📊 Gaming Statistics
- **Total Games**: See how many games you own
- **Total Playtime**: View your cumulative gaming hours across all games
- **Most Played Game**: Discover which game you've spent the most time playing
- **Player Status**: Shows your current Steam status (Online, Offline, Away, etc.)

### 🎮 Recently Played Games
- View your recently played games in a neat table
- See playtime for each game
- Check when you last played each game
- Double-click any game to launch it directly in Steam

### ⚙️ Configurable Settings
- Customizable update intervals
- Adjustable number of recent games to display
- Persistent configuration storage
- Always-on-top window option

### 🔗 Steam Integration
- Uses official Steam Web API
- Direct Steam game launching
- Real-time status updates
- Secure API key storage

## Screenshots

The application features a clean, tabbed interface with three main sections:
- **Status Tab**: Shows your player info and gaming statistics
- **Games Tab**: Displays recently played games in a sortable table
- **Settings Tab**: Configure API keys and display preferences

## Prerequisites

- Python 3.7 or higher
- Steam account
- Steam Web API key (free to obtain)

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd steam-status-bar
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python steam_status_bar.py
   ```

## Setup Guide

### Step 1: Get Your Steam API Key

1. Go to [Steam Web API Key page](https://steamcommunity.com/dev/apikey)
2. Log in with your Steam account
3. Fill in the domain field (you can use `localhost` for personal use)
4. Click "Register" to get your API key
5. **Important**: Keep this key private and don't share it

### Step 2: Find Your Steam ID

1. Visit [SteamID Finder](https://steamidfinder.com/)
2. Enter your Steam profile URL or username
3. Copy your "steamID64" (it's a long number like `76561198000000000`)

### Step 3: Configure the Application

1. Open the Steam Status Bar application
2. Go to the "Settings" tab
3. Enter your Steam API Key in the first field
4. Enter your Steam ID in the second field
5. Adjust other settings as desired:
   - **Update Interval**: How often to refresh data (default: 300 seconds)
   - **Max Recent Games**: Number of recent games to display (default: 5)
6. Click "Save Settings"

The application will automatically start fetching your Steam data!

## Usage

### Main Interface

- **Status Tab**: View your current Steam status and overall gaming statistics
- **Games Tab**: Browse your recently played games and launch them directly
- **Settings Tab**: Configure API settings and display preferences

### Features

- **Auto-refresh**: The application automatically updates your data based on the configured interval
- **Manual refresh**: Click "Update Now" to immediately fetch the latest data
- **Game launching**: Double-click any game in the "Games" tab to open it in Steam
- **Always on top**: The window stays on top of other applications for easy monitoring

### Status Bar

The bottom status bar shows:
- "Ready" when the application is idle
- "Fetching Steam data..." when updating
- "Last updated: HH:MM:SS" after successful updates
- Error messages if something goes wrong

## Configuration

The application stores its configuration in `steam_status_config.ini`. You can edit this file directly if needed:

```ini
[Steam]
steam_api_key = your_api_key_here
steam_id = your_steam_id_here
update_interval = 300
show_achievements = True
max_recent_games = 5
```

## Troubleshooting

### Common Issues

1. **"Error getting owned games"**
   - Check that your API key is correct
   - Verify your Steam ID is the correct 64-bit format
   - Ensure your Steam profile is public

2. **"No data displaying"**
   - Make sure you've entered both API key and Steam ID
   - Check your internet connection
   - Verify your Steam profile privacy settings

3. **"Games not launching"**
   - Ensure Steam is installed and running
   - Check that the Steam browser protocol is enabled

### Steam Profile Privacy

For the application to work properly, your Steam profile must be set to "Public" or "Friends Only" with game details visible. To check this:

1. Go to your Steam profile
2. Click "Edit Profile"
3. Go to "Privacy Settings"
4. Set "Game details" to "Public" or "Friends Only"

## API Rate Limits

The Steam Web API has rate limits. The application is designed to:
- Cache data to minimize API calls
- Use reasonable default update intervals (5 minutes)
- Handle rate limiting gracefully

## Privacy & Security

- Your API key is stored locally on your computer
- The application only makes requests to official Steam API endpoints
- No personal data is transmitted to third parties
- API key is masked in the settings interface

## Platform Support

This application is cross-platform and works on:
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu, Debian, Fedora, etc.)

## Dependencies

- `requests`: For HTTP API calls to Steam
- `tkinter`: GUI framework (included with Python)
- `threading`: For background updates
- `configparser`: For configuration management

## Contributing

Feel free to submit issues and enhancement requests! Some ideas for future features:

- Achievement tracking and statistics
- Friends list and activity
- Game price tracking
- Steam inventory display
- Custom themes and styling
- System tray integration
- Notification system

## License

This project is open source and available under the MIT License.

## Disclaimer

This application is not affiliated with or endorsed by Valve Corporation or Steam. Steam is a trademark of Valve Corporation.

---

**Enjoy tracking your Steam gaming statistics!** 🎮
