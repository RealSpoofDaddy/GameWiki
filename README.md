# GamePedia Project

A comprehensive gaming encyclopedia and Steam integration platform.

## Features

- **Game Database**: Comprehensive collection of game information
- **Advanced Search**: Search by title, developer, genre, platform, and more
- **Steam Integration**: Real-time Steam status and gaming statistics
- **Responsive Design**: Works on desktop and mobile devices
- **Game Pages**: Detailed information about individual games

## Steam Integration

The project includes a Steam Status Bar widget that displays:
- Player profile information and online status
- Gaming statistics (total games, playtime, most played)
- Recently played games with icons and playtime
- Achievement progress visualization
- Real-time updates every 5 minutes

### Steam Widget Features

- **Player Info**: Shows Steam avatar, username, and online status
- **Gaming Stats**: Displays total games owned, total playtime, and most played game
- **Recent Games**: Shows last 3 played games with icons and playtime
- **Achievement Progress**: Visual progress bar for achievements
- **Interactive Elements**: Click on games to launch them in Steam

### Real Steam API Integration

The Steam widget now supports real Steam API integration! You can use either demo mode or connect your actual Steam account.

#### Quick Setup (Real Steam Data):

1. **Get Steam API Key**: Visit https://steamcommunity.com/dev/apikey
2. **Find Your Steam ID**: Use https://steamidfinder.com/
3. **Launch with API Support**: Run `python3 launch.py` (now includes built-in Steam API proxy)
4. **Configure**: Enter your API key and Steam ID in the widget settings
5. **Enjoy**: Real-time Steam data with live updates!

#### Demo Mode:

For testing without Steam API setup, the widget provides a demo mode with realistic sample data.

## File Structure

```
gamepedia/
├── index.html          # Main webpage
├── style.css           # Styling including Steam widget styles
├── script.js           # Main JavaScript with Steam widget functionality
├── js/
│   └── router.js       # Page routing
├── css/
│   └── game-page.css   # Game page specific styles
├── data/
│   └── games.json      # Game database
└── games/
    └── [game-pages]    # Individual game pages
```

## Setup

### Option 1: With Real Steam API (Recommended)
1. **Install dependencies**: `sudo apt install python3-requests` (or equivalent)
2. **Run the server**: `python3 launch.py`
3. **Browser opens automatically** with Steam API support
4. **Configure Steam**: Enter your API key and Steam ID in the widget

### Option 2: Demo Mode Only
1. Clone the repository
2. Open `gamepedia/index.html` in a web browser
3. The Steam widget will show demo data

## Troubleshooting Steam API

### Testing Your Steam API Configuration
```bash
# Test your Steam API credentials first
python3 test_steam_integration.py YOUR_API_KEY YOUR_STEAM_ID
```

### Common Issues
- **"Steam API key not configured"**: Make sure you entered the API key correctly
- **"Steam ID required"**: Verify your Steam ID is a 17-digit number
- **"No player data found"**: Check that your Steam profile is set to public
- **"Permission denied"**: Your API key might be invalid or expired

### Steam Profile Privacy
Your Steam profile must be public for the API to work:
1. Go to your Steam profile → Edit Profile → Privacy Settings
2. Set "Game details" to "Public"
3. Set "Game details" to "Public" (yes, this is important!)

## Steam API Integration

For production use with real Steam data:

1. **Backend Setup**: Create a server-side proxy to handle Steam API requests
2. **API Configuration**: Add your Steam API key and Steam ID
3. **CORS Handling**: Steam API doesn't allow direct browser requests due to CORS policy
4. **Rate Limiting**: Implement proper rate limiting for Steam API calls

### Example Backend Proxy (Node.js)

```javascript
const express = require('express');
const axios = require('axios');
const app = express();

app.get('/api/steam/player/:steamid', async (req, res) => {
  try {
    const response = await axios.get(`https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=${API_KEY}&steamids=${req.params.steamid}`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch Steam data' });
  }
});
```

## Styling

The Steam widget uses Steam's official color scheme:
- Primary: #66c0f4 (Steam blue)
- Secondary: #1b2838 (Steam dark blue)
- Background: #2a475e (Steam gray)
- Text: #c7d5e0 (Steam light gray)

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project is licensed under the MIT License - see the LICENSE file for details.
