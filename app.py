from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask, render_template, request, redirect, Response
from database import get_employees, add_employee, get_employee_by_id, update_employee, delete_employee
from prometheus_client import Counter
from database import create_table

create_table()

app = Flask(__name__)

metrics = PrometheusMetrics(app)

employee_created = Counter(
    "employee_created_total",
    "Total employees created"
)



@app.route("/")
def home():


    employees = get_employees()

    return render_template(
        "index.html",
        employees=employees
        )

@app.route("/add", methods=["POST"])
def add():

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]
    position = request.form["position"]
    salary = request.form["salary"]
    add_employee(
        name,
        email,
        department,
        position,
        salary
    )
    employee_created.inc()
    return redirect("/")
@app.route("/edit/<int:employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        department = request.form["department"]
        position = request.form["position"]
        salary = request.form["salary"]
        employee_updated.inc()
        update_employee(
            employee_id,
            name,
            email,
            department,
            position,
            salary
        )

        return redirect("/")

    employee = get_employee_by_id(employee_id)

    return render_template(
        "edit.html",
        employee=employee
    )

    return redirect("/")
@app.route("/delete/<int:employee_id>")
def delete(employee_id):

    delete_employee(employee_id)
    employee_deleted.inc()
    return redirect("/")

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype="text/plain"
    )

    
@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )