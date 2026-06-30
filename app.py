from flask import Flask, render_template, request, redirect
import psycopg2
from datetime import datetime

app = Flask(__name__)

# ✅ DB Connection
def get_connection():
    return psycopg2.connect(
        "postgresql://meeting_data_new_user:97putwxf15IhBoo1SJnRGT7M2FunFgFb@dpg-d91p0j8js32c739q9vh0-a.oregon-postgres.render.com/meeting_data_new",
        sslmode='require'
    )

# ✅ Create table (NO predefined rows)
def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS meetings (
        id SERIAL PRIMARY KEY,
        date TEXT,
        mpdv_name TEXT,
        mpdv_start_time TEXT,
        mpdv_end_time TEXT,
        m3_name TEXT,
        m3_start_time TEXT,
        m3_end_time TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()

# ✅ Home
@app.route('/')
def index():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM meetings ORDER BY date")
    rows = c.fetchall()

    data = []
    for row in rows:
        try:
            dt = datetime.strptime(row[1], "%Y-%m-%d")
            day = dt.strftime("%a")
        except:
            day = ""
        data.append(row + (day,))

    conn.close()
    return render_template('index.html', data=data)

# ✅ Add new row (user selects date)
@app.route('/add', methods=['POST'])
def add():
    date_val = request.form['date']

    if not date_val:
        return redirect('/')

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "INSERT INTO meetings (date) VALUES (%s)",
        (date_val,)
    )

    conn.commit()
    conn.close()
    return redirect('/')

# ✅ Update row
@app.route('/update', methods=['POST'])
def update():
    if not request.form['date']:
        return redirect('/')

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
