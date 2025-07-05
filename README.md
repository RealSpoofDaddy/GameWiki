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

### Demo Mode

The Steam widget currently runs in demo mode with sample data. To enable real Steam API integration:

1. Get a Steam Web API key from https://steamcommunity.com/dev/apikey
2. Find your Steam ID using https://steamidfinder.com/
3. Set up a backend proxy to handle Steam API requests (due to CORS restrictions)
4. Update the `isDemo` flag in the SteamWidget class to `false`

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

1. Clone the repository
2. Open `gamepedia/index.html` in a web browser
3. The Steam widget will automatically initialize with demo data

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
