from flask import Flask, render_template, request, redirect
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        "postgresql://meeting_data_user:auSOB0tgNP8ikv0Pxbyv7w8daAo1MIsb@dpg-d91o82laeets73fspltg-a.oregon-postgres.render.com/meeting_data",
        sslmode='require'
    )

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS meetings (
        id SERIAL PRIMARY KEY,
        date TEXT UNIQUE,
        mpdv_name TEXT,
        mpdv_start_time TEXT,
        mpdv_end_time TEXT,
        m3_name TEXT,
        m3_start_time TEXT,
        m3_end_time TEXT
    )
    ''')

    dates = [
        "2026-07-01","2026-07-02","2026-07-03",
        "2026-07-06","2026-07-07","2026-07-08",
        "2026-07-09","2026-07-10",
        "2026-07-13","2026-07-14","2026-07-15",
        "2026-07-16","2026-07-17",
        "2026-07-20","2026-07-21","2026-07-22",
        "2026-07-23","2026-07-24",
        "2026-07-27","2026-07-28","2026-07-29",
        "2026-07-30","2026-07-31"
    ]

    for d in dates:
        c.execute(
            "INSERT INTO meetings (date) VALUES (%s) ON CONFLICT (date) DO NOTHING",
            (d,)
        )

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM meetings ORDER BY date")
    rows = c.fetchall()

    data = []
    for row in rows:
        dt = datetime.strptime(row[1], "%Y-%m-%d")
        day = dt.strftime("%a")
        data.append(row + (day,))

    conn.close()
    return render_template('index.html', data=data)

@app.route('/update', methods=['POST'])
def update():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        UPDATE meetings SET
            date=%s,
            mpdv_name=%s,
            mpdv_start_time=%s,
            mpdv_end_time=%s,
            m3_name=%s,
            m3_start_time=%s,
            m3_end_time=%s
        WHERE id=%s
    ''', (
        request.form['date'],
        request.form['mpdv_name'],
        request.form['mpdv_start_time'],
        request.form['mpdv_end_time'],
        request.form['m3_name'],
        request.form['m3_start_time'],
        request.form['m3_end_time'],
        request.form['id']
    ))

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
