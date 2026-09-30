# Docker
[![Docker](https://shields.io)](https://docker.com)

## Docker Description

1. How Docker was configured for the Smart Farmer-to-Buyer Produce Matching System.
  - [Learn how Docker was set up](#how-docker-was-set-up)
2. How a new collaborator can prepare their machine, obtain the project, switch to their development branch, and start the complete development environment.
  - [Setup your machine](#collaborator-setup)


The repository is the source of truth for the current configuration. The Docker environment is intended for **local development**, not production deployment.

---

## Docker Development

The project uses Docker Compose to run three services:

- **`db`** — PostgreSQL 16
[![PostgreSQL](https://shields.io)](https://www.postgresql.org/)

- **`backend`** — Django
[![Django](https://shields.io)](https://www.djangoproject.com/)

- **`frontend`** — React with Vite
[![React](https://shields.io)](https://react.dev)


The services run inside Docker while the developer interacts with them through exposed localhost ports.

```text
Developer Machine
       |
       v
 Docker Compose
       |
       +-------------------------+
       |                         |
       v                         v
   Frontend                  Backend
   React / Vite              Django
   Port 5173                 Port 8000
                                  |
                                  v
                              PostgreSQL
                               Port 5432
                                  |
                                  v
                           postgres_data
                           Docker Volume
```

The current repository configuration uses PostgreSQL 16, Django 4.2, Python 3.11, Node.js 20, React 19 and Vite.

The database is persisted through the Docker-managed `postgres_data` volume, while the backend and frontend source directories are mounted into their respective containers for development-time code reloading.

---

## How Docker Was Set Up

### Why Docker was introduced

The development environment was containerized so that developers do not need to install and configure the project's Python, Node.js, or PostgreSQL runtime environments directly on their host machines.

Docker Compose manages the three services together and provides a consistent development environment across team members' machines.

---

### 1. Database service

The database is provided by the official PostgreSQL 16 Alpine image:

```yaml
image: postgres:16-alpine
```

The Compose service is named:

```text
db
```

and the container is explicitly named:

```text
smart_farmer_db
```

#### a. Database configuration

The service currently uses these development defaults:

```text
Database: smart_farmer_db
Username: smart_farmer_user
Password: smart_farmer_password
Port: 5432
```

These values are configurable through environment variables:

```yaml
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

The Compose configuration provides development fallback values when those variables are not supplied.

#### b. Host-to-container port mapping

```yaml
ports:
  - "5432:5432"
```

This allows database tools running on the developer's machine to connect through:

```text
localhost:5432
```

For example, a developer can use a PostgreSQL-compatible GUI such as DBeaver or pgAdmin.

#### c.Persistent storage

PostgreSQL uses the named Docker volume:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

The purpose of this volume is to keep database records outside the lifecycle of the PostgreSQL container.

Therefore:

```bash
docker compose stop
```

or:

```bash
docker compose down
```

does not normally remove the database records.

The database volume is only removed when explicitly requested, for example:

```bash
docker compose down -v
```

> **Warning:** `docker compose down -v` removes the project's Docker volumes and therefore deletes the local PostgreSQL data stored in `postgres_data`.

#### d. Database health check

The database has a health check using `pg_isready`:

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-smart_farmer_user} -d ${POSTGRES_DB:-smart_farmer_db}"]
  interval: 5s
  timeout: 5s
  retries: 5
```

The backend depends on this health status before starting:

```yaml
depends_on:
  db:
    condition: service_healthy
```

This prevents the backend from attempting to connect to PostgreSQL before the database is ready.

---

### 2. Django Backend Container

The backend is built from:

```text
backend/Dockerfile
```

The Docker image starts from:

```dockerfile
FROM python:3.11-slim
```

The container uses:

```text
Working directory: /app
Port: 8000
```

The Django development server starts with:

```bash
python manage.py runserver 0.0.0.0:8000
```

#### a. Python dependencies

Backend dependencies are defined in:

```text
backend/requirements.txt
```

Current dependencies include:

```text
Django>=4.2,<5.0
psycopg2-binary>=2.9.9
django-cors-headers>=4.3.0
python-dotenv>=1.0.0
```

`psycopg2-binary` provides PostgreSQL connectivity for Django.

#### b. Backend port

Docker maps:

```yaml
ports:
  - "8000:8000"
```

Therefore Django is accessible from the developer's browser at:

```text
http://localhost:8000
```

#### c. Live code reloading

The backend uses:

```yaml
volumes:
  - ./backend:/app
```

This mounts the local `backend/` directory into `/app` inside the container.

Consequently, backend code changes made on the host are immediately visible inside the container and Django's development server can reload them.

#### d. Backend database configuration

Django does not use `localhost` to reach PostgreSQL.

Inside the Docker network, the database service is addressed by its Compose service name:

```text
db
```

The relevant configuration is:

```text
DB_HOST=db
DB_PORT=5432
```

Django therefore connects to:

```text
db:5432
```

rather than:

```text
localhost:5432
```

This distinction is important because `localhost` inside the backend container refers to the backend container itself.

---

### 5. Django Environment Configuration

The Django settings retrieve configuration from environment variables.

The current configuration includes:

```python
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-dev-fallback-key'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```

The database configuration similarly reads from the environment:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'smart_farmer_db'),
        'USER': os.environ.get('POSTGRES_USER', 'smart_farmer_user'),
        'PASSWORD': os.environ.get(
            'POSTGRES_PASSWORD',
            'smart_farmer_password'
        ),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

This keeps the application configuration separate from the Docker implementation.

The fallback values are development values only and must not be treated as production credentials.

---

### 6. CORS Configuration

The React development server runs on:

```text
http://localhost:5173
```

while Django runs on:

```text
http://localhost:8000
```

These are different origins.

The backend therefore includes `django-cors-headers` and permits the frontend development origins:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

The middleware is included in Django's middleware configuration:

```python
'corsheaders.middleware.CorsMiddleware',
```

This allows browser requests from the React development application to reach Django.

---

### 7. React/Vite Frontend Container

The frontend is built from:

```text
frontend/Dockerfile
```

The Docker image uses:

```dockerfile
FROM node:20-alpine
```

The container uses:

```text
Working directory: /app
Port: 5173
```

The development server is started with:

```bash
npm run dev -- --host
```

#### a. Frontend port

Docker maps:

```yaml
ports:
  - "5173:5173"
```

The frontend is therefore available at:

```text
http://localhost:5173
```

#### b. Live reloading

The frontend uses:

```yaml
volumes:
  - ./frontend:/app
  - /app/node_modules
```

The first volume makes the developer's source code available inside the container.

The second volume keeps the container's `node_modules` separate from the host filesystem.

This is important because the host's filesystem should not overwrite the dependencies installed inside the Node.js container.


---

### 8. Docker Ignore Files

Separate `.dockerignore` files are used for the backend and frontend.

#### a. Backend

```text
backend/.dockerignore
```

It excludes items such as:

```text
__pycache__/
*.py[cod]
.venv/
venv/
.git/
.env
*.log
```

This prevents unnecessary files and local secrets from being included in the backend Docker build context.

### b. Frontend

```text
frontend/.dockerignore
```

It excludes items such as:

```text
node_modules/
build/
dist/
.git/
.env
.env.*
npm-debug.log*
```

This prevents local Node dependencies, generated builds, and environment files from being copied into the image.

---

### 9. Environment and Secret Management

The repository contains:

```text
.env.example
```

which documents the development environment variables expected by the project.

It currently includes:

```text
POSTGRES_DB=smart_farmer_db
POSTGRES_USER=smart_farmer_user
POSTGRES_PASSWORD=smart_farmer_password
DB_HOST=db
DB_PORT=5432

DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-infisical
```

The repository also contains:

```text
.infisical.json
```

which identifies the Infisical workspace used for the project.

### 10. Infisical

Infisical is used as the project's secret-management solution for development.

The intended workflow is to inject environment variables at runtime rather than committing real sensitive credentials to Git.

For example:

```bash
infisical run -- docker compose up -d
```

The important principle is:

```text
Application code
       |
       v
Environment variables
       |
       v
Infisical / local development configuration
```

rather than:

```text
Application code
       |
       v
Hard-coded passwords and secrets
```

### NOTE: Important distinction

Not every environment variable is necessarily a secret.

Examples of ordinary development configuration include:

```text
DEBUG
DB_HOST
DB_PORT
POSTGRES_DB
```

Values such as the following should be treated as sensitive:

```text
POSTGRES_PASSWORD
SECRET_KEY
API keys
Access tokens
Third-party service credentials
```

Never place real production credentials in the repository.

---

### 11. Git Configuration for Docker

The root `.gitignore` excludes local environment and runtime files.

Relevant entries include:

```text
.postgres_data/
*.log
.env
.env.*
!.env.example
```

This allows:

```text
.env.example
```

to remain tracked while normal `.env` files remain ignored.

Developers should always check:

```bash
git status
```

before committing to ensure that credentials, local database files, generated files, and other unintended artifacts are not staged.

---

## New Collaborator Setup

### Prerequisites

A new collaborator does **not** need to install Python, Node.js, or PostgreSQL directly on the host machine for the Docker development environment.

The required host tools are:

- Git
- Docker Engine with Docker Compose, or Docker Desktop
- Infisical CLI

---

### 1. Install Docker

Install Docker using the [Official Docker Guide][docker-setup].

[docker-setup]: https://oneuptime.com/blog/post/2026-03-02-how-to-install-docker-engine-on-ubuntu-official-method/view


After installation, verify:

```bash
docker --version
docker compose version
```

The Docker daemon must also be running.

A simple verification is:

```bash
docker ps
```

If Docker is functioning correctly, the command should execute without a daemon connection error.
Errors? Use AI bro.

---

### 2. Install Infisical

Infisical is recommended for team development because it allows project environment variables and secrets to be injected into the Docker process.

On Linux Mint/Ubuntu, the documented installation is:

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/infisical/infisical-cli/setup.deb.sh' | sudo -E bash
```

Then:

```bash
sudo apt-get update
sudo apt-get install -y infisical
```

Verify the installation:

```bash
infisical --version
```
Log in to [Infisical][infisical-login].

[infisical-login]: https://infisical.com/docs/cli/install

Contact Robert for invitation to the team's project in infisical. Ensure you share your gmail with him. 

If access has been provided to the Infisical project, authenticate:

```bash
infisical login
```

Then initialize/link the local repository:

```bash
infisical init
```

The repository already contains:

```text
.infisical.json
```

which provides the project's Infisical workspace configuration.

---

### 3. Clone the Repository

Clone the project:

```bash
git clone https://github.com/deniskibichiy/smart-farmer-buyer.git
```

Enter the project:

```bash
cd smart-farmer-buyer
```

Do not begin development directly on `main`.

---

### 4. Update `main`

Make sure your local `main` branch contains the latest remote changes:

```bash
git switch main
git pull origin main
```

This follows the project's contribution guidelines.

---

### 5. Create Your Feature Branch

Create a dedicated branch for the task you have been assigned.

For example:

```bash
git switch -c feature/your-feature-name
```

Examples:

```bash
git switch -c feature/supply-api
git switch -c feature/matching-algorithm
git switch -c feature/demand-api
```

The branch should describe the work being performed.

Do not work directly on `main`.

---

### 6. Start the Docker Environment

Run:

```bash
infisical run --env=dev -- docker compose up --build
```

or 

```bash
infisical run -- docker compose up -d --build
```

if it doesn't work.

Infisical injects the configured environment variables into the Docker Compose process.

Docker then builds and starts:

```text
db
backend
frontend
```

---

### 7. What Happens When Docker Starts

When this command runs:

```bash
infisical run --env=dev -- docker compose up --build
```

Docker performs the following process:

```text
Build backend image
        |
        v
Build frontend image
        |
        v
Create/start PostgreSQL
        |
        v
PostgreSQL health check
        |
        v
Start Django backend
        |
        v
Start React/Vite frontend
```

The resulting services are:

```text
smart_farmer_db
smart_farmer_backend
smart_farmer_frontend
```

The database is given time to become healthy before the backend starts.

---

### 8. Verify the Containers

Run:

```bash
docker compose ps
```

You should see the three services:

```text
smart_farmer_db
smart_farmer_backend
smart_farmer_frontend
```

The database should report a healthy status.

If a service is not running, inspect its logs:

```bash
docker compose logs
```

Or inspect an individual service:

```bash
docker compose logs backend
```

```bash
docker compose logs frontend
```

```bash
docker compose logs db
```

For continuously updated logs:

```bash
docker compose logs -f
```

---

### 9. Run Django database migrations

After the containers are running, apply Django migrations from inside the backend container:

```bash
infisical run --env=dev -- docker compose exec backend python manage.py migrate
```

This creates the Django database tables in PostgreSQL.

When new Django models are introduced during development, create migrations with:

```bash
infisical run --env=dev -- docker compose exec backend python manage.py makemigrations
```

Then apply them:

```bash
docker compose exec backend python manage.py migrate
```

---

### 10. Create a Django Admin Account

If you need access to Django Admin, create a local superuser:

```bash
infisical run --env=dev -- docker compose exec backend python manage.py createsuperuser
```

Follow Django's prompts to create the account.

The admin interface is available at:

```text
http://localhost:8000/admin
```

---

### 11. Access Django shell

```bash
infisical run --env=dev -- docker compose exec backend python manage.py shell
```

---

### 12. Run Django tests

```bash
infisical run --env=dev -- docker compose exec backend python manage.py test
```

---

### 13. Access the development services

Once the containers are running:

| Service | Address |
|---|---|
| React/Vite frontend | `http://localhost:5173` |
| Django backend | `http://localhost:8000` |
| Django Admin | `http://localhost:8000/admin` |
| PostgreSQL | `localhost:5432` |

The frontend communicates with the Django development server through the configured:

```text
VITE_API_URL=http://localhost:8000
```

---

### 14. Inspecting the PostgreSQL database

The database is available from the host because Compose maps:

```text
5432:5432
```

A developer can use a PostgreSQL-compatible database GUI.

Connection details for the current development configuration are:

```text
Host: localhost
Port: 5432
Database: smart_farmer_db
Username: smart_farmer_user
Password: smart_farmer_password
```

The available approaches are:

### Django Admin

```text
http://localhost:8000/admin
```

Useful for inspecting application records through Django models.

### Database GUI

Compatible PostgreSQL database tools can connect through:

```text
localhost:5432
```

### PostgreSQL terminal

A developer can also access PostgreSQL directly from the container:

```bash
docker compose exec db psql -U smart_farmer_user -d smart_farmer_db
```

---

### 14. Daily Development Workflow

After the initial setup, a developer normally does not need to rebuild everything every time.

#### Start the environment

```bash
docker compose up -d
```

Or, using Infisical:

```bash
infisical run -- docker compose up -d
```

#### Check services

```bash
docker compose ps
```

#### View logs

```bash
docker compose logs -f
```

#### Stop containers

```bash
docker compose stop
```

This stops the containers without removing the database volume.

#### Shut down the Compose environment

```bash
docker compose down
```

This removes the running containers and network but does not normally remove the named database volume.

---

### 16. When to Rebuild

Rebuild the images when container dependencies change.

For example, after modifying:

```text
backend/requirements.txt
```

or:

```text
frontend/package.json
```

run:

```bash
infisical run --env=dev -- docker compose up --build
```

or run:

```bash
infisical run --env=dev -- docker compose up --build backend
```

if you want to rebuild a single service.

For frontend dependency problems, the frontend image can be rebuilt without using the existing build cache:

```bash
infisical run --env=dev -- docker compose build --no-cache frontend
```

Then:

```bash
infisical run --env=dev -- docker compose up -d frontend
```

---

### 17. Common development commands

#### Backend

Run migrations:

```bash
infisical run --env=dev -- docker compose exec backend python manage.py migrate
```

Create migrations:

```bash
infisical run --env=dev -- docker compose exec backend python manage.py makemigrations
```

Run Django tests:

```bash
infisical run --env=dev -- docker compose exec backend python manage.py test
```

Create an admin user:

```bash
infisical run --env=dev -- docker compose exec backend python manage.py createsuperuser
```

#### Frontend

Install a new npm dependency inside the frontend container:

```bash
infisical run --env=dev -- docker compose exec frontend npm install <package-name>
```

The frontend package configuration is stored in:

```text
frontend/package.json
```

Restart service

```bash
infisical run --env=dev -- docker compose up -d --build frontend
```

---

### 18. Important port conflicts

The development environment expects these host ports:

```text
5432 — PostgreSQL
8000 — Django
5173 — React/Vite
```

If Docker reports an error such as:

```text
bind: address already in use
```

another application on the host may already be using the required port.

For example, a locally installed PostgreSQL server could already be using port `5432`.

Check which application is using a required port before changing the Docker configuration.

If a host PostgreSQL service is running on Linux, it may be possible to stop it with:

```bash
sudo systemctl stop postgresql
```

Do not run this command blindly; first confirm that the service is actually responsible for the port conflict.

---

### 19. Database Reset

If the local development database needs to be completely recreated:

```bash
docker compose down -v
```

Then start the environment again:

```bash
infisical run --env=dev -- docker compose up
```

Finally run:

```bash
infisical run --env=dev -- docker compose exec backend python manage.py migrate
```

> **Warning:** `docker compose down -v` deletes the Docker volumes associated with the Compose project. This destroys the local PostgreSQL data stored in the volume.

Do not use this command merely to restart the application.

---


### 20. Docker files in the repo

The Docker development environment is composed of the following important files:

```text
smart-farmer-buyer/
│
├── .env.example
├── .gitignore
├── .infisical.json
├── docker-compose.yml
│
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── requirements.txt
│   └── config/
│       └── settings.py
│
└── frontend/
    ├── Dockerfile
    ├── .dockerignore
    └── package.json
```

#### File responsibilities

| File | Purpose |
|---|---|
| `docker-compose.yml` | Defines and orchestrates the database, backend and frontend services |
| `backend/Dockerfile` | Builds the Django development image |
| `backend/.dockerignore` | Prevents unnecessary backend files from entering the Docker build context |
| `backend/requirements.txt` | Defines Python dependencies |
| `frontend/Dockerfile` | Builds the React/Vite development image |
| `frontend/.dockerignore` | Prevents unnecessary frontend files from entering the Docker build context |
| `frontend/package.json` | Defines frontend dependencies and npm scripts |
| `.env.example` | Documents development environment variables |
| `.infisical.json` | Provides the repository's Infisical workspace configuration |
| `.gitignore` | Prevents local secrets and generated/runtime files from being committed |

---

### 21. First-Time Setup Checklist

A new collaborator is ready to begin development when:

- [ ] Git is installed
- [ ] Docker is installed and running
- [ ] `docker --version` works
- [ ] `docker compose version` works
- [ ] Infisical CLI is installed if using the team secret workflow
- [ ] The repository has been cloned
- [ ] `main` has been updated
- [ ] A feature branch has been created
- [ ] Infisical authentication/project initialization is complete when required
- [ ] Docker Compose starts successfully
- [ ] `smart_farmer_db` is healthy
- [ ] `smart_farmer_backend` is running
- [ ] `smart_farmer_frontend` is running
- [ ] Django migrations have been applied
- [ ] `http://localhost:5173` loads
- [ ] `http://localhost:8000` loads
- [ ] Django Admin is accessible if required
- [ ] No `.env` file or credentials are committed
- [ ] The developer is working from their feature branch

---

The Docker environment is intended to give every collaborator the same development foundation while allowing each developer to work independently on their own Git feature branch.

---