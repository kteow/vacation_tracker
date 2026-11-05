import os
import sqlite3

# папка, где лежит этот файл (там же лежат scheme.sql и vacations.db)
FOLDER = os.path.dirname(os.path.abspath(__file__))
SCHEME_PATH = os.path.join(FOLDER, "scheme.sql")
DB_PATH = os.path.join(FOLDER, "vacations.db")

# читаем SQL-команды из scheme.sql
with open(SCHEME_PATH, encoding="utf-8") as file:
    script = file.read()

# создаём базу и выполняем все команды из файла
conn = sqlite3.connect(DB_PATH)
conn.executescript(script)
conn.commit()
conn.close()

print("База создана:", DB_PATH)