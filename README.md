<!-- This README explains how to build, run, inspect, and publish the full-stack Docker Compose application. -->
# Session 4: Full-Stack Docker Compose

## Goal

Run a frontend, backend, and PostgreSQL database with one command.

## Architecture

```text
Browser -> Frontend (Nginx) -> Backend (Flask) -> PostgreSQL
```

## Topics

- Multi-container application
- Dockerfiles
- Docker Compose
- Environment variables
- Networks
- Persistent volume
- Health checks

## Instructor Flow

### 1. Show the project

```bash
tree -a -I __pycache__
```

### 2. Review the containers

- `frontend`: HTML/JavaScript served by Nginx
- `backend`: Python Flask API
- `db`: PostgreSQL database

### 3. Review `compose.yaml`

Point out:

- `build` and `image`
- `ports`
- `environment`
- `depends_on`
- `healthcheck`
- `networks`
- `volumes`

### 4. Start the application

```bash
docker compose up --build
```

Open: <http://localhost:8080>

### 5. Inspect the stack

```bash
docker compose ps
docker compose logs backend
docker compose exec db psql -U appuser -d taskdb -c "SELECT * FROM tasks;"
```

### 6. Demonstrate persistence

Add a task, then run:

```bash
docker compose down
docker compose up
```

The task remains because PostgreSQL uses a named volume.

### 7. Stop and clean up

Stop containers and keep data:

```bash
docker compose down
```

Stop containers and delete data:

```bash
docker compose down -v
```

## Push Images to Docker Hub

Only publish the custom `frontend` and `backend` images. PostgreSQL already uses the official `postgres` image.

### 1. Create Docker Hub Repositories

Sign in to <https://hub.docker.com> and create:

- `phase2-session4-frontend`
- `phase2-session4-backend`

### 2. Build and Push Locally

Create a Docker Hub access token:

1. Open **Docker Hub > Account settings > Personal access tokens**.
2. Create a token with **Read & Write** permission.
3. Sign in from the terminal:

```bash
docker login -u YOUR_DOCKERHUB_USERNAME
```

Use the access token as the password.

Build and push both images:

```bash
docker build -t YOUR_DOCKERHUB_USERNAME/phase2-session4-frontend:latest ./frontend
docker push YOUR_DOCKERHUB_USERNAME/phase2-session4-frontend:latest

docker build -t YOUR_DOCKERHUB_USERNAME/phase2-session4-backend:latest ./backend
docker push YOUR_DOCKERHUB_USERNAME/phase2-session4-backend:latest
```

### 3. Build and Push with GitHub Actions

The workflow `.github/workflows/docker-publish.yml` runs when code is pushed to `main`. It builds and pushes both images.

Add the Docker Hub credentials to GitHub:

1. Open the GitHub repository.
2. Go to **Settings > Secrets and variables > Actions**.
3. Under **Secrets**, add:
   - `DOCKERHUB_USERNAME`: your Docker Hub username
   - `DOCKERHUB_TOKEN`: a Docker Hub access token with Read & Write permission
4. Push the project to the `main` branch or run the workflow manually from the **Actions** tab.

Use GitHub **Secrets**, not regular variables, for passwords and tokens. The username is also stored as a secret here to keep the workflow simple.

## Quick Checks

```bash
curl http://localhost:8080/api/tasks
docker compose ps
```

## Student Exercise

Add a `description` field to each task.
