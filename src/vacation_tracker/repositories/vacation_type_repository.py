from database.database import get_connection
from models.vacation_type import VacationType

def _map(row):
    # превращаем кортеж из базы в объект VacationType
    return VacationType(*row)

def get_by_id(vacation_type_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT vacation_type_id, type_name FROM vacation_types "
                "WHERE vacation_type_id = ?", (vacation_type_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT vacation_type_id, type_name FROM vacation_types "
                "ORDER BY vacation_type_id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]