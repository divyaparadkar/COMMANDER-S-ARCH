import sqlite3
import hashlib
import os
import json
import re
from typing import Dict, List, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ssb_prep.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    """Hash password using PBKDF2 with a secure random salt."""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + '$' + key.hex()

def verify_password(stored_password_hash: str, password: str) -> bool:
    """Verify password against stored salt and key."""
    try:
        salt_hex, key_hex = stored_password_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        key = bytes.fromhex(key_hex)
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return key == new_key
    except Exception:
        return False

def init_db():
    """Create tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            api_key TEXT DEFAULT '',
            piq_json TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create attempt_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attempt_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            test_type TEXT NOT NULL,
            text TEXT NOT NULL,
            context TEXT DEFAULT '',
            analysis_json TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Create sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            expiry REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()

def register_user(username: str, password: str, email: Optional[str] = None) -> Tuple[bool, str]:
    """Register a new user in the database with validation."""
    username = username.strip()
    if not username or not password:
        return False, "Username and password cannot be empty."
        
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
        
    if not re.match(r"^[a-zA-Z0-9_-]+$", username):
        return False, "Username can only contain alphanumeric characters, underscores, and hyphens."
        
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
        
    if email:
        email = email.strip()
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            return False, "Invalid email format."
            
    password_hash = hash_password(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
            (username, password_hash, email)
        )
        conn.commit()
        return True, "Registration successful."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Verify credentials and return user details if authenticated."""
    username = username.strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and verify_password(user['password_hash'], password):
            # Parse PIQ JSON if it exists
            piq_data = {}
            if user['piq_json']:
                try:
                    piq_data = json.loads(user['piq_json'])
                except Exception:
                    pass
            return {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "api_key": user['api_key'],
                "piq_data": piq_data
            }
        return None
    finally:
        conn.close()

def update_user_api_key(user_id: int, api_key: str):
    """Update user API key."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET api_key = ? WHERE id = ?", (api_key, user_id))
        conn.commit()
    finally:
        conn.close()

def update_user_piq(user_id: int, piq_data: Dict):
    """Update user PIQ data as a serialized JSON string."""
    piq_json = json.dumps(piq_data)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET piq_json = ? WHERE id = ?", (piq_json, user_id))
        conn.commit()
    finally:
        conn.close()

def save_user_attempt(user_id: int, timestamp: str, test_type: str, text: str, context: str, analysis: Dict):
    """Save attempt history for a user."""
    analysis_json = json.dumps(analysis)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO attempt_history (user_id, timestamp, test_type, text, context, analysis_json) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, timestamp, test_type, text, context, analysis_json)
        )
        conn.commit()
    finally:
        conn.close()

def get_user_history(user_id: int) -> List[Dict]:
    """Retrieve all attempt history for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT timestamp, test_type, text, context, analysis_json FROM attempt_history WHERE user_id = ? ORDER BY timestamp ASC",
            (user_id,)
        )
        rows = cursor.fetchall()
        history = []
        for row in rows:
            try:
                analysis = json.loads(row['analysis_json'])
            except Exception:
                analysis = {}
            history.append({
                "timestamp": row['timestamp'],
                "test_type": row['test_type'],
                "text": row['text'],
                "context": row['context'],
                "analysis": analysis
            })
        return history
    finally:
        conn.close()

def update_user_password(user_id: int, new_password: str) -> Tuple[bool, str]:
    """Change a user's password securely."""
    if not new_password:
        return False, "Password cannot be empty."
    password_hash = hash_password(new_password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))
        conn.commit()
        return True, "Password changed successfully."
    except Exception as e:
        return False, f"Database error: {str(e)}"
    finally:
        conn.close()

def create_session(user_id: int) -> str:
    """Create a new session token for the user, valid for 30 days."""
    import uuid
    import time
    token = str(uuid.uuid4())
    expiry = time.time() + 30 * 24 * 60 * 60  # 30 days
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO sessions (token, user_id, expiry) VALUES (?, ?, ?)",
            (token, user_id, expiry)
        )
        conn.commit()
        return token
    finally:
        conn.close()

def verify_session(token: str) -> Optional[int]:
    """Verify session token and return user_id if valid."""
    import time
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT user_id, expiry FROM sessions WHERE token = ?",
            (token,)
        )
        row = cursor.fetchone()
        if row:
            if row['expiry'] > time.time():
                return row['user_id']
            else:
                # Expired session, clean up
                cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
                conn.commit()
        return None
    finally:
        conn.close()

def delete_session(token: str):
    """Delete a session token."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
    finally:
        conn.close()
