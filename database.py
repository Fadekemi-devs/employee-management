
import os
import psycopg

def get_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        department VARCHAR(100),
        position VARCHAR(100),
        salary INTEGER
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
def add_employee(name, email, department, position, salary):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(
            """

            INSERT INTO employees
            (name, email, department, position, salary)
            VALUES (%s, %s, %s, %s, %s)
        """,
        (name, email, department, position, salary)
        )

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
    email,
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
            email=%s,
            department=%s,
            position=%s,
            salary=%s
        WHERE id=%s
        """,
        (
            name,
            email,
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