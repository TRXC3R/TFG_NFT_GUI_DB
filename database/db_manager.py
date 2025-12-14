"""
database/db.py
Funciones para interactuar con SQLite de forma segura
"""

import sqlite3
import bcrypt
from datetime import datetime
from pathlib import Path

DB_PATH = Path("./database/users_database.db")

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        """Obtiene conexión a la BD"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Acceso a columnas por nombre
        return conn
    
    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """)
        conn.commit()
        conn.close()
    
    # ==================== USUARIOS ====================
    def create_user(self, username: str, password: str, email: str = None) -> bool:
        """Crea un nuevo usuario con contraseña hasheada"""
        try:
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            print(f"El usuario {username} ya existe")
            return False  # Usuario ya existe
    
    def verify_user(self, username: str, password: str) -> dict:
        """Verifica credenciales y devuelve datos del usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            return {"id": user['id'], "username": user['username']}
        return None
    
    def get_user(self, user_id: int) -> dict:
        """Obtiene datos de un usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    # ==================== IMÁGENES ====================
    def save_image(self, user_id: int, prompt: str, style: str, seed: int, 
                   file_path: str, metadata: dict = None) -> int:
        """Guarda registro de imagen generada"""
        import json
        conn = self.get_connection()
        cursor = conn.cursor()
        metadata_json = json.dumps(metadata) if metadata else None
        cursor.execute(
            """INSERT INTO images 
               (user_id, prompt, style, seed, file_path, metadata)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, prompt, style, seed, file_path, metadata_json)
        )
        conn.commit()
        image_id = cursor.lastrowid
        conn.close()
        return image_id
    
    def get_user_images(self, user_id: int, limit: int = 50) -> list:
        """Obtiene todas las imágenes de un usuario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM images WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        )
        images = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return images
    
    def get_image(self, image_id: int) -> dict:
        """Obtiene datos de una imagen específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images WHERE id = ?", (image_id,))
        image = cursor.fetchone()
        conn.close()
        return dict(image) if image else None
    
    def get_all_images(self, limit: int = 100) -> list:
        """Obtiene todas las imágenes de la plataforma (pública)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT i.*, u.username FROM images i
               JOIN users u ON i.user_id = u.id
               WHERE i.is_minted = 1
               ORDER BY i.created_at DESC LIMIT ?""",
            (limit,)
        )
        images = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return images
    
    # ==================== NFT MINTING ====================
    def mark_as_minted(self, image_id: int, ipfs_hash: str, nft_address: str, 
                       token_id: int) -> bool:
        """Marca una imagen como NFT minteado"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE images 
               SET is_minted = 1, ipfs_hash = ?, nft_contract_address = ?, nft_token_id = ?
               WHERE id = ?""",
            (ipfs_hash, nft_address, token_id, image_id)
        )
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    
    # ==================== MARKETPLACE ====================
    def create_listing(self, image_id: int, seller_id: int, price: float) -> int:
        """Crea un anuncio de venta"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO listings (image_id, seller_id, price) VALUES (?, ?, ?)",
            (image_id, seller_id, price)
        )
        conn.commit()
        listing_id = cursor.lastrowid
        conn.close()
        return listing_id
    
    def get_active_listings(self, limit: int = 50) -> list:
        """Obtiene listados activos del marketplace"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT l.*, i.file_path, i.prompt, u.username
               FROM listings l
               JOIN images i ON l.image_id = i.id
               JOIN users u ON l.seller_id = u.id
               WHERE l.is_active = 1
               ORDER BY l.created_at DESC LIMIT ?""",
            (limit,)
        )
        listings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return listings

# Instancia global (singleton)
db = DatabaseManager()
