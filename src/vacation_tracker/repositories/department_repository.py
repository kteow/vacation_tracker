from database.database import get_connection
from models.department import Department

def _map(row):
    return Department(*row)

def create(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO departments(name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_by_id(department_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT department_id, name FROM departments WHERE department_id = ?",
                (department_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT department_id, name FROM departments ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(department_id, name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE departments SET name = ? WHERE department_id = ?",
                (name, department_id))
    conn.commit()
    conn.close()

def delete(department_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM departments WHERE department_id = ?", (department_id,))
    conn.commit()
    conn.close()