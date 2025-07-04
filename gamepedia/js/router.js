/**
 * Router Module - Handles hash-based navigation for dynamic game pages
 * Enables URLs like: gamepedia/index.html#game/zelda-breath-of-the-wild
 */

class GameRouter {
    constructor() {
        this.routes = {
            'home': this.showHomePage.bind(this),
            'game': this.showGamePage.bind(this)
        };
        
        this.currentRoute = null;
        this.currentGameId = null;
        
        // Listen for hash changes
        window.addEventListener('hashchange', () => this.handleRoute());
        window.addEventListener('load', () => this.handleRoute());
    }

    /**
     * Handle route changes
     */
    handleRoute() {
        const hash = window.location.hash.slice(1); // Remove the #
        
        if (!hash) {
            this.showHomePage();
            return;
        }

        const [route, ...params] = hash.split('/');
        
        if (this.routes[route]) {
            this.routes[route](params);
        } else {
            this.showHomePage();
        }
    }

    /**
     * Navigate to a specific route
     */
    navigate(path) {
        window.location.hash = path;
    }

    /**
     * Show the home page
     */
    showHomePage() {
        this.currentRoute = 'home';
        this.currentGameId = null;
        
        // Show main content, hide game page
        document.getElementById('mainContent').style.display = 'block';
        document.getElementById('gamePageContainer').style.display = 'none';
        
        // Update page title
        document.title = 'GamePedia - The Free Gaming Encyclopedia';
        
        // Clear active navigation
        this.updateNavigation();
    }

    /**
     * Show a game page
     */
    showGamePage(params) {
        if (!params[0]) {
            this.showHomePage();
            return;
        }

        const gameSlug = params[0];
        const game = this.findGameBySlug(gameSlug);
        
        if (!game) {
            this.showHomePage();
            return;
        }

        this.currentRoute = 'game';
        this.currentGameId = game.id;
        
        // Hide main content, show game page
        document.getElementById('mainContent').style.display = 'none';
        document.getElementById('gamePageContainer').style.display = 'block';
        
        // Render the game page
        this.renderGamePage(game);
        
        // Update page title
        document.title = `${game.title} - GamePedia`;
        
        // Add to recently viewed
        if (window.addToRecentlyViewed) {
            window.addToRecentlyViewed(game);
        }
        
        // Update navigation
        this.updateNavigation();
    }

    /**
     * Find game by slug (URL-friendly version of title)
     */
    findGameBySlug(slug) {
        return gamesDatabase.find(game => this.gameToSlug(game.title) === slug);
    }

    /**
     * Convert game title to URL-friendly slug
     */
    gameToSlug(title) {
        return title
            .toLowerCase()
            .replace(/[^a-z0-9\s]/g, '') // Remove special characters
            .replace(/\s+/g, '-') // Replace spaces with hyphens
            .replace(/-+/g, '-') // Replace multiple hyphens with single
            .replace(/^-|-$/g, ''); // Remove leading/trailing hyphens
    }

    /**
     * Get URL for a game
     */
    getGameUrl(game) {
        return `#game/${this.gameToSlug(game.title)}`;
    }

