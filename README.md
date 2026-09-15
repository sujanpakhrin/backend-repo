# Assignment 11 - Multi-Tier Application Backend

## Overview

This repository contains the backend service for Assignment 11, a multi-tier application built with Flask and MySQL.

The backend provides REST API endpoints for managing users and connects to a MySQL database using Docker Compose.

### Technologies Used

* Python 3.14
* Flask
* MySQL 8.0
* Docker
* Docker Compose
* Pytest
* GitHub Actions
* Docker Hub
* Self-hosted GitHub Actions runner on a Vagrant VM

## Project Structure

```text
backend/
├── .github/
│   └── workflows/
│       └── backend.yml
├── backend/
│   ├── __init__.py
│   ├── app.py
│   └── database.py
├── db-init/
│   └── init.sql
├── tests/
│   └── test_api.py
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Backend API

### GET `/`

Returns a welcome message.

```bash
curl http://localhost:5000/
```

### GET `/api/users`

Returns all users from the MySQL database.

```bash
curl http://localhost:5000/api/users
```

Example response:

```json
[
  {
    "id": 1,
    "name": "Sujan",
    "email": "sujan@example.com"
  },
  {
    "id": 2,
    "name": "Kenny",
    "email": "kenny@example.com"
  }
]
```

### POST `/api/users`

Creates a new user.

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alex","email":"alex@example.com"}'
```

Example response:

```json
{
  "id": 3,
  "name": "Alex",
  "email": "alex@example.com"
}
```

## Database Service

The MySQL database is defined in `docker-compose.yml`.

The database service uses:

* MySQL 8.0
* Database: `assignment11`
* Application user: `appuser`
* Application password: `apppassword`
* Root password: `rootpassword`
* MySQL port: `3306`

The database data is stored in a Docker volume named `mysql_data`.

The `db-init/init.sql` file automatically creates the `users` table and inserts initial sample users when the database is initialized.

## Run Tests Locally

Create and activate a Python virtual environment if required:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the unit tests:

```bash
pytest
```

The tests use mocking, so they do not require a real MySQL database connection.

## Run with Docker Compose

Build and start the application:

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
```

Test the backend:

```bash
curl http://localhost:5000/api/users
```

Stop the services:

```bash
docker compose down
```

## Docker Image

The backend Docker image is published to Docker Hub:

```text
codeykenny/backend-repo
```

The GitHub Actions workflow publishes three image tags:

```text
latest
<commit-sha>
<build-number>
```

## GitHub Actions CI/CD

The backend workflow is located at:

```text
.github/workflows/backend.yml
```

The workflow contains three stages:

### 1. Test

The workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs the Python dependencies.
4. Runs the Pytest test suite.

### 2. Build

After the tests pass, GitHub Actions:

1. Sets up Docker Buildx.
2. Logs in to Docker Hub.
3. Builds the Docker image.
4. Pushes the image to Docker Hub.

The image is published with:

```text
latest
commit SHA
GitHub Actions build number
```

### 3. Deploy

After the build succeeds, the deployment runs on a self-hosted GitHub Actions runner hosted inside a Vagrant VM.

The deployment:

1. Checks out the repository.
2. Logs in to Docker Hub.
3. Pulls the latest Docker image.
4. Starts the backend and MySQL services using Docker Compose.
5. Verifies that the `/api/users` endpoint is available.

The deployment uses:

```text
runs-on: self-hosted
```

## Application Architecture

```text
GitHub Actions
      |
      | Test -> Build -> Deploy
      |
      v
Self-hosted Vagrant Runner
      |
      +-------------------+
      |                   |
      v                   v
Flask Backend          MySQL
   :5000                :3306
```

The backend communicates with MySQL through the Docker Compose network.

## Repository

GitHub repository:

https://github.com/sujanpakhrin/backend-repo

