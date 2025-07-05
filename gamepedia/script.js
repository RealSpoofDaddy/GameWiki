// Global variables
let gamesDatabase = [];
let currentSearchResults = [];
let recentlyViewedGames = JSON.parse(localStorage.getItem('recentlyViewed') || '[]');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadGamesDatabase();
    initializeEventListeners();
    displayFeaturedGame();
    displayRecentGames();
    updateStatistics();
    displayRecentlyViewed();
    initializeSteamWidget();
});

// Load games database
async function loadGamesDatabase() {
    try {
        const response = await fetch('data/games.json');
        gamesDatabase = await response.json();
        updateStatistics();
        displayRecentGames();
        displayFeaturedGame();
    } catch (error) {
        console.error('Error loading games database:', error);
        // Fallback to sample data if JSON file doesn't load
        gamesDatabase = getSampleGames();
        updateStatistics();
        displayRecentGames();
        displayFeaturedGame();
    }
}

// Sample games data as fallback
function getSampleGames() {
    return [
        {
            id: 1,
            title: "The Legend of Zelda: Breath of the Wild",
            developer: "Nintendo EPD",
            publisher: "Nintendo",
            releaseDate: "2017-03-03",
            platforms: ["Nintendo Switch", "Wii U"],
            genre: "action-adventure",
            description: "An open-world action-adventure game that reinvented the Zelda formula with innovative gameplay mechanics and a vast, explorable world.",
            imageUrl: "https://via.placeholder.com/200x300/0066cc/ffffff?text=Zelda+BOTW",
            categories: ["adventure", "open-world", "nintendo"],
            tags: ["exploration", "puzzle", "fantasy"],
            rating: "E10+",
            featured: true
        },
        {
            id: 2,
            title: "Cyberpunk 2077",
            developer: "CD Projekt RED",
            publisher: "CD Projekt",
            releaseDate: "2020-12-10",
            platforms: ["PC", "PlayStation 4", "PlayStation 5", "Xbox One", "Xbox Series X/S"],
            genre: "rpg",
            description: "A futuristic RPG set in Night City, offering a deep narrative experience with cybernetic enhancements and multiple story paths.",
            imageUrl: "https://via.placeholder.com/200x300/ffcc00/000000?text=Cyberpunk+2077",
            categories: ["rpg", "sci-fi", "open-world"],
            tags: ["futuristic", "story-driven", "choices"],
            rating: "M"
        },
        {
            id: 3,
            title: "Minecraft",
            developer: "Mojang Studios",
            publisher: "Microsoft",
            releaseDate: "2011-11-18",
            platforms: ["PC", "PlayStation", "Xbox", "Nintendo Switch", "Mobile"],
            genre: "simulation",
            description: "A sandbox game that allows players to build, explore, and survive in procedurally generated worlds made of blocks.",
            imageUrl: "https://via.placeholder.com/200x300/00aa00/ffffff?text=Minecraft",
            categories: ["sandbox", "survival", "creative"],
            tags: ["building", "multiplayer", "creativity"],
            rating: "E10+"
        },
        {
            id: 4,
            title: "Among Us",
            developer: "InnerSloth",
            publisher: "InnerSloth",
            releaseDate: "2018-06-15",
            platforms: ["PC", "Mobile", "Nintendo Switch", "PlayStation", "Xbox"],
            genre: "strategy",
            description: "A multiplayer social deduction game where players work together to maintain a spaceship while identifying impostors among the crew.",
            imageUrl: "https://via.placeholder.com/200x300/ff0000/ffffff?text=Among+Us",
            categories: ["multiplayer", "social", "indie"],
            tags: ["deduction", "party", "online"],
            rating: "E10+"
        },
        {
            id: 5,
            title: "The Witcher 3: Wild Hunt",
            developer: "CD Projekt RED",
            publisher: "CD Projekt",
            releaseDate: "2015-05-19",
            platforms: ["PC", "PlayStation 4", "PlayStation 5", "Xbox One", "Xbox Series X/S", "Nintendo Switch"],
            genre: "rpg",
            description: "An epic fantasy RPG following Geralt of Rivia on his quest to find his adopted daughter in a war-torn open world.",
            imageUrl: "https://via.placeholder.com/200x300/8B0000/ffffff?text=Witcher+3",
            categories: ["rpg", "fantasy", "open-world"],
            tags: ["story-driven", "choices", "mature"],
            rating: "M"
        },
        {
            id: 6,
            title: "Super Mario Odyssey",
            developer: "Nintendo EPD",
            publisher: "Nintendo",
            releaseDate: "2017-10-27",
            platforms: ["Nintendo Switch"],
            genre: "platformer",
            description: "A 3D platformer featuring Mario and his hat companion Cappy on a globe-trotting adventure to save Princess Peach.",
            imageUrl: "https://via.placeholder.com/200x300/ff6600/ffffff?text=Mario+Odyssey",
            categories: ["platformer", "adventure", "nintendo"],
            tags: ["family-friendly", "exploration", "collectibles"],
            rating: "E10+"
        },
        {
            id: 7,
            title: "God of War (2018)",
            developer: "Santa Monica Studio",
            publisher: "Sony Interactive Entertainment",
            releaseDate: "2018-04-20",
            platforms: ["PlayStation 4", "PlayStation 5", "PC"],
            genre: "action",
            description: "A mature reboot of the God of War series, focusing on Kratos and his son Atreus in Norse mythology.",
            imageUrl: "https://via.placeholder.com/200x300/4B0082/ffffff?text=God+of+War",
            categories: ["action", "adventure", "mythology"],
            tags: ["story-driven", "combat", "father-son"],
            rating: "M"
        },
        {
            id: 8,
            title: "Fall Guys",
            developer: "Mediatonic",
            publisher: "Devolver Digital",
            releaseDate: "2020-08-04",
            platforms: ["PC", "PlayStation 4", "PlayStation 5", "Xbox One", "Xbox Series X/S", "Nintendo Switch"],
            genre: "party",
            description: "A colorful battle royale game featuring jellybean-like characters competing in whimsical obstacle courses.",
            imageUrl: "https://via.placeholder.com/200x300/FF69B4/ffffff?text=Fall+Guys",
            categories: ["party", "multiplayer", "casual"],
            tags: ["fun", "colorful", "competitive"],
            rating: "E"
        },
        {
            id: 9,
            title: "Hades",
            developer: "Supergiant Games",
            publisher: "Supergiant Games",
            releaseDate: "2020-09-17",
            platforms: ["PC", "PlayStation 4", "PlayStation 5", "Xbox One", "Xbox Series X/S", "Nintendo Switch"],
            genre: "roguelike",
            description: "A roguelike dungeon crawler where you play as Zagreus, son of Hades, attempting to escape the underworld.",
            imageUrl: "https://via.placeholder.com/200x300/DC143C/ffffff?text=Hades",
            categories: ["roguelike", "indie", "mythology"],
            tags: ["story-driven", "challenging", "replayable"],
            rating: "T"
        },
        {
            id: 10,
            title: "Animal Crossing: New Horizons",
            developer: "Nintendo EPD",
            publisher: "Nintendo",
            releaseDate: "2020-03-20",
            platforms: ["Nintendo Switch"],
            genre: "simulation",
            description: "A life simulation game where players develop a deserted island into a thriving community of anthropomorphic animals.",
            imageUrl: "https://via.placeholder.com/200x300/90EE90/000000?text=Animal+Crossing",
            categories: ["simulation", "social", "nintendo"],
            tags: ["relaxing", "customization", "social"],
            rating: "E"
        }
    ];
}

