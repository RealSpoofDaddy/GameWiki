# GamePedia - The Free Gaming Encyclopedia

A comprehensive Wikipedia-style encyclopedia dedicated to video games, featuring modern web design, advanced search functionality, and responsive layout.

## 🎮 Features

### Core Functionality
- **Wikipedia-inspired Design**: Clean, professional layout with serif typography and familiar navigation
- **Advanced Search**: Live search with autocomplete suggestions and filtering by genre, platform, and year
- **Responsive Design**: Mobile-first approach that works seamlessly across all devices
- **Game Database**: JSON-based database with detailed game information
- **Featured Content**: Daily featured games and recent additions
- **Statistics Dashboard**: Real-time stats showing total games, developers, and platforms

### Search & Navigation
- **Live Search**: Real-time search suggestions as you type
- **Multiple Filters**: Filter by genre, platform, release year
- **Category Browsing**: Browse games by various categories
- **Random Game**: Discover games with the random game feature
- **Recently Viewed**: Track and revisit recently viewed games (stored locally)
- **Keyboard Shortcuts**: Use Ctrl+/ to focus search, Escape to close overlays

### Game Pages
- **Wikipedia-style Articles**: Detailed game pages with table of contents
- **Infoboxes**: Comprehensive game information in structured format
- **Cross-linking**: Internal links between related games, developers, and series
- **Categories**: Organized tagging system for easy navigation

## 📁 Project Structure

```
gamepedia/
├── index.html              # Main homepage
├── style.css               # Comprehensive styling
├── script.js               # Interactive functionality
├── README.md               # This documentation
├── data/
│   └── games.json          # Game database
├── games/
│   └── zelda-breath-of-the-wild.html  # Sample game page
└── assets/                 # Images and media (placeholder)
```

## 🚀 Quick Start

1. **Clone or download** the project files
2. **Open** `index.html` in your web browser
3. **Start exploring** the gaming encyclopedia!

For development with live reload, use a local server:
```bash
# Using Python
python -m http.server 8000

# Using Node.js (if you have serve installed)
npx serve .

# Using PHP
php -S localhost:8000
```

## 🎯 Usage Guide

### Basic Navigation
- **Search**: Use the prominent search bar to find games, developers, or platforms
- **Browse**: Click category cards to browse by different criteria
- **Random**: Use "Random Game" to discover new content
- **Filter**: Use the dropdown filters to narrow your search results

### Advanced Features
- **Keyboard Navigation**: 
  - `Ctrl + /` to focus search
  - `Escape` to close search suggestions or results
- **Recently Viewed**: Automatically tracks your browsing history
- **Local Storage**: Preferences and history are saved locally

### Adding New Games
To add new games to the database, edit `data/games.json`:

```json
{
  "id": 16,
  "title": "Your Game Title",
  "developer": "Developer Name",
  "publisher": "Publisher Name",
  "releaseDate": "YYYY-MM-DD",
  "platforms": ["Platform1", "Platform2"],
  "genre": "genre-name",
  "description": "Game description...",
  "imageUrl": "path/to/image.jpg",
  "categories": ["category1", "category2"],
  "tags": ["tag1", "tag2"],
  "rating": "E/E10+/T/M",
  "featured": false
}
```

### Creating Game Pages
1. Create a new HTML file in the `games/` folder
2. Use `games/zelda-breath-of-the-wild.html` as a template
3. Follow the Wikipedia-style structure with:
   - Table of contents
   - Infobox with game details
   - Detailed sections (Overview, Gameplay, Development, Reception, etc.)
   - References and categories

## 🎨 Customization

### Styling
The CSS is organized into sections:
- **Typography**: Wikipedia-inspired fonts and text styling
- **Layout**: CSS Grid and Flexbox for responsive design
- **Components**: Styled components for search, cards, infoboxes
- **Responsive**: Mobile-first breakpoints at 768px and 480px

### Color Scheme
The design uses Wikipedia's color palette:
- **Primary Text**: #222
- **Links**: #0645ad (unvisited), #0b0080 (visited)
- **Background**: #f8f9fa (light gray)
- **Borders**: #a2a9b1

### Adding New Features
The JavaScript is modular and well-documented. Key functions:
- `loadGamesDatabase()`: Loads and processes game data
- `searchGames()`: Handles search functionality
- `displaySearchResults()`: Renders search results
- `filterByCategory()`: Category-based filtering

## 📱 Responsive Design

The website is fully responsive with three main breakpoints:

- **Desktop** (1200px+): Full layout with sidebar
- **Tablet** (768px-1199px): Adapted layout
- **Mobile** (< 768px): Stacked layout, simplified navigation

## 🔧 Technical Details

### Browser Support
- Modern browsers (Chrome 60+, Firefox 55+, Safari 12+, Edge 79+)
- Progressive enhancement for older browsers
- Mobile browsers supported

### Performance
- Lightweight: ~50KB total (excluding images)
- Fast loading with minimal dependencies
- Lazy loading ready for images
- Local storage for improved UX

### Accessibility
- Semantic HTML5 structure
- ARIA labels for interactive elements
- Keyboard navigation support
- High contrast color scheme
- Print-friendly styles

## 🏗️ Development

### File Organization
- **HTML**: Semantic structure with proper document outline
- **CSS**: BEM-inspired naming, mobile-first approach
- **JavaScript**: ES6+ features, modular structure
- **JSON**: Structured data format for easy management

### Best Practices
- Clean, maintainable code
- Comprehensive commenting
- Consistent naming conventions
- Responsive images with alt text
- SEO-optimized meta tags

## 📈 Extensions & Enhancements

### Potential Features
- **User Accounts**: Registration and personalization
- **Reviews & Ratings**: Community-driven content
- **Advanced Filtering**: More granular search options
- **Image Gallery**: Enhanced visual content
- **Social Features**: Sharing and discussion
- **API Integration**: Real-time game data
- **Progressive Web App**: Offline functionality

### Content Management
- **Admin Interface**: Easy game addition/editing
- **Bulk Import**: CSV/JSON import functionality
- **Image Management**: Upload and optimization
- **Version Control**: Track changes and revisions

## 🤝 Contributing

This project serves as a template for gaming encyclopedias. Feel free to:
- Add more games to the database
- Create additional game pages
- Enhance the design and functionality
- Fix bugs or improve performance
- Suggest new features

## 📄 License

This project is open source and available under the MIT License. Feel free to use, modify, and distribute as needed.

## 🙏 Acknowledgments

- **Wikipedia**: Design inspiration and structural guidance
- **Nintendo**: Sample game data and references
- **Web Community**: Best practices and accessibility standards

---

**GamePedia** - Making gaming knowledge accessible to everyone! 🎮