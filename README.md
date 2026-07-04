# Flask SQL Executor

A lightweight web app built with Flask that lets you connect to a PostgreSQL database, run SQL commands, and upload/read files — all from the browser.

## Features

- DB Connection Status — green badge in the navbar confirms your database is connected
- SQL Query Executor — run any SQL command (CREATE, INSERT, SELECT, UPDATE, DROP, etc.)
- File Upload — drag & drop or browse to upload any text file
- File Reader — click an uploaded file or type its name to view contents in the browser
- File Download — download any uploaded file directly from the viewer

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/im-eraya-san/k8s-app.git
cd k8s-app/app
```

### 2. Configure environment variables

In `docker-compose.yml` at the root of the repo, update the `app` service environment to match your setup:

```yaml
environment:
  - HOST=192.168.1.x        # IP of the machine running PostgreSQL
  - DB_USER=postgres
  - DB_PASSWORD=your_password
  - DB_NAME=your_database
```

### 3. Start the services

```bash
cd k8s-app
docker-compose up -d
```

Then open **http://localhost:5000** in your browser.

## Project Structure

```
k8s-app/
├── LICENSE
├── README.md
├── docker-compose.yml
└── app/
    ├── Dockerfile
    └── data/
        ├── app.py
        └── index.html
```

## Dockerfile

```dockerfile
FROM alpine
RUN mkdir /app
RUN apk add --no-cache python3 py3-pip; pip3 install flask psycopg2-binary python-dotenv --break-system-packages
WORKDIR /app
COPY data/* .
RUN mkdir templates; mv index.html templates/.
EXPOSE 5000
CMD ["python", "app.py"]
```

## Docker Compose

```yaml
services:
  backend:
    container_name: postgres
    image: postgres:14.0
    network_mode: host
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: pg123
      PGDATA: /data/
    volumes:
      - ./data/:/data/
    restart: unless-stopped

  app:
    image: 3raya/sql-web-admin:0.1   # public image — no build needed
    container_name: postgres-admin
    network_mode: host
    restart: always
    environment:
      - HOST=192.168.1.x
      - DB_PASSWORD=pg123
      - DB_USER=postgres
      - DB_NAME=postgres
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the web UI |
| GET | `/api/status` | Check database connection status |
| POST | `/api/execute` | Execute a SQL query |
| POST | `/api/upload` | Upload a file |
| GET | `/api/files` | List all uploaded files |
| GET | `/api/read/<filename>` | Read file contents as text |
| GET | `/api/download/<filename>` | Download a file |

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `HOST` | IP or hostname of the PostgreSQL server | `192.168.1.x` |
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `pg123` |
| `DB_NAME` | Database name to connect to | `postgres` |

## Tech Stack

- **Backend** — Python, Flask, psycopg2
- **Database** — PostgreSQL
- **Frontend** — Vanilla HTML, CSS, JavaScript (no frameworks)
- **Deployment** — Docker, Docker Compose
