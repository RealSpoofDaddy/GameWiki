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
    // For now, just show an alert. In a real implementation, this would navigate to a game page
    alert(`Opening game page for: ${game.title}\n\nThis would navigate to games/${game.title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.html`);
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