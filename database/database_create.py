import sqlite3  # встроенная в Python библиотека для работы с SQLite

# Подключаемся к файлу базы данных (если файла нет, он создастся сам)
connection = sqlite3.connect("vacations.db")

# Включаем проверку внешних ключей (в SQLite она по умолчанию выключена)
connection.execute("PRAGMA foreign_keys = ON")

# Читаем SQL-запросы из файла scheme.sql
with open("scheme.sql", encoding="utf-8") as file:
    sql_script = file.read()

# Выполняем сразу все запросы из файла
connection.executescript(sql_script)

# Проверяем, что данные добавились: выводим сотрудников
cursor = connection.cursor()
cursor.execute("SELECT surname, name, position FROM employees")
for row in cursor.fetchall():
    print(row)

# Закрываем соединение
connection.close()
