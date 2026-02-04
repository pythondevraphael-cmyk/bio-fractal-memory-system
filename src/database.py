import sqlite3
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def connect_db(db_path="data/bio_fractal.db"):
    # Garante que a pasta data exista
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar ao banco: {e}")
        return None

def create_structure(conn):
    query = """
    CREATE TABLE IF NOT EXISTS synapses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        parent_id INTEGER,
        depth INTEGER DEFAULT 0,
        FOREIGN KEY (parent_id) REFERENCES synapses (id)
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit() # Importante: Salva a estrutura
    except Exception as e:
        logging.error(f"Erro ao criar tabela: {e}")