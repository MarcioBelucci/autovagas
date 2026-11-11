import sqlite3
from datetime import datetime

DB_NAME = "vagas.db"

def inicializar_banco():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            empresa TEXT,
            local TEXT,
            link TEXT UNIQUE NOT NULL,
            plataforma TEXT,
            descricao TEXT,
            score INTEGER,
            data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'novo'
        );
    """)
    conn.commit()
    conn.close()

def salvar_vaga(vaga):
    """
    Salva a vaga no banco. Se o link já existir (UNIQUE), retorna False.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vagas (titulo, empresa, local, link, plataforma, descricao, score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            vaga.get("titulo"),
            vaga.get("empresa"),
            vaga.get("local"),
            vaga.get("link"),
            vaga.get("plataforma"),
            vaga.get("descricao"),
            vaga.get("score", 0)
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Vaga já cadastrada anteriormente
        return False
    finally:
        conn.close()