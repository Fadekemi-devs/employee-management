# Employee Management App

A Flask web application for managing employee records, built as a DevOps capstone project during an internship at ALAT by Wema.

Live demo: (add the Render URL here)



## What it does
- User registration and login (Flask-Login)
- Add, view, edit and delete employee records
- Stores data in PostgreSQL
- Exposes Prometheus metrics at /metrics

## Tech stack
- Python 3.13 and Flask
- PostgreSQL 17
- Docker and Docker Compose
- Prometheus for monitoring
- GitHub Actions for CI
- Render for cloud hosting

## Run locally with Docker Compose
    docker compose up --build

- App: http://localhost:5000
- Prometheus: http://localhost:9090

If the image build fails with a DNS error, build it with the host network first:

    docker build --network=host -f dockerfile -t employee-management-app .
    docker compose up

## Configuration
The app reads its settings from environment variables:

| Variable | Purpose |
| --- | --- |
| DATABASE_URL | PostgreSQL connection string |
| SECRET_KEY | Flask session secret |
| PORT | Port the app listens on (5000) |

Never commit real values. Secrets are set in the Render dashboard or in docker-compose.yml for local use only.

## CI/CD
- `ci.yml` runs on every push to main: installs dependencies, syntax-checks the code and builds the Docker image.
- `deploy.yml` is the Azure deployment workflow. It runs manually (workflow_dispatch) because no Azure subscription was available.
- Render deploys automatically f[ -f README.md ] && echo "README exists - stop and tell me" || cat > README.md <<'EOF'
# Employee Management App

A Flask web application for managing employee records, built as a DevOps capstone project during an internship at ALAT by Wema.

Live demo: (add the Render URL here)

## What it does
- User registration and login (Flask-Login)
- Add, view, edit and delete employee records
- Stores data in PostgreSQL
- Exposes Prometheus metrics at /metrics

## Tech stack
- Python 3.13 and Flask
- PostgreSQL 17
- Docker and Docker Compose
- Prometheus for monitoring
- GitHub Actions for CI
- Render for cloud hosting

## Run locally with Docker Compose
    docker compose up --build

- App: http://localhost:5000
-[ -f README.md ] && echo "README exists - stop and tell me" || cat > README.md <<'EOF'
# Employee Management App

A Flask web application for managing employee records, built as a DevOps capstone project during an internship at ALAT by Wema.

Live demo: (add the Render URL here)

## What it does
- User registration and login (Flask-Login)
- Add, view, edit and delete employee records
- Stores data in PostgreSQL
- Exposes Prometheus metrics at /metrics

## Tech stack
- Python 3.13 and Flask
- PostgreSQL 17
- Docker and Docker Compose
- Prometheus for monitoring
- GitHub Actions for CI
- Render for cloud hosting

## Run locally with Docker Compose
    docker compose up --build

- App: http://localhost:5000
- Prometheus: http://localhost:9090

If the image build fails with a DNS error, build it with the host network first:

    docker build --network=host -f dockerfile -t employee-management-app .
    docker compose up

## Configuration
The app reads its settings from environment variables:

| Variable | Purpose |
| --- | --- |
| DATABASE_URL | PostgreSQL connection string |
| SECRET_KEY | Flask session secret |
| PORT | Port the app listens on (5000) |

Never commit real values. Secrets are set in the Render dashboard or in docker-compose.yml for local use only.

## CI/CD
- `ci.yml` runs on every push to main: installs dependencies, syntax-checks the code and builds the Docker image.
- `deploy.yml` is the Azure deployment workflow. It runs manually (workflow_dispatch) because no Azure subscription was available.
- Render deploys automatically from the main branch.

#zzzrometheus: http://localhost:9090:

| Variable | Purpose |
| --- | --- |
| DATABASE_URL | PostgreSQL connection string |
| SECRET_KEY | Flask session secret |
| PORT | Port the app listens on (5000) |

Never commit real values. Secrets are set in the Render dashboard or in docker-compose.yml for local use only.

## CI/CD
- `ci.yml` runs on every push to main: installs dependencies, syntax-checks the code and builds the Docker image.
- `deploy.yml` is the Azure deployment workflow. It runs manually (workflow_dispatch) because no Azure subscription was available.
- Render deploys automatically from the main branch.

## Monitoring
The app uses prometheus-flask-exporter. Prometheus scrapes /metrics every 5 seconds, and the target can be checked at http://localhost:9090/targets.

## Future work
- Run the Azure deployment workflow and apply the Terraform configuration in the terraform folder once an Azure subscription is available.
- Add Grafana dashboards.
- Replace the Flask development server with a production server such as gunicorn.
EOFrom the main branch.

## Monitoring
The app uses prometheus-flask-exporter. Prometheus scrapes /metrics every 5 seconds, and the target can be checked at http://localhost:9090/targets.

## Future work
- Run the Azure deployment workflow and apply the Terraform configuration in the terraform folder once an Azure subscription is available.
- Add Grafana dashboards.
- Replace the Flask development server with a production server such as gunicorn.
