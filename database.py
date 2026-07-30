
import os
import psycopg
from werkzeug.security import generate_password_hash
def get_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])

def create_table():
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
def get_employees():
    conn = get_connection()

    cur = conn.cursor()

    cur.execute("SELECT * FROM employees")

    employees = cur.fetchall()

    cur.close()
    conn.close()

    return employees
def add_employee(name, email, department, position, salary, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO employees (name, email, department, position, salary, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, email, department, position, salary, user_id))
    conn.commit()
    cur.close()
    conn.close()
def get_employee_by_id(employee_id):

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


def update_employee(
    employee_id,
    name,
    department,
    position,
    salary
):

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
        (
            name,
            department,
            position,
            salary,
            employee_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()
def delete_employee(employee_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM employees WHERE id = %s",
        (employee_id,)
    )

    conn.commit()

    cur.close()
    conn.close()
def register_user(username, email, password):
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
def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user
def get_employee_by_user_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE user_id = %s", (user_id,))
    employee = cur.fetchone()
    cur.close()
    conn.close()
    return employee
def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user