    /**
     * Render the game page
     */
    renderGamePage(game) {
        const container = document.getElementById('gamePageContent');
        
        // Format release date
        const releaseDate = new Date(game.releaseDate);
        const formattedDate = releaseDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        // Get game URL for sharing
        const gameUrl = this.getGameUrl(game);

        container.innerHTML = `
            <div class="game-page-header">
                <button class="back-button" onclick="gameRouter.navigate('')">
                    ← Back to Home
                </button>
                <div class="breadcrumb">
                    <a href="#" onclick="gameRouter.navigate('')">Home</a> > 
                    <span>${game.title}</span>
                </div>
            </div>

            <article class="game-article">
                <header class="game-header">
                    <div class="game-header-content">
                        <div class="game-image-container">
                            <img src="${game.imageUrl}" alt="${game.title}" class="game-main-image">
                        </div>
                        <div class="game-title-section">
                            <h1 class="game-title">${game.title}</h1>
                            <div class="game-subtitle">
                                <p class="game-tagline">${game.description}</p>
                            </div>
                        </div>
                    </div>
                </header>

                <div class="game-content">
                    <div class="game-main-content">
                        <section class="game-description">
                            <h2>About ${game.title}</h2>
                            <p>${game.description}</p>
                            
                            <div class="game-tags">
                                ${game.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                            </div>
                        </section>
                        
                        <section class="game-details">
                            <h2>Game Details</h2>
                            <div class="details-grid">
                                <div class="detail-item">
                                    <strong>Release Date:</strong>
                                    <span>${formattedDate}</span>
                                </div>
                                <div class="detail-item">
                                    <strong>Genre:</strong>
                                    <span class="genre-link" onclick="filterByGenre('${game.genre}')">${game.genre}</span>
                                </div>
                                <div class="detail-item">
                                    <strong>ESRB Rating:</strong>
                                    <span class="rating rating-${game.rating.toLowerCase().replace('+', 'plus')}">${game.rating}</span>
                                </div>
                            </div>
                        </section>
                    </div>

                    <aside class="game-sidebar">
                        <div class="info-box">
                            <h3>Game Information</h3>
                            <div class="info-list">
                                <div class="info-item">
                                    <strong>Developer:</strong>
                                    <span>${game.developer}</span>
                                </div>
                                <div class="info-item">
                                    <strong>Publisher:</strong>
                                    <span>${game.publisher}</span>
                                </div>
                                <div class="info-item">
                                    <strong>Platforms:</strong>
                                    <div class="platforms-list">
                                        ${game.platforms.map(platform => 
                                            `<span class="platform-tag">${platform}</span>`
                                        ).join('')}
                                    </div>
                                </div>
                                <div class="info-item">
                                    <strong>Categories:</strong>
                                    <div class="categories-list">
                                        ${game.categories.map(category => 
                                            `<span class="category-tag">${category}</span>`
                                        ).join('')}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="quick-actions">
                            <h3>Quick Actions</h3>
                            <button class="action-button" onclick="shareGame('${game.title}', '${gameUrl}')">
                                📤 Share Game
                            </button>
                            <button class="action-button" onclick="randomGame()">
                                🎮 Random Game
                            </button>
                            <button class="action-button" onclick="addToFavorites(${game.id})">
                                ⭐ Add to Favorites
                            </button>
                        </div>
                    </aside>
                </div>
            </article>
        `;

        // Scroll to top
        document.getElementById('gamePageContainer').scrollTop = 0;
    }

    /**
     * Update navigation state
     */
    updateNavigation() {
        // Update any active navigation indicators
        const navLinks = document.querySelectorAll('.main-nav a');
        navLinks.forEach(link => link.classList.remove('active'));
        
        if (this.currentRoute === 'home') {
            const homeLink = document.querySelector('.main-nav a[href="index.html"]');
            if (homeLink) homeLink.classList.add('active');
        }
    }

    /**
     * Navigate to a game by ID
     */
    navigateToGame(gameId) {
        const game = gamesDatabase.find(g => g.id === gameId);
        if (game) {
            this.navigate(this.getGameUrl(game));
        }
    }

    /**
     * Get current game if on game page
     */
    getCurrentGame() {
        if (this.currentRoute === 'game' && this.currentGameId) {
            return gamesDatabase.find(g => g.id === this.currentGameId);
        }
        return null;
    }
}

// Helper functions for game page interactions
function filterByGenre(genre) {
    gameRouter.navigate('');
    setTimeout(() => {
        document.getElementById('genreFilter').value = genre;
        if (window.applyFilters) {
            window.applyFilters();
        }
    }, 100);
}

function shareGame(title, url) {
    const fullUrl = `${window.location.origin}${window.location.pathname}${url}`;
    
    if (navigator.share) {
        navigator.share({
            title: `${title} - GamePedia`,
            text: `Check out ${title} on GamePedia`,
            url: fullUrl
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(fullUrl).then(() => {
            alert('Game URL copied to clipboard!');
        });
    }
}

function addToFavorites(gameId) {
    // Placeholder for favorites functionality
    alert('Favorites feature coming soon!');
}

// Initialize router when DOM is loaded
let gameRouter;
document.addEventListener('DOMContentLoaded', function() {
    gameRouter = new GameRouter();
});