// Initialize event listeners
function initializeEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const genreFilter = document.getElementById('genreFilter');
    const platformFilter = document.getElementById('platformFilter');
    const yearFilter = document.getElementById('yearFilter');

    // Search functionality
    searchInput.addEventListener('input', handleSearchInput);
    searchInput.addEventListener('focus', showSearchSuggestions);
    searchInput.addEventListener('blur', hideSearchSuggestions);
    searchBtn.addEventListener('click', performSearch);

    // Filter functionality
    genreFilter.addEventListener('change', applyFilters);
    platformFilter.addEventListener('change', applyFilters);
    yearFilter.addEventListener('change', applyFilters);

    // Keyboard navigation
    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey && event.key === '/') {
            event.preventDefault();
            searchInput.focus();
        }
        if (event.key === 'Escape') {
            hideSearchSuggestions();
            hideSearchResults();
        }
    });
}

// Search input handler
function handleSearchInput(event) {
    const query = event.target.value.trim();
    
    if (query.length > 2) {
        showSearchSuggestions();
        updateSearchSuggestions(query);
    } else {
        hideSearchSuggestions();
    }
    
    if (query.length === 0) {
        hideSearchResults();
    }
}

// Update search suggestions
function updateSearchSuggestions(query) {
    const suggestions = gamesDatabase
        .filter(game => 
            game.title.toLowerCase().includes(query.toLowerCase()) ||
            game.developer.toLowerCase().includes(query.toLowerCase()) ||
            game.genre.toLowerCase().includes(query.toLowerCase())
        )
        .slice(0, 5);

    displaySearchSuggestions(suggestions, query);
}

// Display search suggestions
function displaySearchSuggestions(suggestions, query) {
    const suggestionsContainer = document.getElementById('searchSuggestions');
    
    if (suggestions.length === 0) {
        suggestionsContainer.style.display = 'none';
        return;
    }

    suggestionsContainer.innerHTML = suggestions
        .map(game => `
            <div class="suggestion-item" onclick="selectGame(${game.id})">
                <strong>${highlightMatch(game.title, query)}</strong>
                <br>
                <small>${game.developer} • ${game.releaseDate.split('-')[0]} • ${game.genre}</small>
            </div>
        `)
        .join('');
    
    suggestionsContainer.style.display = 'block';
}

// Highlight matching text
function highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
}

// Show/hide search suggestions
function showSearchSuggestions() {
    const query = document.getElementById('searchInput').value.trim();
    if (query.length > 2) {
        updateSearchSuggestions(query);
    }
}

function hideSearchSuggestions() {
    setTimeout(() => {
        document.getElementById('searchSuggestions').style.display = 'none';
    }, 200);
}

// Perform search
function performSearch() {
    const query = document.getElementById('searchInput').value.trim();
    
    if (query.length === 0) {
        hideSearchResults();
        return;
    }

    const results = searchGames(query);
    displaySearchResults(results, query);
    hideSearchSuggestions();
}

