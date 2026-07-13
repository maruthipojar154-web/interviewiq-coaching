# ============================================================
# Database — MySQL connection pool (mysql-connector-python)
# ============================================================
import mysql.connector
from mysql.connector import pooling
from config import Config

_pool = None


def init_pool():
    global _pool
    try:
        _pool = pooling.MySQLConnectionPool(
            pool_name="interviewiq_pool",
            pool_size=10,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME,
            autocommit=True,
        )
        # Quick test
        conn = _pool.get_connection()
        conn.close()
        print(f"✅ MySQL connected: {Config.DB_NAME}")
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        print("   Check DB_HOST / DB_USER / DB_PASSWORD / DB_NAME in your .env file.")


def get_connection():
    if _pool is None:
        init_pool()
    return _pool.get_connection()


def query(sql, params=None, fetchone=False, fetchall=False, commit=False):
    """
    Run a SQL query and return results.
    - fetchone: returns a single dict row or None
    - fetchall: returns a list of dict rows
    - commit: for INSERT/UPDATE/DELETE, returns lastrowid
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        if commit:
            conn.commit()
            result = cursor.lastrowid
        cursor.close()
        return result
    finally:
        conn.close()
