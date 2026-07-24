import os
from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask, render_template, request, redirect, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from prometheus_client import Counter, generate_latest
from werkzeug.security import check_password_hash
from database import (
    get_employees,
    add_employee,
    get_employee_by_id,
    update_employee,
    delete_employee,
    register_user,
    get_user_by_username,
    get_user_by_id,
    get_employee_by_user_id
)
from database import create_table

create_table()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devkey")

login_manager = LoginManager(app)
login_manager.login_view = "login"

metrics = PrometheusMetrics(app)

employee_created = Counter("employee_created_total", "Total employees created")
employee_updated = Counter("employee_updated_total", "Total employees updated")
employee_deleted = Counter("employee_deleted_total", "Total employees deleted")

class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
    def is_authenticated(self): return True
    def is_active(self): return True
    def is_anonymous(self): return False
    def get_id(self): return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(int(user_id))
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        existing_user = get_user_by_username(username)
        if existing_user:
            return render_template("register.html",
                error="Username already taken")
        register_user(username, email, password)
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_data = get_user_by_username(username)
        if user_data and check_password_hash(user_data[3], password):
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            return redirect("/dashboard")
        return render_template("login.html",
            error="Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/dashboard")
@login_required
def dashboard():
    employees = get_employees()
    return render_template("dashboard.html", employees=employees)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    employee = get_employee_by_user_id(current_user.id)
    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        position = request.form["position"]
        salary = request.form["salary"]
        if employee:
            update_employee(employee[0], name, department, position, salary)
            employee_updated.inc()
        else:
            add_employee(name, current_user.email, department, position, salary, current_user.id)
            employee_created.inc()
        return redirect("/profile")
    return render_template("profile.html",
        employee=employee,
        username=current_user.username)

@app.route("/delete/<int:employee_id>")
@login_required
def delete(employee_id):
    employee = get_employee_by_id(employee_id)
    if employee and employee[6] == current_user.id:
        delete_employee(employee_id)
        employee_deleted.inc()
    return redirect("/profile")

@app.route("/metrics")
def metrics_endpoint():
    return Response(generate_latest(), mimetype="text/plain")

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)