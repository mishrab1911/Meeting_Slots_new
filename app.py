from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ✅ Predefined dates
dates_data = [
    ("01-Jul-26","Wed"),("02-Jul-26","Thu"),("03-Jul-26","Fri"),
    ("06-Jul-26","Mon"),("07-Jul-26","Tue"),("08-Jul-26","Wed"),
    ("09-Jul-26","Thu"),("10-Jul-26","Fri"),
    ("13-Jul-26","Mon"),("14-Jul-26","Tue"),("15-Jul-26","Wed"),
    ("16-Jul-26","Thu"),("17-Jul-26","Fri"),
    ("20-Jul-26","Mon"),("21-Jul-26","Tue"),("22-Jul-26","Wed"),
    ("23-Jul-26","Thu"),("24-Jul-26","Fri"),
    ("27-Jul-26","Mon"),("28-Jul-26","Tue"),("29-Jul-26","Wed"),
    ("30-Jul-26","Thu"),("31-Jul-26","Fri")
]

# ✅ Initialize DB with fixed rows
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS meetings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        day TEXT,
        mpdv_name TEXT,
        mpdv_start_time TEXT,
        mpdv_end_time TEXT,
        m3_name TEXT,
        m3_start_time TEXT,
        m3_end_time TEXT
    )
    ''')

    # Insert dates if not exist
    for date, day in dates_data:
        c.execute("INSERT OR IGNORE INTO meetings (date, day) VALUES (?, ?)", (date, day))

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM meetings ORDER BY id")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

# ✅ UPDATE instead of INSERT
@app.route('/update', methods=['POST'])
def update():
    row_id = request.form['id']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''
        UPDATE meetings SET
            mpdv_name=?,
            mpdv_start_time=?,
            mpdv_end_time=?,
            m3_name=?,
            m3_start_time=?,
            m3_end_time=?
        WHERE id=?
    ''', (
        request.form['mpdv_name'],
        request.form['mpdv_start_time'],
        request.form['mpdv_end_time'],
        request.form['m3_name'],
        request.form['m3_start_time'],
        request.form['m3_end_time'],
        row_id
    ))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
