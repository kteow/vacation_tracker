import sqlite3
import os

#путь к файлу vacations.db (лежит рядом с этим файлом)
DB_PATH = os.path.join(os.path.dirname(__file__), "vacations.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)        #подключаемся к базе
    conn.execute("PRAGMA foreign_keys = ON")  #включаем проверку связей между таблицами
    return conn