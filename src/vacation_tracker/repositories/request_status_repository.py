from database.database import get_connection
from models.request_status import RequestStatus

def _map(row):
    return RequestStatus(*row)

def create(status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO request_statuses(status) VALUES (?)", (status,))
    conn.commit()
    conn.close()

def get_by_id(request_status_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT request_status_id, status FROM request_statuses "
                "WHERE request_status_id = ?", (request_status_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT request_status_id, status FROM request_statuses "
                "ORDER BY request_status_id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def update(request_status_id, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE request_statuses SET status = ? WHERE request_status_id = ?",
                (status, request_status_id))
    conn.commit()
    conn.close()

def delete(request_status_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM request_statuses WHERE request_status_id = ?",
                (request_status_id,))
    conn.commit()
    conn.close()