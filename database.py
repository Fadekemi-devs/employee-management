import os
import sqlite3
import psycopg
from werkzeug.security import generate_password_hash

class DBCursor:
    def __init__(self, mode, cursor):
        self.mode = mode
        self.cursor = cursor

    def execute(self, sql, params=()):
        if self.mode == 'sqlite':
            sql = sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
            sql = sql.replace("%s", "?")
        self.cursor.execute(sql, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()

class DBConnection:
    def __init__(self, mode, conn):
        self.mode = mode
        self.conn = conn

    def cursor(self):
        return DBCursor(self.mode, self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            pg_conn = psycopg.connect(db_url)
            return DBConnection('pg', pg_conn)
        except Exception as e:
            print(f"DATABASE_URL PostgreSQL connection failed: {e}")

    host = os.environ.get("DB_HOST")
    if host and host != "db":
        user = os.environ.get("DB_USER", "postgres")
        password = os.environ.get("DB_PASSWORD", "password")
        dbname = os.environ.get("DB_NAME", "employee_db")
        port = os.environ.get("DB_PORT", "5432")
        try:
            url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
            pg_conn = psycopg.connect(url)
            return DBConnection('pg', pg_conn)
        except Exception as e:
            print(f"PostgreSQL connection to host {host} failed: {e}")

    db_path = os.environ.get("SQLITE_DB_PATH", "/tmp/employee.db")
    sq_conn = sqlite3.connect(db_path)
    return DBConnection('sqlite', sq_conn)

def create_table():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                department VARCHAR(100),
                position VARCHAR(100),
                salary INTEGER,
                user_id INTEGER REFERENCES users(id)
            )
        """)

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database tables: {e}")

def get_employees():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees")
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return employees
    except Exception as e:
        print(f"Error in get_employees: {e}")
        return []

def add_employee(name, email, department, position, salary, user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO employees (name, email, department, position, salary, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, email, department, position, salary, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error in add_employee: {e}")
        return False

def get_employee_by_id(employee_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM employees WHERE id = %s",
            (employee_id,)
        )
        employee = cur.fetchone()
        cur.close()
        conn.close()
        return employee
    except Exception as e:
        print(f"Error in get_employee_by_id: {e}")
        return None

def update_employee(employee_id, name, department, position, salary):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE employees
            SET
                name=%s,
                department=%s,
                position=%s,
                salary=%s
            WHERE id=%s
            """,
            (name, department, position, salary, employee_id)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error in update_employee: {e}")
        return False

def delete_employee(employee_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM employees WHERE id = %s",
            (employee_id,)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error in delete_employee: {e}")
        return False

def register_user(username, email, password):
    try:
        password_hash = generate_password_hash(password)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error in register_user: {e}")
        return False

def get_user_by_username(username):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        print(f"Error in get_user_by_username: {e}")
        return None

def get_employee_by_user_id(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employees WHERE user_id = %s", (user_id,))
        employee = cur.fetchone()
        cur.close()
        conn.close()
        return employee
    except Exception as e:
        print(f"Error in get_employee_by_user_id: {e}")
        return None

def get_user_by_id(user_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        print(f"Error in get_user_by_id: {e}")
        return None
