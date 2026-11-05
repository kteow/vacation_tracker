from database.database import get_connection
from models.vacation_request import VacationRequest

# порядок столбцов как в модели VacationRequest:
# 6 столбцов таблицы + employee_full_name, type_name, status_name
SELECT_REQUEST = """
    SELECT v.request_id, v.employee_id, v.vacation_type_id, v.start_date,
           v.duration_days, v.request_status,
           e.surname || ' ' || e.name,
           t.type_name, s.status
    FROM vacation_requests v
    JOIN employees e ON e.employee_id = v.employee_id
    JOIN vacation_types t ON t.vacation_type_id = v.vacation_type_id
    JOIN request_statuses s ON s.request_status_id = v.request_status
"""

def _map(row):
    return VacationRequest(*row)

def create(employee_id, vacation_type_id, start_date, duration_days):
    conn = get_connection()
    cur = conn.cursor()
    # новая заявка всегда получает статус 1 ("На рассмотрении")
    cur.execute("""
        INSERT INTO vacation_requests(employee_id, vacation_type_id,
                                      start_date, duration_days, request_status)
        VALUES (?, ?, ?, ?, 1)
    """, (employee_id, vacation_type_id, start_date, duration_days))
    conn.commit()
    conn.close()

def get_by_id(request_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_REQUEST + " WHERE v.request_id = ?", (request_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_REQUEST + " ORDER BY v.start_date")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_employee(employee_id):
    # заявки одного сотрудника (для меню "Мои заявки")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_REQUEST + " WHERE v.employee_id = ? ORDER BY v.start_date",
                (employee_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update_status(request_id, status_id):
    # одобрить (2) или отклонить (3) заявку
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE vacation_requests SET request_status = ? WHERE request_id = ?",
                (status_id, request_id))
    conn.commit()
    conn.close()

def update(request_id, vacation_type_id, start_date, duration_days):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE vacation_requests
        SET vacation_type_id = ?, start_date = ?, duration_days = ?
        WHERE request_id = ?
    """, (vacation_type_id, start_date, duration_days, request_id))
    conn.commit()
    conn.close()

def delete(request_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM vacation_requests WHERE request_id = ?", (request_id,))
    conn.commit()
    conn.close()