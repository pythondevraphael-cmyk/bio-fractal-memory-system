import sqlite3
import logging


logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def connect_db(db_path="data/bio_fractal.db"):
    """Conecta ao SQLite garantindo que a pasta data exista."""
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Erro ao conectar ao banco: {e}")
        return None

def create_structure(conn):
    """Cria a tabela synapses com logica de autorreferencia."""
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
        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Erro na criacao da tabela: {e}")

def seed_root(conn):
    """Garante o neuronio raiz (Intelligence)."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM synapses WHERE parent_id IS NULL")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO synapses (content, parent_id, depth) VALUES ('Inteligencia Artificial', NULL, 0)")
        conn.commit()
        logging.info("Neuronio raiz plantado.")