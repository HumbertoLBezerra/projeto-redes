import sqlite3
from datetime import datetime
from pathlib import Path

ARQUIVO_DB = Path("captura.db")


def conectar():
    conn = sqlite3.connect(ARQUIVO_DB, check_same_thread=False)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pacotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            momento REAL NOT NULL,
            origem TEXT,
            destino TEXT,
            protocolo TEXT,
            tamanho INTEGER,
            resumo TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_origem ON pacotes(origem)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_destino ON pacotes(destino)")
    conn.commit()
    return conn


def gravar_lote(conn, pacotes):
    """Insere vários pacotes (dicionários) de uma vez, em uma transação."""
    linhas = [
        (p["momento"], p["origem"], p["destino"],
         p["protocolo"], p["tamanho"], p["resumo"])
        for p in pacotes
    ]
    conn.executemany(
        "INSERT INTO pacotes (momento, origem, destino, protocolo, tamanho, resumo) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        linhas,
    )
    conn.commit()


def exportar_log(conn, arquivo_saida, origem=None, protocolo=None):
    """Gera um arquivo de log a partir do banco, com filtros opcionais."""
    sql = "SELECT momento, resumo FROM pacotes WHERE 1=1"
    params = []
    if origem:
        sql += " AND origem = ?"
        params.append(origem)
    if protocolo:
        sql += " AND protocolo = ?"
        params.append(protocolo)
    sql += " ORDER BY momento"

    Path(arquivo_saida).parent.mkdir(parents=True, exist_ok=True)
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        for momento, resumo in conn.execute(sql, params):
            hora = datetime.fromtimestamp(momento).strftime("%H:%M:%S.%f")
            f.write(f"{hora} {resumo}\n")
    return arquivo_saida