from database.database import get_connection
from models.user_role import UserRole

def _map(row):
    return UserRole(*row)

def create(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_roles(name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_by_id(user_role_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_role_id, name FROM user_roles WHERE user_role_id = ?",
                (user_role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_role_id, name FROM user_roles ORDER BY user_role_id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(user_role_id, name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE user_roles SET name = ? WHERE user_role_id = ?",
                (name, user_role_id))
    conn.commit()
    conn.close()

def delete(user_role_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM user_roles WHERE user_role_id = ?", (user_role_id,))
    conn.commit()
    conn.close()