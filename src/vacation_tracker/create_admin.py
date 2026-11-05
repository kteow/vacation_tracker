from database.database import get_connection
from services.password_service import hash_password
from services import auth_service

# данные администратора, можешь поменять на свои
LOGIN = "admin"
PASSWORD = "1234567890"

conn = get_connection()
cur = conn.cursor()

# если справочники пустые, заполняем их (без них нельзя создать сотрудника)
cur.execute("SELECT COUNT(*) FROM user_roles")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO user_roles(name) VALUES ('Администратор'), ('Сотрудник')")

cur.execute("SELECT COUNT(*) FROM departments")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO departments(name) VALUES "
                "('Отдел кадров'), ('Бухгалтерия'), ('IT-отдел')")

# проверяем, есть ли уже такой логин
cur.execute("SELECT COUNT(*) FROM employees WHERE login = ?", (LOGIN,))
if cur.fetchone()[0] > 0:
    # администратор есть: просто ставим ему пароль заново
    cur.execute("UPDATE employees SET password_hash = ?, user_role_id = 1 "
                "WHERE login = ?", (hash_password(PASSWORD), LOGIN))
    print("Пароль администратора обновлён")
else:
    # администратора нет: создаём (роль 1 = Администратор)
    cur.execute("""
        INSERT INTO employees(name, surname, patronymic, login, password_hash,
                              position, user_role_id, department_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("Админ", "Системный", None, LOGIN, hash_password(PASSWORD),
          "Администратор", 1, 1))
    print("Администратор создан")

conn.commit()
conn.close()

# проверяем вход тем же кодом, которым входит программа
user = auth_service.authenticate(LOGIN, PASSWORD)
if user and user.user_role_id == 1:
    print("Вход работает! Логин:", LOGIN, "Пароль:", PASSWORD)
else:
    print("Вход НЕ работает, пришли скриншот этой ошибки")