// Search games
function searchGames(query) {
    const lowerQuery = query.toLowerCase();
    
    return gamesDatabase.filter(game => 
        game.title.toLowerCase().includes(lowerQuery) ||
        game.developer.toLowerCase().includes(lowerQuery) ||
        game.publisher.toLowerCase().includes(lowerQuery) ||
        game.genre.toLowerCase().includes(lowerQuery) ||
        game.description.toLowerCase().includes(lowerQuery) ||
        game.platforms.some(platform => platform.toLowerCase().includes(lowerQuery)) ||
        game.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
    );
}

// Apply filters
function applyFilters() {
    const genre = document.getElementById('genreFilter').value;
    const platform = document.getElementById('platformFilter').value;
    const year = document.getElementById('yearFilter').value;
    const query = document.getElementById('searchInput').value.trim();

    let results = query ? searchGames(query) : gamesDatabase;

    if (genre) {
        results = results.filter(game => game.genre === genre);
    }

    if (platform) {
        results = results.filter(game => 
            game.platforms.some(p => p.toLowerCase().includes(platform.toLowerCase()))
        );
    }

    if (year) {
        results = results.filter(game => game.releaseDate.startsWith(year));
    }

    displaySearchResults(results, query || 'filtered results');
}

// Display search results
function displaySearchResults(results, query) {
    const searchResultsSection = document.getElementById('searchResults');
    const resultsList = document.getElementById('resultsList');
    
    if (results.length === 0) {
        resultsList.innerHTML = `
            <div class="result-item">
                <h3 class="result-title">No results found</h3>
                <p class="result-description">No games match your search criteria.</p>
            </div>
        `;
    } else {
        resultsList.innerHTML = results
            .map(game => `
                <div class="result-item" onclick="selectGame(${game.id})">
                    <h3 class="result-title">${game.title}</h3>
                    <div class="result-meta">
                        ${game.developer} • ${game.releaseDate.split('-')[0]} • ${game.genre} • ${game.platforms.join(', ')}
                    </div>
                    <p class="result-description">${game.description}</p>
                </div>
            `)
            .join('');
    }
    
    searchResultsSection.style.display = 'block';
    currentSearchResults = results;
}

// Hide search results
function hideSearchResults() {
    document.getElementById('searchResults').style.display = 'none';
    currentSearchResults = [];
}

// Select game
function selectGame(gameId) {
    const game = gamesDatabase.find(g => g.id === gameId);
    if (game) {
        addToRecentlyViewed(game);
        openGamePage(game);
    }
}

// Open game page
function openGamePage(game) {
    // Use the router to navigate to the game page
    if (window.gameRouter) {
        gameRouter.navigateToGame(game.id);
    } else {
        // Fallback if router isn't loaded yet
        window.location.hash = `game/${game.title.toLowerCase().replace(/[^a-z0-9\s]/g, '').replace(/\s+/g, '-')}`;
    }
}

// Display featured game
function displayFeaturedGame() {
    const featuredContainer = document.getElementById('featuredGame');
    
    // Try to find a featured game, or pick a random one
    let featuredGame = gamesDatabase.find(game => game.featured);
    if (!featuredGame && gamesDatabase.length > 0) {
        featuredGame = gamesDatabase[Math.floor(Math.random() * gamesDatabase.length)];
    }
    
    if (featuredGame) {
        featuredContainer.innerHTML = `
            <img src="${featuredGame.imageUrl}" alt="${featuredGame.title}" class="featured-game-image">
            <div class="featured-game-info">
                <h3><a href="#" onclick="selectGame(${featuredGame.id})">${featuredGame.title}</a></h3>
                <div class="featured-game-meta">
                    ${featuredGame.developer} • ${featuredGame.releaseDate.split('-')[0]} • ${featuredGame.platforms.join(', ')}
                </div>
                <p>${featuredGame.description}</p>
                <p><a href="#" onclick="selectGame(${featuredGame.id})">Read more...</a></p>
            </div>
        `;
    }
}

// Display recent games
function displayRecentGames() {
    const recentContainer = document.getElementById('recentGames');
    
    if (gamesDatabase.length === 0) {
        recentContainer.innerHTML = '<p>Loading games...</p>';
        return;
    }
    
    // Get 6 most recent games (by release date)
    const recentGames = gamesDatabase
        .sort((a, b) => new Date(b.releaseDate) - new Date(a.releaseDate))
        .slice(0, 6);
    
    recentContainer.innerHTML = recentGames
        .map(game => `
            <div class="game-card" onclick="selectGame(${game.id})">
                <img src="${game.imageUrl}" alt="${game.title}" class="game-card-image">
                <h4>${game.title}</h4>
                <div class="game-card-meta">${game.developer} • ${game.releaseDate.split('-')[0]}</div>
            </div>
        `)
        .join('');
}

// Update statistics
function updateStatistics() {
    const totalGames = gamesDatabase.length;
    const totalDevelopers = new Set(gamesDatabase.map(game => game.developer)).size;
    const totalPlatforms = new Set(gamesDatabase.flatMap(game => game.platforms)).size;
    
    document.getElementById('totalGames').textContent = totalGames;
    document.getElementById('totalDevelopers').textContent = totalDevelopers;
    document.getElementById('totalPlatforms').textContent = totalPlatforms;
}

