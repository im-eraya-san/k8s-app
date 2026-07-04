# Flask SQL Executor

A lightweight web app built with Flask that lets you connect to a SQLite database, run SQL commands, and upload/read files — all from the browser.

## Features

- DB Connection Status — green badge in the navbar confirms your database is connected
- SQL Query Executor — run any SQL command (CREATE, INSERT, SELECT, UPDATE, DROP, etc.)
- File Upload — drag & drop or browse to upload any text file
- File Reader — click an uploaded file or type its name to view contents in the browser
- File Download — download any uploaded file directly from the viewer

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/flask-sql-executor.git
cd flask-sql-executor
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Project Structure

```
flask_app/
├── app.py                  # Flask backend — routes & DB logic
├── requirements.txt        # Python dependencies
├── uploads/                # Uploaded files saved here (auto-created)
└── templates/
    └── index.html          # Frontend UI
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

## Switching Databases

By default the app uses **SQLite** (a `database.db` file is auto-created). To use PostgreSQL or MySQL, swap out `get_db()` in `app.py`:

### PostgreSQL

```bash
pip install psycopg2-binary
```
```python
import psycopg2
def get_db():
    return psycopg2.connect("postgresql://user:password@localhost/dbname")
```

### MySQL

```bash
pip install pymysql
```
```python
import pymysql
def get_db():
    return pymysql.connect(host='localhost', user='root', password='', database='mydb')
```

## Tech Stack

- **Backend** — Python, Flask
- **Database** — SQLite (swappable)
- **Frontend** — Vanilla HTML, CSS, JavaScript (no frameworks)

## License

MIT — feel free to use and modify.
