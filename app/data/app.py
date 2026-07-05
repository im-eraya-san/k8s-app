from flask import Flask, render_template, request, jsonify, send_from_directory
import psycopg2
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    return psycopg2.connect(
        host=os.environ['HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        dbname=os.environ['DB_NAME']
    )


@app.route("/")
def index():
    return render_template("index.html")


# ── Machine info ───────────────────────────────────────────
@app.route("/api/info")
def info():
    import socket
    return jsonify({
        "hostname": socket.gethostname(),
        "db_host": os.environ.get("HOST", "N/A")
    })


# ── DB status ─────────────────────────────────────────────
@app.route("/api/status")
def db_status():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        conn.close()
        return jsonify({"connected": True})
    except Exception as e:
        return jsonify({"connected": False, "error": str(e)})


# ── SQL execute ────────────────────────────────────────────
@app.route("/api/execute", methods=["POST"])
def execute_sql():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"success": False, "error": "No query provided"}), 400

    # Statements that must run outside a transaction block
    AUTOCOMMIT_KEYWORDS = ("CREATE DATABASE", "DROP DATABASE", "CREATE TABLESPACE", "DROP TABLESPACE")

    conn = get_db()

    try:
        statements = [s.strip() for s in query.split(";") if s.strip()]
        last_result = None

        for stmt in statements:
            needs_autocommit = stmt.upper().startswith(AUTOCOMMIT_KEYWORDS)

            if needs_autocommit:
                conn.autocommit = True
            else:
                conn.autocommit = False

            cursor = conn.cursor()
            cursor.execute(stmt)

            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                last_result = {"columns": columns, "rows": rows, "rowcount": len(rows)}
            else:
                if not needs_autocommit:
                    conn.commit()
                last_result = {
                    "columns": [], "rows": [], "rowcount": cursor.rowcount,
                    "message": f"Query OK — {cursor.rowcount} row(s) affected"
                }

        return jsonify({"success": True, "result": last_result})

    except Exception as e:
        if not conn.autocommit:
            conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 400

    finally:
        conn.close()


# ── Upload file ────────────────────────────────────────────
@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file part in request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    size = os.path.getsize(save_path)

    return jsonify({"success": True, "filename": filename, "size": size})


# ── List uploaded files ────────────────────────────────────
@app.route("/api/files")
def list_files():
    files = []
    for f in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, f)
        files.append({"name": f, "size": os.path.getsize(path)})
    files.sort(key=lambda x: x["name"])
    return jsonify({"files": files})


# ── Read file contents ─────────────────────────────────────
@app.route("/api/read/<filename>")
def read_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(path):
        return jsonify({"success": False, "error": f"File '{filename}' not found"}), 404

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return jsonify({"success": True, "filename": filename, "content": content})
    except UnicodeDecodeError:
        return jsonify({"success": False, "error": "File is binary and cannot be displayed as text"}), 400


# ── Download file ──────────────────────────────────────────
@app.route("/api/download/<filename>")
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