// Recently viewed functionality
function addToRecentlyViewed(game) {
    recentlyViewedGames = recentlyViewedGames.filter(g => g.id !== game.id);
    recentlyViewedGames.unshift(game);
    
    if (recentlyViewedGames.length > 5) {
        recentlyViewedGames = recentlyViewedGames.slice(0, 5);
    }
    
    localStorage.setItem('recentlyViewed', JSON.stringify(recentlyViewedGames));
    displayRecentlyViewed();
}

function displayRecentlyViewed() {
    const container = document.getElementById('recentlyViewed');
    
    if (recentlyViewedGames.length === 0) {
        container.innerHTML = '<p class="no-recent">No recently viewed games</p>';
        return;
    }
    
    container.innerHTML = recentlyViewedGames
        .map(game => `
            <div class="recent-item">
                <a href="#" onclick="selectGame(${game.id})">${game.title}</a>
            </div>
        `)
        .join('');
}

// Category filtering
function filterByCategory(category) {
    let results = [];
    
    switch (category) {
        case 'platform':
            // Group by platform and show results
            const platforms = new Set(gamesDatabase.flatMap(game => game.platforms));
            results = gamesDatabase; // Show all for now
            break;
        case 'genre':
            // Group by genre
            const genres = new Set(gamesDatabase.map(game => game.genre));
            results = gamesDatabase;
            break;
        case 'year':
            // Group by year
            const years = new Set(gamesDatabase.map(game => game.releaseDate.split('-')[0]));
            results = gamesDatabase;
            break;
        case 'developer':
            // Group by developer
            const developers = new Set(gamesDatabase.map(game => game.developer));
            results = gamesDatabase;
            break;
    }
    
    displaySearchResults(results, `Browse by ${category}`);
}

// Quick navigation functions
function showNewGames() {
    const newGames = gamesDatabase
        .filter(game => new Date(game.releaseDate) > new Date('2023-01-01'))
        .sort((a, b) => new Date(b.releaseDate) - new Date(a.releaseDate));
    
    displaySearchResults(newGames, 'New Releases');
}

function showClassicGames() {
    const classicGames = gamesDatabase
        .filter(game => new Date(game.releaseDate) < new Date('2010-01-01'));
    
    displaySearchResults(classicGames, 'Classic Games');
}

function showIndieGames() {
    const indieGames = gamesDatabase
        .filter(game => game.categories.includes('indie'));
    
    displaySearchResults(indieGames, 'Indie Games');
}

function showMultiplayerGames() {
    const multiplayerGames = gamesDatabase
        .filter(game => 
            game.categories.includes('multiplayer') || 
            game.tags.includes('multiplayer') || 
            game.tags.includes('online')
        );
    
    displaySearchResults(multiplayerGames, 'Multiplayer Games');
}

// Random game function
function randomGame() {
    if (gamesDatabase.length > 0) {
        const randomGame = gamesDatabase[Math.floor(Math.random() * gamesDatabase.length)];
        selectGame(randomGame.id);
    }
}

// Browse section functions
function showBrowseSection() {
    document.getElementById('searchResults').style.display = 'none';
    // Could implement a dedicated browse interface here
    alert('Browse functionality - this would show a dedicated browsing interface');
}

function showCategoriesSection() {
    document.getElementById('searchResults').style.display = 'none';
    // Could implement a categories view here
    alert('Categories functionality - this would show all available categories');
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Enhanced search with debouncing
const debouncedSearch = debounce(handleSearchInput, 300);

// Initialize search with debouncing
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.removeEventListener('input', handleSearchInput);
        searchInput.addEventListener('input', debouncedSearch);
    }
});

// Export functions for use in HTML
window.selectGame = selectGame;
window.randomGame = randomGame;
window.filterByCategory = filterByCategory;
window.showBrowseSection = showBrowseSection;
window.showCategoriesSection = showCategoriesSection;
window.showNewGames = showNewGames;
window.showClassicGames = showClassicGames;
window.showIndieGames = showIndieGames;
window.showMultiplayerGames = showMultiplayerGames;
window.addToRecentlyViewed = addToRecentlyViewed;
window.applyFilters = applyFilters;

