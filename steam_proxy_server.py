#!/usr/bin/env python3
"""
GamePedia - Ultimate Gaming Platform
Military-grade secure Steam API proxy with comprehensive gaming features
"""

import asyncio
import json
import os
import sys
import time
import webbrowser
import threading
import secrets
import hashlib
import hmac
import base64
import sqlite3
import ipaddress
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from collections import defaultdict
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bcrypt

class SecurityManager:
    """Advanced security management with multiple layers of protection"""
    
    def __init__(self):
        self.setup_encryption()
        self.setup_database()
        self.setup_rate_limiting()
        self.setup_ip_security()
        self.setup_audit_logging()
        
    def setup_encryption(self):
        """Initialize military-grade encryption"""
        # Generate or load encryption key
        key_file = '.security_key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            # Generate new key
            password = secrets.token_bytes(32)
            salt = secrets.token_bytes(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            self.encryption_key = base64.urlsafe_b64encode(kdf.derive(password))
            
            # Save key securely
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            os.chmod(key_file, 0o600)  # Read-only for owner
            
        self.cipher = Fernet(self.encryption_key)
        
    def setup_database(self):
        """Initialize secure database"""
        self.db_path = 'gamepedia_secure.db'
        self.init_database()
        
    def init_database(self):
        """Create secure database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Users table (encrypted)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                steam_id_hash TEXT NOT NULL,
                api_key_encrypted BLOB NOT NULL,
                steam_id_encrypted BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                login_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Audit log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                action TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                details TEXT,
                success BOOLEAN DEFAULT 1
            )
        ''')
        
        # Rate limiting table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rate_limits (
                ip_address TEXT PRIMARY KEY,
                request_count INTEGER DEFAULT 0,
                window_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                blocked_until TIMESTAMP NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def setup_rate_limiting(self):
        """Configure rate limiting"""
        self.rate_limits = {
            'auth_attempts': {'max': 5, 'window': 300},  # 5 attempts per 5 minutes
            'api_calls': {'max': 100, 'window': 60},      # 100 calls per minute
            'session_creation': {'max': 10, 'window': 3600}  # 10 sessions per hour
        }
        
    def setup_ip_security(self):
        """Configure IP security"""
        self.blocked_ips = set()
        self.allowed_ips = set()  # If empty, allow all (except blocked)
        self.suspicious_ips = defaultdict(int)
        
    def setup_audit_logging(self):
        """Configure audit logging"""
        self.audit_enabled = True
        
    def encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode())
        
    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data).decode()
        
    def hash_steam_id(self, steam_id: str) -> str:
        """Create secure hash of Steam ID"""
        return hashlib.sha256(f"{steam_id}:{self.encryption_key}".encode()).hexdigest()
        
    def generate_secure_token(self) -> str:
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(64)  # 64 bytes = 512 bits
        
    def check_rate_limit(self, ip_address: str, action: str) -> bool:
        """Check if IP is rate limited"""
        if action not in self.rate_limits:
            return True
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        limit_config = self.rate_limits[action]
        window_start = datetime.now() - timedelta(seconds=limit_config['window'])
        
        cursor.execute('''
            SELECT request_count, window_start, blocked_until FROM rate_limits 
            WHERE ip_address = ?
        ''', (ip_address,))
        
        result = cursor.fetchone()
        
        if result:
            count, start, blocked_until = result
            
            # Check if currently blocked
            if blocked_until and datetime.fromisoformat(str(blocked_until)) > datetime.now():
                conn.close()
                return False
                
            # Check if within current window
            if datetime.fromisoformat(start) > window_start:
                if count >= limit_config['max']:
                    # Block IP for 1 hour
                    cursor.execute('''
                        UPDATE rate_limits 
                        SET blocked_until = ? 
                        WHERE ip_address = ?
                    ''', (datetime.now() + timedelta(hours=1), ip_address))
                    conn.commit()
                    conn.close()
                    return False
                    
                # Increment counter
                cursor.execute('''
                    UPDATE rate_limits 
                    SET request_count = request_count + 1 
                    WHERE ip_address = ?
                ''', (ip_address,))
            else:
                # Reset window
                cursor.execute('''
                    UPDATE rate_limits 
                    SET request_count = 1, window_start = ? 
                    WHERE ip_address = ?
                ''', (datetime.now(), ip_address))
        else:
            # First request from this IP
            cursor.execute('''
                INSERT INTO rate_limits (ip_address, request_count) 
                VALUES (?, 1)
            ''', (ip_address,))
            
        conn.commit()
        conn.close()
        return True
        
    def log_audit(self, user_id: str | None, action: str, ip_address: str, 
                  user_agent: str, details: str = None, success: bool = True):
        """Log security audit event"""
        if not self.audit_enabled:
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (user_id, action, ip_address, user_agent, details, success)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id or "UNKNOWN", action, ip_address, user_agent, details, success))
        
        conn.commit()
        conn.close()
        
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP is blocked"""
        return ip_address in self.blocked_ips
        
    def validate_session_security(self, token: str, ip_address: str, user_agent: str) -> bool:
        """Validate session with additional security checks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, expires_at, ip_address, user_agent, is_active 
            FROM sessions WHERE token = ?
        ''', (token,))
        
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
            
        user_id, expires_at, session_ip, session_ua, is_active = result
        
        # Check if session is active
        if not is_active:
            conn.close()
            return False
            
        # Check expiration
        if datetime.fromisoformat(expires_at) < datetime.now():
            # Deactivate expired session
            cursor.execute('''
                UPDATE sessions SET is_active = 0 WHERE token = ?
            ''', (token,))
            conn.commit()
            conn.close()
            return False
            
        # Optional: Check IP consistency (can be disabled for mobile users)
        # if session_ip != ip_address:
        #     return False
            
        # Update last used
        cursor.execute('''
            UPDATE sessions SET last_used = ? WHERE token = ?
        ''', (datetime.now(), token))
        
        conn.commit()
        conn.close()
        return True

class GameDataManager:
    """Comprehensive game data management system"""
    
    def __init__(self):
        self.setup_game_database()
        self.setup_external_apis()
        
    def setup_game_database(self):
        """Initialize comprehensive game database"""
        conn = sqlite3.connect('gamepedia_games.db')
        cursor = conn.cursor()
        
        # Games table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                steam_id INTEGER UNIQUE,
                name TEXT NOT NULL,
                short_description TEXT,
                detailed_description TEXT,
                header_image TEXT,
                website TEXT,
                developers TEXT,
                publishers TEXT,
                release_date TEXT,
                platforms TEXT,
                genres TEXT,
                categories TEXT,
                screenshots TEXT,
                movies TEXT,
                achievements_count INTEGER DEFAULT 0,
                metacritic_score INTEGER,
                price_current REAL,
                price_original REAL,
                price_discount_percent INTEGER,
                system_requirements TEXT,
                supported_languages TEXT,
                reviews_positive INTEGER DEFAULT 0,
                reviews_negative INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User game data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_games (
                user_id TEXT,
                game_id INTEGER,
                playtime_forever INTEGER DEFAULT 0,
                playtime_2weeks INTEGER DEFAULT 0,
                last_played TIMESTAMP,
                achievements_unlocked INTEGER DEFAULT 0,
                rating INTEGER,
                review TEXT,
                wishlist BOOLEAN DEFAULT 0,
                favorite BOOLEAN DEFAULT 0,
                custom_tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, game_id)
            )
        ''')
        
        # Game reviews
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                game_id INTEGER,
                rating INTEGER NOT NULL,
                review_text TEXT,
                helpful_count INTEGER DEFAULT 0,
                funny_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Game news
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                title TEXT NOT NULL,
                content TEXT,
                url TEXT,
                author TEXT,
                published_date TIMESTAMP,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Price history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                platform TEXT,
                price REAL,
                discount_percent INTEGER,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def setup_external_apis(self):
        """Configure external gaming APIs"""
        self.steam_api_base = "https://api.steampowered.com"
        self.steam_store_base = "https://store.steampowered.com/api"
        self.rawg_api_base = "https://api.rawg.io/api"
        self.igdb_api_base = "https://api.igdb.com/v4"
        
    async def get_game_details(self, app_id: int) -> dict:
        """Get comprehensive game details"""
        try:
            # Get Steam store data
            steam_response = await self.get_steam_store_data(app_id)
            
            # Get additional data from RAWG
            rawg_response = await self.get_rawg_data(steam_response.get('name', ''))
            
            # Combine and structure data
            game_data = self.combine_game_data(steam_response, rawg_response)
            
            # Save to database
            self.save_game_data(game_data)
            
            return game_data
            
        except Exception as e:
            print(f"Error getting game details for {app_id}: {e}")
            return {}
            
    async def get_steam_store_data(self, app_id: int) -> dict:
        """Get Steam store page data"""
        try:
            url = f"{self.steam_store_base}/appdetails"
            params = {'appids': app_id, 'format': 'json'}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if str(app_id) in data and data[str(app_id)]['success']:
                return data[str(app_id)]['data']
            return {}
            
        except Exception as e:
            print(f"Error getting Steam store data: {e}")
            return {}
            
    async def get_rawg_data(self, game_name: str) -> dict:
        """Get additional game data from RAWG"""
        try:
            url = f"{self.rawg_api_base}/games"
            params = {'search': game_name, 'key': 'your_rawg_api_key'}  # Add your RAWG API key
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('results'):
                return data['results'][0]
            return {}
            
        except Exception as e:
            print(f"Error getting RAWG data: {e}")
            return {}
            
    def combine_game_data(self, steam_data: dict, rawg_data: dict) -> dict:
        """Combine data from multiple sources"""
        combined = {
            'steam_id': steam_data.get('steam_appid'),
            'name': steam_data.get('name'),
            'short_description': steam_data.get('short_description'),
            'detailed_description': steam_data.get('detailed_description'),
            'header_image': steam_data.get('header_image'),
            'website': steam_data.get('website'),
            'developers': ', '.join(steam_data.get('developers', [])),
            'publishers': ', '.join(steam_data.get('publishers', [])),
            'release_date': steam_data.get('release_date', {}).get('date'),
            'platforms': json.dumps(steam_data.get('platforms', {})),
            'genres': ', '.join([g.get('description', '') for g in steam_data.get('genres', [])]),
            'categories': ', '.join([c.get('description', '') for c in steam_data.get('categories', [])]),
            'screenshots': json.dumps([s.get('path_full') for s in steam_data.get('screenshots', [])]),
            'movies': json.dumps([m.get('mp4', {}).get('max') for m in steam_data.get('movies', [])]),
            'achievements_count': steam_data.get('achievements', {}).get('total', 0),
            'metacritic_score': steam_data.get('metacritic', {}).get('score'),
            'price_current': steam_data.get('price_overview', {}).get('final', 0) / 100 if steam_data.get('price_overview') else None,
            'price_original': steam_data.get('price_overview', {}).get('initial', 0) / 100 if steam_data.get('price_overview') else None,
            'price_discount_percent': steam_data.get('price_overview', {}).get('discount_percent'),
            'system_requirements': json.dumps(steam_data.get('pc_requirements', {})),
            'supported_languages': steam_data.get('supported_languages'),
            
            # Add RAWG data
            'rawg_rating': rawg_data.get('rating'),
            'rawg_ratings_count': rawg_data.get('ratings_count'),
            'rawg_suggestions_count': rawg_data.get('suggestions_count'),
            'rawg_tags': ', '.join([tag.get('name', '') for tag in rawg_data.get('tags', [])]),
        }
        
        return combined
        
    def save_game_data(self, game_data: dict):
        """Save game data to database"""
        conn = sqlite3.connect('gamepedia_games.db')
        cursor = conn.cursor()
        
        # Insert or update game data
        cursor.execute('''
            INSERT OR REPLACE INTO games (
                steam_id, name, short_description, detailed_description,
                header_image, website, developers, publishers, release_date,
                platforms, genres, categories, screenshots, movies,
                achievements_count, metacritic_score, price_current,
                price_original, price_discount_percent, system_requirements,
                supported_languages, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            game_data.get('steam_id'),
            game_data.get('name'),
            game_data.get('short_description'),
            game_data.get('detailed_description'),
            game_data.get('header_image'),
            game_data.get('website'),
            game_data.get('developers'),
            game_data.get('publishers'),
            game_data.get('release_date'),
            game_data.get('platforms'),
            game_data.get('genres'),
            game_data.get('categories'),
            game_data.get('screenshots'),
            game_data.get('movies'),
            game_data.get('achievements_count'),
            game_data.get('metacritic_score'),
            game_data.get('price_current'),
            game_data.get('price_original'),
            game_data.get('price_discount_percent'),
            game_data.get('system_requirements'),
            game_data.get('supported_languages'),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        
    def search_games(self, query: str, filters: dict = None) -> list:
        """Advanced game search with filters"""
        conn = sqlite3.connect('gamepedia_games.db')
        cursor = conn.cursor()
        
        sql = '''
            SELECT * FROM games 
            WHERE name LIKE ? OR short_description LIKE ? OR genres LIKE ?
        '''
        params = [f'%{query}%', f'%{query}%', f'%{query}%']
        
        if filters:
            if filters.get('genre'):
                sql += ' AND genres LIKE ?'
                params.append(f'%{filters["genre"]}%')
                
            if filters.get('min_price') is not None:
                sql += ' AND price_current >= ?'
                params.append(filters['min_price'])
                
            if filters.get('max_price') is not None:
                sql += ' AND price_current <= ?'
                params.append(filters['max_price'])
                
            if filters.get('min_score') is not None:
                sql += ' AND metacritic_score >= ?'
                params.append(filters['min_score'])
                
        sql += ' ORDER BY name LIMIT 50'
        
        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        conn.close()
        return results

class EnhancedSteamAPIProxy:
    """Enhanced Steam API proxy with security and comprehensive features"""
    
    def __init__(self):
        self.security_manager = SecurityManager()
        self.game_data_manager = GameDataManager()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GamePedia-Ultimate/3.0-Secure'
        })
        
    async def authenticate_user(self, api_key: str, steam_id: str, 
                              ip_address: str, user_agent: str) -> dict:
        """Enhanced user authentication with security"""
        try:
            # Check rate limiting
            if not self.security_manager.check_rate_limit(ip_address, 'auth_attempts'):
                self.security_manager.log_audit(
                    None, 'AUTH_RATE_LIMITED', ip_address, user_agent, 
                    f'Rate limit exceeded', False
                )
                return {'error': 'Too many authentication attempts. Please try again later.'}
            
            # Check if IP is blocked
            if self.security_manager.is_ip_blocked(ip_address):
                self.security_manager.log_audit(
                    None, 'AUTH_BLOCKED_IP', ip_address, user_agent, 
                    f'Blocked IP attempt', False
                )
                return {'error': 'Access denied.'}
            
            # Validate credentials with Steam API
            test_response = await self.get_player_summaries(api_key, steam_id)
            
            if 'error' in test_response:
                self.security_manager.log_audit(
                    None, 'AUTH_FAILED', ip_address, user_agent, 
                    f'Invalid credentials: {test_response["error"]}', False
                )
                return {'error': test_response['error']}
            
            # Create secure user record
            user_id = secrets.token_urlsafe(16)
            steam_id_hash = self.security_manager.hash_steam_id(steam_id)
            
            # Encrypt and store credentials
            encrypted_api_key = self.security_manager.encrypt_data(api_key)
            encrypted_steam_id = self.security_manager.encrypt_data(steam_id)
            
            conn = sqlite3.connect(self.security_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO users (
                    id, steam_id_hash, api_key_encrypted, steam_id_encrypted, 
                    last_login, login_count
                ) VALUES (?, ?, ?, ?, ?, COALESCE((SELECT login_count FROM users WHERE steam_id_hash = ?), 0) + 1)
            ''', (user_id, steam_id_hash, encrypted_api_key, encrypted_steam_id, 
                  datetime.now(), steam_id_hash))
            
            # Create secure session
            session_token = self.security_manager.generate_secure_token()
            expires_at = datetime.now() + timedelta(hours=24)
            
            cursor.execute('''
                INSERT INTO sessions (
                    token, user_id, expires_at, ip_address, user_agent
                ) VALUES (?, ?, ?, ?, ?)
            ''', (session_token, user_id, expires_at, ip_address, user_agent))
            
            conn.commit()
            conn.close()
            
            # Log successful authentication
            self.security_manager.log_audit(
                user_id, 'AUTH_SUCCESS', ip_address, user_agent, 
                f'Steam ID: {steam_id}', True
            )
            
            return {
                'success': True,
                'session_token': session_token,
                'expires_at': expires_at.isoformat(),
                'message': 'Authentication successful'
            }
            
        except Exception as e:
            self.security_manager.log_audit(
                None, 'AUTH_ERROR', ip_address, user_agent, 
                f'Exception: {str(e)}', False
            )
            return {'error': f'Authentication failed: {str(e)}'}
    
    async def get_comprehensive_user_data(self, session_token: str, 
                                        ip_address: str, user_agent: str) -> dict:
        """Get comprehensive user data with enhanced security"""
        try:
            # Validate session with security checks
            if not self.security_manager.validate_session_security(
                session_token, ip_address, user_agent
            ):
                return {"error": "Invalid or expired session"}
            
            # Check rate limiting
            if not self.security_manager.check_rate_limit(ip_address, 'api_calls'):
                return {"error": "Rate limit exceeded"}
            
            # Get user credentials
            conn = sqlite3.connect(self.security_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT u.id, u.api_key_encrypted, u.steam_id_encrypted 
                FROM users u
                JOIN sessions s ON u.id = s.user_id
                WHERE s.token = ? AND s.is_active = 1
            ''', (session_token,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return {"error": "Session not found"}
            
            user_id, encrypted_api_key, encrypted_steam_id = result
            
            # Decrypt credentials
            api_key = self.security_manager.decrypt_data(encrypted_api_key)
            steam_id = self.security_manager.decrypt_data(encrypted_steam_id)
            
            # Get Steam data
            steam_data = await self.get_enhanced_steam_data(api_key, steam_id)
            
            # Get additional game data
            enhanced_data = await self.enhance_with_game_data(steam_data, user_id)
            
            # Log successful data retrieval
            self.security_manager.log_audit(
                user_id, 'DATA_RETRIEVED', ip_address, user_agent, 
                'Comprehensive user data', True
            )
            
            return enhanced_data
            
        except Exception as e:
            self.security_manager.log_audit(
                None, 'DATA_ERROR', ip_address, user_agent, 
                f'Exception: {str(e)}', False
            )
            return {"error": f"Failed to get user data: {str(e)}"}
    
    async def get_enhanced_steam_data(self, api_key: str, steam_id: str) -> dict:
        """Get enhanced Steam data with additional features"""
        try:
            # Get basic Steam data
            player_data = await self.get_player_summaries(api_key, steam_id)
            games_data = await self.get_owned_games(api_key, steam_id)
            recent_data = await self.get_recently_played_games(api_key, steam_id, 10)
            
            # Get achievements for top games
            achievements_data = {}
            if games_data.get('response', {}).get('games'):
                top_games = sorted(
                    games_data['response']['games'], 
                    key=lambda x: x.get('playtime_forever', 0), 
                    reverse=True
                )[:3]
                
                for game in top_games:
                    app_id = game.get('appid')
                    if app_id:
                        achievements = await self.get_player_achievements(api_key, steam_id, app_id)
                        if achievements and 'error' not in achievements:
                            achievements_data[app_id] = achievements
            
            return {
                'player': player_data,
                'games': games_data,
                'recent': recent_data,
                'achievements': achievements_data
            }
            
        except Exception as e:
            return {"error": f"Failed to get Steam data: {str(e)}"}
    
    async def enhance_with_game_data(self, steam_data: dict, user_id: str) -> dict:
        """Enhance Steam data with comprehensive game information"""
        try:
            result = {
                'player': None,
                'stats': None,
                'recentGames': None,
                'topGames': None,
                'achievements': None,
                'recommendations': None,
                'priceAlerts': None
            }
            
            # Process player data
            if steam_data.get('player', {}).get('response', {}).get('players'):
                result['player'] = steam_data['player']['response']['players'][0]
            
            # Process games data
            if steam_data.get('games', {}).get('response', {}).get('games'):
                games = steam_data['games']['response']['games']
                
                # Basic stats
                total_games = len(games)
                total_playtime = sum(game.get('playtime_forever', 0) for game in games)
                most_played = max(games, key=lambda x: x.get('playtime_forever', 0)) if games else None
                
                result['stats'] = {
                    'total_games': total_games,
                    'total_playtime': f"{total_playtime // 60:,} hours",
                    'most_played': most_played.get('name', 'None') if most_played else 'None',
                    'average_playtime': f"{(total_playtime // total_games) // 60:.1f} hours" if total_games > 0 else "0 hours",
                    'games_never_played': len([g for g in games if g.get('playtime_forever', 0) == 0]),
                    'games_played_recently': len([g for g in games if g.get('playtime_2weeks', 0) > 0])
                }
                
                # Top games
                top_games = sorted(games, key=lambda x: x.get('playtime_forever', 0), reverse=True)[:10]
                result['topGames'] = await self.process_game_list(top_games, user_id)
            
            # Process recent games
            if steam_data.get('recent', {}).get('response', {}).get('games'):
                recent_games = steam_data['recent']['response']['games']
                result['recentGames'] = await self.process_game_list(recent_games, user_id)
            
            # Process achievements
            if steam_data.get('achievements'):
                result['achievements'] = self.process_achievements(steam_data['achievements'])
            
            # Generate recommendations
            result['recommendations'] = await self.generate_recommendations(user_id, games if 'games' in locals() else [])
            
            return result
            
        except Exception as e:
            return {"error": f"Failed to enhance data: {str(e)}"}
    
    async def process_game_list(self, games: list, user_id: str) -> list:
        """Process and enhance game list with additional data"""
        processed_games = []
        
        for game in games:
            app_id = game.get('appid')
            if app_id:
                # Get detailed game data
                game_details = await self.game_data_manager.get_game_details(app_id)
                
                enhanced_game = {
                    'appid': app_id,
                    'name': game.get('name', 'Unknown'),
                    'playtime_forever': game.get('playtime_forever', 0),
                    'playtime_2weeks': game.get('playtime_2weeks', 0),
                    'img_icon_url': f"https://media.steampowered.com/steamcommunity/public/images/apps/{app_id}/{game.get('img_icon_url', '')}.jpg" if game.get('img_icon_url') else None,
                    'img_logo_url': f"https://media.steampowered.com/steamcommunity/public/images/apps/{app_id}/{game.get('img_logo_url', '')}.jpg" if game.get('img_logo_url') else None,
                    
                    # Enhanced data
                    'header_image': game_details.get('header_image'),
                    'short_description': game_details.get('short_description'),
                    'genres': game_details.get('genres'),
                    'developers': game_details.get('developers'),
                    'publishers': game_details.get('publishers'),
                    'release_date': game_details.get('release_date'),
                    'metacritic_score': game_details.get('metacritic_score'),
                    'price_current': game_details.get('price_current'),
                    'price_original': game_details.get('price_original'),
                    'price_discount_percent': game_details.get('price_discount_percent'),
                    'achievements_count': game_details.get('achievements_count'),
                    'screenshots': json.loads(game_details.get('screenshots', '[]')) if game_details.get('screenshots') else [],
                    'system_requirements': json.loads(game_details.get('system_requirements', '{}')) if game_details.get('system_requirements') else {},
                }
                
                processed_games.append(enhanced_game)
        
        return processed_games
    
    def process_achievements(self, achievements_data: dict) -> dict:
        """Process achievements data"""
        processed = {}
        
        for app_id, data in achievements_data.items():
            if 'playerstats' in data:
                achievements = data['playerstats'].get('achievements', [])
                total = len(achievements)
                unlocked = sum(1 for ach in achievements if ach.get('achieved', 0) == 1)
                
                processed[app_id] = {
                    'total': total,
                    'unlocked': unlocked,
                    'percentage': (unlocked / total * 100) if total > 0 else 0,
                    'recent_unlocks': [
                        ach for ach in achievements 
                        if ach.get('achieved', 0) == 1 and ach.get('unlocktime', 0) > 0
                    ][-5:]  # Last 5 unlocked
                }
        
        return processed
    
    async def generate_recommendations(self, user_id: str, owned_games: list) -> list:
        """Generate game recommendations based on user data"""
        try:
            # Get user's favorite genres
            genres = []
            for game in owned_games:
                if game.get('playtime_forever', 0) > 60:  # More than 1 hour
                    # Get game genres (would need to implement game data lookup)
                    pass
            
            # For now, return popular games (would implement ML recommendations)
            recommendations = [
                {
                    'name': 'Baldur\'s Gate 3',
                    'reason': 'Highly rated RPG',
                    'score': 95,
                    'price': 59.99
                },
                {
                    'name': 'Cyberpunk 2077',
                    'reason': 'Action RPG with great reviews',
                    'score': 86,
                    'price': 29.99
                },
                {
                    'name': 'The Witcher 3: Wild Hunt',
                    'reason': 'Based on your RPG preferences',
                    'score': 93,
                    'price': 39.99
                }
            ]
            
            return recommendations
            
        except Exception as e:
            return []
    
    # Steam API methods (enhanced versions)
    async def get_player_summaries(self, api_key: str, steam_id: str) -> dict:
        """Get player profile information"""
        try:
            url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
            params = {
                'key': api_key,
                'steamids': steam_id,
                'format': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {"error": f"Failed to get player summaries: {str(e)}"}
    
    async def get_owned_games(self, api_key: str, steam_id: str) -> dict:
        """Get owned games with enhanced data"""
        try:
            url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
            params = {
                'key': api_key,
                'steamid': steam_id,
                'format': 'json',
                'include_appinfo': 1,
                'include_played_free_games': 1,
                'include_free_sub': 1
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {"error": f"Failed to get owned games: {str(e)}"}
    
    async def get_recently_played_games(self, api_key: str, steam_id: str, count: int = 10) -> dict:
        """Get recently played games"""
        try:
            url = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"
            params = {
                'key': api_key,
                'steamid': steam_id,
                'format': 'json',
                'count': count
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {"error": f"Failed to get recent games: {str(e)}"}
    
    async def get_player_achievements(self, api_key: str, steam_id: str, app_id: int) -> dict:
        """Get player achievements for a specific game"""
        try:
            url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
            params = {
                'key': api_key,
                'steamid': steam_id,
                'appid': app_id,
                'format': 'json'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {"error": f"Failed to get achievements: {str(e)}"}

class GamePediaServer(SimpleHTTPRequestHandler):
    """Enhanced HTTP server with secure Steam API proxy"""
    
    def __init__(self, *args, steam_proxy=None, **kwargs):
        self.steam_proxy = steam_proxy
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # Handle legacy Steam API proxy requests (deprecated)
        if parsed_path.path.startswith('/api/steam/'):
            self.send_json_response({"error": "Please use the new secure authentication system"}, 400)
        else:
            # Handle static files
            self.handle_static_files()
    
    def do_POST(self):
        """Handle POST requests for secure Steam API"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/steam/authenticate':
            asyncio.run(self.handle_authentication())
        elif parsed_path.path == '/api/steam/validate':
            self.handle_session_validation()
        elif parsed_path.path == '/api/steam/user-data':
            asyncio.run(self.handle_user_data())
        else:
            self.send_error(404)
    
    async def handle_authentication(self):
        """Handle user authentication"""
        try:
            if not self.steam_proxy:
                self.send_json_response({"error": "Steam proxy not initialized"}, 500)
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            api_key = data.get('api_key')
            steam_id = data.get('steam_id')
            
            if not api_key or not steam_id:
                self.send_json_response({"error": "API key and Steam ID are required"}, 400)
                return
            
            # Authenticate with Steam API
            result = await self.steam_proxy.authenticate_user(api_key, steam_id)
            
            if result.get('success'):
                self.send_json_response(result)
            else:
                self.send_json_response(result, 401)
                
        except Exception as e:
            self.send_json_response({"error": f"Authentication error: {str(e)}"}, 500)
    
    def handle_session_validation(self):
        """Handle session token validation"""
        try:
            if not self.steam_proxy:
                self.send_json_response({"error": "Steam proxy not initialized"}, 500)
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            session_token = data.get('session_token')
            
            if not session_token:
                self.send_json_response({"error": "Session token required"}, 400)
                return
            
            is_valid = self.steam_proxy.validate_session_token(session_token)
            
            if is_valid:
                self.send_json_response({"valid": True})
            else:
                self.send_json_response({"valid": False}, 401)
                
        except Exception as e:
            self.send_json_response({"error": f"Validation error: {str(e)}"}, 500)
    
    async def handle_user_data(self):
        """Handle user data retrieval"""
        try:
            if not self.steam_proxy:
                self.send_json_response({"error": "Steam proxy not initialized"}, 500)
                return
                
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            session_token = data.get('session_token')
            
            if not session_token:
                self.send_json_response({"error": "Session token required"}, 400)
                return
            
            # Get comprehensive user data
            user_data = await self.steam_proxy.get_comprehensive_user_data(session_token)
            
            if 'error' in user_data:
                self.send_json_response(user_data, 401)
            else:
                self.send_json_response(user_data)
                
        except Exception as e:
            self.send_json_response({"error": f"Data retrieval error: {str(e)}"}, 500)
    
    def handle_static_files(self):
        """Handle static file requests"""
        # Add CORS headers for all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().do_GET()
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response with CORS headers"""
        response = json.dumps(data, indent=2)
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def get_free_port():
    """Find a free port to use for the server"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def create_server_handler(steam_proxy):
    """Create a server handler with Steam proxy"""
    def handler(*args, **kwargs):
        return GamePediaServer(*args, steam_proxy=steam_proxy, **kwargs)
    return handler

def main():
    """Main server function"""
    # Initialize Steam API proxy
    steam_proxy = EnhancedSteamAPIProxy()
    
    # Change to gamepedia directory
    gamepedia_dir = Path(__file__).parent / 'gamepedia'
    if not gamepedia_dir.exists():
        print("❌ Error: gamepedia directory not found!")
        print("Please make sure you're running this script from the project root directory.")
        return False
    
    os.chdir(gamepedia_dir)
    
    # Find free port and start server
    port = get_free_port()
    server_handler = create_server_handler(steam_proxy)
    
    try:
        with HTTPServer(("", port), server_handler) as httpd:
            url = f"http://localhost:{port}"
            
            print("🎮 GamePedia + Secure Steam API Server v2.0")
            print("=" * 55)
            print(f"🚀 Server URL: {url}")
            print(f"🔧 Port: {port}")
            print(f"📁 Serving from: {gamepedia_dir}")
            print("🔗 Steam API Proxy: Active (Secure)")
            print("\n" + "🎯 SECURITY FEATURES:")
            print("✅ Session-based Authentication")
            print("✅ Encrypted Credential Storage")
            print("✅ No Client-side API Key Exposure")
            print("✅ Automatic Session Expiration")
            print("✅ Secure Token Generation")
            print("\n" + "🔧 STEAM INTEGRATION:")
            print("✅ Real-time Steam Data")
            print("✅ Player Profile & Statistics")
            print("✅ Recently Played Games")
            print("✅ Secure API Proxy")
            print("✅ Auto-refresh Every 5 Minutes")
            print("\n" + "⚙️ SETUP:")
            print("1. Get Steam API Key: https://steamcommunity.com/dev/apikey")
            print("2. Find Steam ID: https://steamidfinder.com/")
            print("3. Configure in the Steam widget (one-time setup)")
            print("4. Your credentials are stored securely server-side")
            print("\n" + "=" * 55)
            print(f"🌐 Opening browser to {url}")
            print("❌ Press Ctrl+C to stop the server")
            
            # Open browser after delay
            def open_browser():
                time.sleep(1.5)
                webbrowser.open(url)
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

if __name__ == "__main__":
    if not main():
        sys.exit(1)