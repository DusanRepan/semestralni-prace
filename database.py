import sqlite3

DB_NAME = "data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabulka druhů zvěře
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS druhy_zvere (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazev TEXT UNIQUE NOT NULL
        )
    """)

    # Tabulka záznamů
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS zaznamy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            druh_id INTEGER,
            vek INTEGER,
            pohlavi TEXT,
            datum_pozorovani TEXT,
            datum_uloveni TEXT,
            FOREIGN KEY (druh_id) REFERENCES druhy_zvere(id)
        )
    """)

    conn.commit()
    conn.close()

def init_druhy():
    druhy = [
        "Zajíc polní",
        "Králík divoký",
        "Srnec obecný",
        "Jelen evropský",
        "Prase divoké",
        "Liška obecná",
        "Jezevec lesní"
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for druh in druhy:
        cursor.execute(
            "INSERT OR IGNORE INTO druhy_zvere (nazev) VALUES (?)",
            (druh,)
        )

    conn.commit()
    conn.close()

def ziskej_vsechny_druhy():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nazev FROM druhy_zvere ORDER BY nazev ASC"
    )

    druhy = cursor.fetchall()
    conn.close()
    return druhy


def pridej_druh(nazev):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO druhy_zvere (nazev) VALUES (?)",
        (nazev,)
    )

    conn.commit()
    conn.close()

def ziskej_nazev_druhu(druh_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nazev FROM druhy_zvere WHERE id=?",
        (druh_id,)
    )

    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""