// Enhanced Steam Widget - Ultimate Gaming Features
class SteamWidget {
    constructor() {
        this.baseUrl = window.location.origin;
        this.isDemo = false;
        this.sessionToken = localStorage.getItem('steam_session_token') || null;
        this.demoData = {
            // Enhanced demo data with comprehensive features
            player: {
                personaname: "GameMaster Pro",
                avatarfull: "https://avatars.steamstatic.com/b5bd56c1aa4644a474a2e4972be27ef9e82e517e_full.jpg",
                personastate: 1,
                profileurl: "https://steamcommunity.com/profiles/76561198123456789"
            },
            stats: {
                total_games: 247,
                total_playtime: "3,847 hours",
                most_played: "Counter-Strike 2",
                average_playtime: "15.6 hours",
                games_never_played: 23,
                games_played_recently: 12
            },
            recentGames: [
                {
                    appid: 730,
                    name: "Counter-Strike 2",
                    playtime_forever: 1847,
                    playtime_2weeks: 32,
                    img_icon_url: "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/730/69f7ebe2735c366c65c0b33dae00e12dc40edbe4.jpg",
                    header_image: "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg",
                    short_description: "For over two decades, Counter-Strike has offered an elite competitive experience...",
                    genres: "Action, Free to Play",
                    metacritic_score: 83,
                    price_current: 0,
                    achievements_count: 167
                },
                {
                    appid: 1091500,
                    name: "Cyberpunk 2077",
                    playtime_forever: 156,
                    playtime_2weeks: 28,
                    img_icon_url: "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/1091500/836fb70d06ed5a7e4b3b4c2b7a8c1a7ecb1e9d6e.jpg",
                    header_image: "https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/header.jpg",
                    short_description: "Cyberpunk 2077 is an open-world, action-adventure RPG set in the megalopolis of Night City...",
                    genres: "RPG, Action, Adventure",
                    metacritic_score: 86,
                    price_current: 29.99,
                    price_original: 59.99,
                    price_discount_percent: 50,
                    achievements_count: 44
                },
                {
                    appid: 1086940,
                    name: "Baldur's Gate 3",
                    playtime_forever: 89,
                    playtime_2weeks: 15,
                    img_icon_url: "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/1086940/8c1c6e2e2e7e2e2e2e2e2e2e2e2e2e2e2e2e2e2e.jpg",
                    header_image: "https://cdn.cloudflare.steamstatic.com/steam/apps/1086940/header.jpg",
                    short_description: "Baldur's Gate 3 is a story-rich, party-based RPG set in the universe of Dungeons & Dragons...",
                    genres: "RPG, Strategy, Adventure",
                    metacritic_score: 96,
                    price_current: 59.99,
                    achievements_count: 54
                }
            ],
            topGames: [
                {
                    appid: 730,
                    name: "Counter-Strike 2",
                    playtime_forever: 1847,
                    metacritic_score: 83,
                    achievements_count: 167
                },
                {
                    appid: 1091500,
                    name: "Cyberpunk 2077",
                    playtime_forever: 156,
                    metacritic_score: 86,
                    achievements_count: 44
                }
            ],
            achievements: {
                730: { total: 167, unlocked: 89, percentage: 53.3 },
                1091500: { total: 44, unlocked: 23, percentage: 52.3 }
            },
            recommendations: [
                {
                    name: "The Witcher 3: Wild Hunt",
                    reason: "Based on your RPG preferences",
                    score: 93,
                    price: 39.99
                },
                {
                    name: "Elden Ring",
                    reason: "Highly rated action RPG",
                    score: 96,
                    price: 59.99
                }
            ]
        };
        
        this.init();
    }

    async init() {
        // Check if we have a valid session token
        if (this.sessionToken) {
            try {
                const isValid = await this.validateSession();
                if (isValid) {
                    this.isDemo = false;
                    this.startUpdates();
                } else {
                    this.sessionToken = null;
                    localStorage.removeItem('steam_session_token');
                    this.showConfiguration();
                }
            } catch (error) {
                console.error('Session validation error:', error);
                this.showDemoMode();
            }
        } else {
            this.showConfiguration();
        }
    }

