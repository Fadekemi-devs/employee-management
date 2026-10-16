import os
import psycopg
from werkzeug.security import generate_password_hash

def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            return psycopg.connect(db_url)
        except psycopg.OperationalError as e:
            print(f"DATABASE_URL connection failed: {e}. Attempting fallback options...")

    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "password")
    dbname = os.environ.get("DB_NAME", "employee_db")
    port = os.environ.get("DB_PORT", "5432")

    configured_host = os.environ.get("DB_HOST", "localhost")

    hosts = [configured_host]
    if "dpg-db7k5i2vcj2c73dv1a3g-a" not in hosts:
        hosts.append("dpg-db7k5i2vcj2c73dv1a3g-a")
    if "localhost" not in hosts:
        hosts.append("localhost")

    last_exception = None
    for host in hosts:
        try:
            url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
            return psycopg.connect(url)
        except psycopg.OperationalError as e:
            last_exception = e
            print(f"Connection to host '{host}' failed: {e}")

    if last_exception:
        raise last_exception
    raise psycopg.OperationalError("Unable to connect to any database server")

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
