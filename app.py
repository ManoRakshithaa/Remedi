from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)
DATABASE = "remedi.db"

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity TEXT NOT NULL,
            unit TEXT NOT NULL,
            dosage TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            taken INTEGER DEFAULT 0,
            taken_date TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = get_db()
    medicines = conn.execute(
        'SELECT * FROM medicines ORDER BY reminder_time'
    ).fetchall()
    streak = conn.execute(
        'SELECT COUNT(*) as count FROM streaks WHERE completed = 1'
    ).fetchone()["count"]
    conn.close()
    return render_template("index.html", medicines=medicines, streak=streak)

@app.route("/add", methods=["GET", "POST"])
def add_medicine():
    if request.method == "POST":
        name = request.form["name"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]
        dosage = request.form.get("dosage", "")
        hour = request.form["hour"].zfill(2)
        minute = request.form["minute"].zfill(2)
        ampm = request.form["ampm"]
        food = request.form.get("food", "")

        if food:
            reminder_time = f"{hour}:{minute} {ampm} | {food}"
        else:
            reminder_time = f"{hour}:{minute} {ampm}"

        conn = get_db()
        conn.execute(
            "INSERT INTO medicines (name, quantity, unit, dosage, reminder_time) VALUES (?, ?, ?, ?, ?)",
            (name, quantity, unit, dosage, reminder_time)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    return render_template("add_medicine.html")

@app.route("/taken/<int:medicine_id>")
def mark_taken(medicine_id):
    today = date.today().isoformat()
    conn = get_db()

    conn.execute(
        "UPDATE medicines SET taken = 1, taken_date = ? WHERE id = ?",
        (today, medicine_id)
    )
    conn.commit()

    total = conn.execute('SELECT COUNT(*) as count FROM medicines').fetchone()["count"]
    taken_today = conn.execute(
        'SELECT COUNT(*) as count FROM medicines WHERE taken = 1'
    ).fetchone()["count"]

    if total > 0 and total == taken_today:
        existing = conn.execute(
            'SELECT * FROM streaks WHERE date = ?', (today,)
        ).fetchone()
        if not existing:
            conn.execute(
                'INSERT INTO streaks (date, completed) VALUES (?, 1)', (today,)
            )
            conn.commit()

    conn.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:medicine_id>")
def delete_medicine(medicine_id):
    conn = get_db()
    conn.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

# This runs init_db always, even on Render via gunicorn
init_db()

if __name__ == "__main__":
    app.run(debug=True)