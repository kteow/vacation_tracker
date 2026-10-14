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

# Проверяем, что данные добавились: выводим заявки с фамилиями, видами и статусами
cursor = connection.cursor()
cursor.execute("""
    SELECT employees.surname, vacation_types.type_name,
           vacation_requests.start_date, vacation_requests.duration_days,
           request_statuses.status
    FROM vacation_requests
    JOIN employees ON employees.employee_id = vacation_requests.employee_id
    JOIN vacation_types ON vacation_types.vacation_type_id = vacation_requests.vacation_type_id
    JOIN request_statuses ON request_statuses.request_status_id = vacation_requests.request_status
""")
for row in cursor.fetchall():
    print(row)

# Закрываем соединение
connection.close()
