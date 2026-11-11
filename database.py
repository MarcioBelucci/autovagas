import sqlite3

DB_NAME = "vagas.db"


def _conexao():
    return sqlite3.connect(DB_NAME)


def inicializar_banco():
    with _conexao() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vagas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL, empresa TEXT, local TEXT,
                link TEXT UNIQUE NOT NULL, plataforma TEXT, descricao TEXT,
                score INTEGER, data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pendente', erro_envio TEXT
            );
        """)
        colunas = {linha[1] for linha in conn.execute("PRAGMA table_info(vagas)")}
        if "erro_envio" not in colunas:
            conn.execute("ALTER TABLE vagas ADD COLUMN erro_envio TEXT")


def salvar_vaga(vaga):
    """Registra uma vaga pendente. Retorna False se o link já era conhecido."""
    try:
        with _conexao() as conn:
            conn.execute("""
                INSERT INTO vagas
                    (titulo, empresa, local, link, plataforma, descricao, score, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pendente')
            """, (
                vaga.get("titulo"), vaga.get("empresa"), vaga.get("local"),
                vaga.get("link"), vaga.get("plataforma"), vaga.get("descricao"),
                vaga.get("score", 0),
            ))
        return True
    except sqlite3.IntegrityError:
        return False


def status_vaga(link):
    with _conexao() as conn:
        linha = conn.execute("SELECT status FROM vagas WHERE link = ?", (link,)).fetchone()
    return linha[0] if linha else None


def atualizar_status(link, status, erro=None):
    with _conexao() as conn:
        conn.execute(
            "UPDATE vagas SET status = ?, erro_envio = ? WHERE link = ?",
            (status, erro, link),
        )
