from database.database import get_connection
from models.employee import Employee

# SELECT вынесли в одну переменную, чтобы не писать его в каждой функции.
# Порядок столбцов ТОЧНО такой же, как поля в модели Employee.
# JOIN подтягивает названия роли и подразделения вместо номеров.
SELECT_EMPLOYEE = """
    SELECT e.employee_id, e.name, e.surname, e.patronymic, e.login,
           e.password_hash, e.position, e.user_role_id, e.department_id,
           r.name, d.name
    FROM employees e
    JOIN user_roles r ON r.user_role_id = e.user_role_id
    JOIN departments d ON d.department_id = e.department_id
"""

def _map(row):
    # превращаем кортеж из базы в объект Employee
    return Employee(*row)

def create(name, surname, patronymic, login, password_hash,
           position, user_role_id, department_id):
    conn = get_connection()      # подключаемся к базе
    cur = conn.cursor()          # курсор нужен для выполнения запросов
    cur.execute("""
        INSERT INTO employees(name, surname, patronymic, login,
                              password_hash, position, user_role_id, department_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, surname, patronymic, login, password_hash,
          position, user_role_id, department_id))   # ? защищают от SQL-инъекций
    conn.commit()                # сохраняем изменения
    conn.close()                 # закрываем соединение

def get_by_id(employee_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_EMPLOYEE + " WHERE e.employee_id = ?", (employee_id,))
    row = cur.fetchone()         # одна строка или None, если не нашли
    conn.close()
    return _map(row) if row else None

def get_by_login(login):
    # нужна для входа в систему и для проверки, что логин свободен
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_EMPLOYEE + " WHERE e.login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_EMPLOYEE + " ORDER BY e.surname")
    rows = cur.fetchall()        # список всех найденных строк
    conn.close()
    return [_map(r) for r in rows]   # каждую строку превращаем в Employee

def update(employee_id, name, surname, patronymic, position, department_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE employees
        SET name = ?, surname = ?, patronymic = ?,
            position = ?, department_id = ?
        WHERE employee_id = ?
    """, (name, surname, patronymic, position, department_id, employee_id))
    conn.commit()                # WHERE важен: без него изменятся ВСЕ сотрудники
    conn.close()

def delete(employee_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
    conn.commit()
    conn.close()