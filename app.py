# app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create table if not exists
def init_db():
    conn = sqlite3.connect("queue.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    reason TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("queue.db")
    c = conn.cursor()
    c.execute("SELECT * FROM queue")
    queue = c.fetchall()
    conn.close()
    return render_template("index.html", queue=queue)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    reason = request.form["reason"]
    conn = sqlite3.connect("queue.db")
    c = conn.cursor()
    c.execute("INSERT INTO queue (name, reason) VALUES (?, ?)", (name, reason))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/next")
def next_person():
    conn = sqlite3.connect("queue.db")
    c = conn.cursor()
    c.execute("SELECT * FROM queue ORDER BY id LIMIT 1")
    first = c.fetchone()
    if first:
        c.execute("DELETE FROM queue WHERE id=?", (first[0],))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
