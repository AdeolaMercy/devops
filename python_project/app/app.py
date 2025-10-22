from flask import Flask
import os
import psycopg2

app = Flask(__name__)

@app.route("/")
def home():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "postgres"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASS", "postgres")
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    cur.close()
    conn.close()

    return f"Hello from Flask + PostgreSQL!<br>Database version: {version}"

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=5000, debug=False)
