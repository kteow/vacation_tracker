import sqlite3
import os

# папка, где лежит этот файл (там же лежат vacations.db и scheme.sql)
FOLDER = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(FOLDER, "vacations.db")
SCHEME_PATH = os.path.join(FOLDER, "scheme.sql")

def get_connection():
    conn = sqlite3.connect(DB_PATH)           # подключаемся к базе
    conn.execute("PRAGMA foreign_keys = ON")  # включаем проверку связей между таблицами
    return conn

def init_database():
    # если таблицы ещё не созданы, создаём их из scheme.sql
    # здесь подключаемся напрямую, без проверки связей: скрипт сам создаёт всё по порядку
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master "
                "WHERE type = 'table' AND name = 'employees'")
    table_exists = cur.fetchone()
    if not table_exists:
        with open(SCHEME_PATH, encoding="utf-8") as file:
            conn.executescript(file.read())
        conn.commit()
    conn.close()