    async validateSession() {
        try {
            const response = await fetch(`${this.baseUrl}/api/steam/validate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_token: this.sessionToken
                })
            });

            return response.ok;
        } catch (error) {
            console.error('Session validation error:', error);
            return false;
        }
    }

    showConfiguration() {
        const widget = document.getElementById('steamStatus');
        if (!widget) return;

        widget.innerHTML = `
            <div class="steam-config">
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 2.5em; margin-bottom: 10px;">🎮</div>
                    <h4 style="color: #ffffff; margin: 0;">Connect Your Steam Account</h4>
                    <p style="color: #c7d5e0; font-size: 0.85em; margin: 8px 0;">Access advanced gaming features and comprehensive statistics</p>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <label>Steam API Key:</label>
                    <input type="password" id="steamApiKey" placeholder="Enter your Steam API key" 
                           style="margin-bottom: 10px;">
                    
                    <label>Steam ID:</label>
                    <input type="text" id="steamId" placeholder="Enter your Steam ID" 
                           style="margin-bottom: 15px;">
                    
                    <button class="steam-connect-btn" onclick="steamWidget.authenticateUser()">
                        🔐 Connect & Enable Advanced Features
                    </button>
                    
                    <button class="steam-connect-btn" onclick="steamWidget.showDemoMode()" 
                            style="margin-top: 10px; background: rgba(255, 255, 255, 0.1); color: #c7d5e0;">
                        👁️ View Demo Instead
                    </button>
                </div>
                
                <div class="steam-help-text">
                    <h5 style="color: #ffffff; margin: 0 0 10px 0;">🚀 Advanced Features:</h5>
                    <p style="margin: 5px 0;">• <strong>Real-time Data:</strong> Live Steam statistics and game tracking</p>
                    <p style="margin: 5px 0;">• <strong>Achievement Tracking:</strong> Progress monitoring across all games</p>
                    <p style="margin: 5px 0;">• <strong>Game Recommendations:</strong> AI-powered suggestions based on your library</p>
                    <p style="margin: 5px 0;">• <strong>Price Alerts:</strong> Notifications for wishlist games on sale</p>
                    <p style="margin: 5px 0;">• <strong>Comprehensive Analytics:</strong> Detailed gaming insights</p>
                    
                    <h5 style="color: #ffffff; margin: 15px 0 10px 0;">🔗 Quick Setup:</h5>
                    <p style="margin: 5px 0;">• <strong>API Key:</strong> <a href="https://steamcommunity.com/dev/apikey" target="_blank">Get your key here</a></p>
                    <p style="margin: 5px 0;">• <strong>Steam ID:</strong> <a href="https://steamidfinder.com/" target="_blank">Find your ID here</a></p>
                    <p style="margin: 10px 0 0 0; font-size: 0.8em; color: #98a8b0;">
                        🔒 <strong>Military-Grade Security:</strong> Your credentials are encrypted with AES-256 and stored securely server-side.
                    </p>
                </div>
            </div>
        `;
    }

    showDemoMode() {
        this.isDemo = true;
        this.displayComprehensiveData(this.demoData);
        this.showDemoIndicator();
    }

    showDemoIndicator() {
        const widget = document.getElementById('steamStatus');
        if (!widget) return;

        // Add demo indicator
        const demoIndicator = document.createElement('div');
        demoIndicator.style.cssText = `
            background: linear-gradient(135deg, #ff6b6b, #ffa500);
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.85em;
            text-align: center;
            margin-bottom: 20px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.2);
        `;
        demoIndicator.innerHTML = '🎭 Demo Mode - <a href="#" onclick="steamWidget.showConfiguration()" style="color: white; text-decoration: underline; font-weight: 700;">Connect Real Account for Advanced Features</a>';
        widget.insertBefore(demoIndicator, widget.firstChild);
    }

    async authenticateUser() {
        const apiKey = document.getElementById('steamApiKey').value.trim();
        const steamId = document.getElementById('steamId').value.trim();

        if (!apiKey || !steamId) {
            this.showError('Please enter both Steam API Key and Steam ID');
            return;
        }

        // Show loading state
        const widget = document.getElementById('steamStatus');
        widget.innerHTML = `
            <div class="steam-loading">
                <div class="loading-spinner"></div>
                <p>🔐 Establishing Secure Connection...</p>
                <p style="font-size: 0.8em; color: #98a8b0;">Encrypting credentials and validating with Steam API</p>
                <div style="margin-top: 15px; font-size: 0.75em; color: #7a8c98;">
                    <p>• Validating Steam API credentials</p>
                    <p>• Creating encrypted session</p>
                    <p>• Initializing advanced features</p>
                </div>
            </div>
        `;

        try {
            // Send credentials to server for secure authentication
            const response = await fetch(`${this.baseUrl}/api/steam/authenticate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    api_key: apiKey,
                    steam_id: steamId
                })
            });

            const result = await response.json();

            if (response.ok && result.session_token) {
                // Store only the secure session token
                this.sessionToken = result.session_token;
                localStorage.setItem('steam_session_token', this.sessionToken);
                
                this.isDemo = false;
                this.startUpdates();
                
                // Show success message
                this.showSuccess('✅ Advanced Gaming Features Activated!');
                
            } else {
                this.showError(result.error || 'Authentication failed. Please check your credentials.');
            }
        } catch (error) {
            console.error('Steam authentication error:', error);
            this.showError('Connection failed. Please try again.');
        }
    }

    async startUpdates() {
        await this.updateSteamData();
        
        // Set up automatic updates every 5 minutes
        setInterval(async () => {
            await this.updateSteamData();
        }, 300000);
    }

    async updateSteamData() {
        if (this.isDemo) return;

        try {
            const response = await fetch(`${this.baseUrl}/api/steam/user-data`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_token: this.sessionToken
                })
            });

            if (!response.ok) {
                throw new Error('Failed to fetch Steam data');
            }

            const steamData = await response.json();
            this.displayComprehensiveData(steamData);

        } catch (error) {
            console.error('Error updating Steam data:', error);
            this.showError('Failed to update Steam data');
        }
    }

    displayComprehensiveData(data) {
        const widget = document.getElementById('steamStatus');
        if (!widget) return;

        // Create comprehensive layout
        widget.innerHTML = `
            <div class="steam-comprehensive-layout">
                <div id="playerInfo"></div>
                <div id="enhancedStats"></div>
                <div id="recentGamesSection"></div>
                <div id="achievementsSection"></div>
                <div id="recommendationsSection"></div>
            </div>
        `;

        // Display each section
        this.displayPlayerInfo(data.player);
        this.displayEnhancedStats(data.stats);
        this.displayRecentGames(data.recentGames || data.topGames);
        this.displayAchievements(data.achievements);
        this.displayRecommendations(data.recommendations);
    }

    displayPlayerInfo(player) {
        const container = document.getElementById('playerInfo');
        if (!container || !player) return;

        const statusMap = {
            0: { text: "Offline", class: "steam-status-offline" },
            1: { text: "Online", class: "steam-status-online" },
            2: { text: "Busy", class: "steam-status-online" },
            3: { text: "Away", class: "steam-status-offline" },
            4: { text: "Snooze", class: "steam-status-offline" },
            5: { text: "Looking to trade", class: "steam-status-online" },
            6: { text: "Looking to play", class: "steam-status-online" }
        };

        const status = statusMap[player.personastate] || statusMap[0];

        container.innerHTML = `
            <div class="steam-player-info">
                <img src="${player.avatarfull}" alt="${player.personaname}" class="steam-avatar">
                <div class="steam-player-details">
                    <h4>${player.personaname}</h4>
                    <div class="steam-player-status ${status.class}">
                        ${status.text}
                    </div>
                    ${player.profileurl ? `<a href="${player.profileurl}" target="_blank" style="color: #66c0f4; font-size: 0.8em; text-decoration: none;">View Steam Profile →</a>` : ''}
                </div>
            </div>
        `;
    }

    displayEnhancedStats(stats) {
        const container = document.getElementById('enhancedStats');
        if (!container || !stats) return;

        container.innerHTML = `
            <div class="steam-enhanced-stats">
                <h4 style="color: #ffffff; margin: 0 0 15px 0; font-size: 1em;">📊 Gaming Analytics</h4>
                <div class="steam-stats-grid">
                    <div class="steam-stat-card">
                        <div class="steam-stat-icon">🎮</div>
                        <div class="steam-stat-content">
                            <div class="steam-stat-value">${stats.total_games}</div>
                            <div class="steam-stat-label">Total Games</div>
                        </div>
                    </div>
                    <div class="steam-stat-card">
                        <div class="steam-stat-icon">⏱️</div>
                        <div class="steam-stat-content">
                            <div class="steam-stat-value">${stats.total_playtime}</div>
                            <div class="steam-stat-label">Total Playtime</div>
                        </div>
                    </div>
                    <div class="steam-stat-card">
                        <div class="steam-stat-icon">🏆</div>
                        <div class="steam-stat-content">
                            <div class="steam-stat-value">${stats.most_played}</div>
                            <div class="steam-stat-label">Most Played</div>
                        </div>
                    </div>
                    <div class="steam-stat-card">
                        <div class="steam-stat-icon">📈</div>
                        <div class="steam-stat-content">
                            <div class="steam-stat-value">${stats.average_playtime || 'N/A'}</div>
                            <div class="steam-stat-label">Avg Playtime</div>
                        </div>
                    </div>
                    <div class="steam-stat-card">
                        <div class="steam-stat-icon">🎯</div>
                        <div class="steam-stat-content">
                            <div class="steam-stat-value">${stats.games_played_recently || 0}</div>
                            <div class="steam-stat-label">Recently Active</div>
                        </div>
                    </div>
                    <div class="steam-stat-card">
                        <div class="steam-stat-icon">📚</div>
                        <div class="steam-stat-content">
                            <div class="steam-stat-value">${stats.games_never_played || 0}</div>
                            <div class="steam-stat-label">Backlog</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    displayRecentGames(games) {
        const container = document.getElementById('recentGamesSection');
        if (!container || !games || games.length === 0) return;

        const gamesList = games.slice(0, 5).map(game => {
            const playtimeHours = Math.floor(game.playtime_forever / 60);
            const playtimeMinutes = game.playtime_forever % 60;
            const playtimeText = playtimeHours > 0 ? `${playtimeHours}h ${playtimeMinutes}m` : `${playtimeMinutes}m`;
            
            const recentPlaytime = game.playtime_2weeks ? `+${Math.floor(game.playtime_2weeks / 60)}h this week` : '';
            
            return `
                <div class="steam-enhanced-game-card" onclick="steamWidget.showGameDetails(${game.appid}, '${game.name}')">
                    <div class="steam-game-header">
                        ${game.header_image ? `<img src="${game.header_image}" alt="${game.name}" class="steam-game-header-img">` : ''}
                        <div class="steam-game-overlay">
                            <h5 class="steam-game-name">${game.name}</h5>
                            <div class="steam-game-meta">
                                <span class="steam-playtime">${playtimeText}</span>
                                ${recentPlaytime ? `<span class="steam-recent-time">${recentPlaytime}</span>` : ''}
                            </div>
                        </div>
                    </div>
                    <div class="steam-game-details">
                        ${game.short_description ? `<p class="steam-game-desc">${game.short_description.substring(0, 80)}...</p>` : ''}
                        <div class="steam-game-info-row">
                            ${game.genres ? `<span class="steam-genre-tag">${game.genres.split(',')[0]}</span>` : ''}
                            ${game.metacritic_score ? `<span class="steam-score-badge">${game.metacritic_score}</span>` : ''}
                            ${game.price_current !== undefined ? 
                                `<span class="steam-price-tag ${game.price_discount_percent ? 'discounted' : ''}">
                                    ${game.price_current === 0 ? 'Free' : `$${game.price_current}`}
                                    ${game.price_discount_percent ? `<s>$${game.price_original}</s>` : ''}
                                </span>` : ''
                            }
                        </div>
                        ${game.achievements_count ? `<div class="steam-achievement-mini">🏆 ${game.achievements_count} achievements</div>` : ''}
                    </div>
                </div>
            `;
        }).join('');

        container.innerHTML = `
            <div class="steam-recent-games-enhanced">
                <h4 style="color: #ffffff; margin: 0 0 15px 0; font-size: 1em;">🎮 Recently Played Games</h4>
                <div class="steam-games-grid">
                    ${gamesList}
                </div>
                <button class="steam-view-all-btn" onclick="steamWidget.showAllGames()">
                    View All Games →
                </button>
            </div>
        `;
    }

    displayAchievements(achievements) {
        const container = document.getElementById('achievementsSection');
        if (!container || !achievements) return;

        const achievementsList = Object.entries(achievements).map(([appId, data]) => {
            return `
                <div class="steam-achievement-item">
                    <div class="steam-achievement-progress">
                        <div class="steam-achievement-info">
                            <span class="steam-achievement-count">${data.unlocked}/${data.total}</span>
                            <span class="steam-achievement-percentage">${data.percentage.toFixed(1)}%</span>
                        </div>
                        <div class="steam-achievement-bar">
                            <div class="steam-achievement-fill" style="width: ${data.percentage}%"></div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        const totalAchievements = Object.values(achievements).reduce((sum, data) => sum + data.total, 0);
        const unlockedAchievements = Object.values(achievements).reduce((sum, data) => sum + data.unlocked, 0);
        const overallPercentage = totalAchievements > 0 ? (unlockedAchievements / totalAchievements * 100) : 0;

        container.innerHTML = `
            <div class="steam-achievements-section">
                <h4 style="color: #ffffff; margin: 0 0 15px 0; font-size: 1em;">🏆 Achievement Progress</h4>
                <div class="steam-overall-achievement">
                    <div class="steam-achievement-summary">
                        <span class="steam-achievement-total">${unlockedAchievements}/${totalAchievements} Achievements</span>
                        <span class="steam-achievement-overall">${overallPercentage.toFixed(1)}% Complete</span>
                    </div>
                    <div class="steam-achievement-bar-main">
                        <div class="steam-achievement-fill-main" style="width: ${overallPercentage}%"></div>
                    </div>
                </div>
                ${achievementsList}
            </div>
        `;
    }

    displayRecommendations(recommendations) {
        const container = document.getElementById('recommendationsSection');
        if (!container || !recommendations || recommendations.length === 0) return;

        const recommendationsList = recommendations.map(rec => {
            return `
                <div class="steam-recommendation-card">
                    <div class="steam-rec-content">
                        <h5 class="steam-rec-title">${rec.name}</h5>
                        <p class="steam-rec-reason">${rec.reason}</p>
                        <div class="steam-rec-meta">
                            <span class="steam-rec-score">⭐ ${rec.score}/100</span>
                            <span class="steam-rec-price">$${rec.price}</span>
                        </div>
                    </div>
                    <button class="steam-rec-btn" onclick="steamWidget.viewOnSteam('${rec.name}')">
                        View on Steam
                    </button>
                </div>
            `;
        }).join('');

        container.innerHTML = `
            <div class="steam-recommendations-section">
                <h4 style="color: #ffffff; margin: 0 0 15px 0; font-size: 1em;">🎯 Recommended For You</h4>
                <div class="steam-recommendations-grid">
                    ${recommendationsList}
                </div>
            </div>
        `;
    }

    showGameDetails(appId, gameName) {
        // Create modal for game details
        const modal = document.createElement('div');
        modal.className = 'steam-game-modal';
        modal.innerHTML = `
            <div class="steam-modal-content">
                <div class="steam-modal-header">
                    <h3>${gameName}</h3>
                    <button class="steam-modal-close" onclick="this.parentElement.parentElement.parentElement.remove()">×</button>
                </div>
                <div class="steam-modal-body">
                    <p>Loading game details...</p>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    showAllGames() {
        this.showInfo('Game library view coming soon!');
    }

    viewOnSteam(gameName) {
        const searchUrl = `https://store.steampowered.com/search/?term=${encodeURIComponent(gameName)}`;
        window.open(searchUrl, '_blank');
    }

    launchGame(appId) {
        if (this.isDemo) {
            this.showInfo('Demo mode - Game launching not available');
            return;
        }
        
        window.open(`steam://rungameid/${appId}`, '_blank');
    }

    showError(message) {
        const widget = document.getElementById('steamStatus');
        if (!widget) return;

        widget.innerHTML = `
            <div class="steam-error">
                <div class="steam-error-icon">⚠️</div>
                <p>${message}</p>
                <button class="steam-connect-btn" onclick="steamWidget.showConfiguration()" style="margin-top: 15px;">
                    Try Again
                </button>
            </div>
        `;
    }

    showSuccess(message) {
        const widget = document.getElementById('steamStatus');
        if (!widget) return;

        widget.innerHTML = `
            <div style="text-align: center; padding: 30px 20px; color: #4caf50;">
                <div style="font-size: 3em; margin-bottom: 15px;">✅</div>
                <p style="font-size: 1.1em; font-weight: 600;">${message}</p>
                <p style="font-size: 0.85em; color: #98a8b0; margin-top: 10px;">Loading your comprehensive gaming data...</p>
            </div>
        `;

        // Clear success message after 3 seconds
        setTimeout(() => {
            this.updateSteamData();
        }, 3000);
    }

    showInfo(message) {
        const infoDiv = document.createElement('div');
        infoDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #66c0f4, #57cbde);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            font-size: 0.9em;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
        `;
        infoDiv.textContent = message;
        document.body.appendChild(infoDiv);

        setTimeout(() => {
            infoDiv.remove();
        }, 3000);
    }

    disconnect() {
        this.sessionToken = null;
        localStorage.removeItem('steam_session_token');
        this.isDemo = true;
        this.showConfiguration();
    }
}

// Initialize Steam Widget when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('steamStatus')) {
        window.steamWidget = new SteamWidget();
    }
});

// Clean up when page is unloaded
window.addEventListener('beforeunload', function() {
    if (window.steamWidget) {
        window.steamWidget.disconnect();
    }
});