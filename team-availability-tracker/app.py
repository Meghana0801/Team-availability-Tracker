from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT,
            available INTEGER
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        users = [
            (1, "Rahul", 1),
            (2, "Priya", 0),
            (3, "Arjun", 1)
        ]

        cursor.executemany(
            "INSERT INTO users VALUES (?, ?, ?)",
            users
        )

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/users')
def get_users():

    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return jsonify([
        {
            "id": u[0],
            "name": u[1],
            "available": bool(u[2])
        }
        for u in users
    ])

@app.route('/toggle/<int:id>', methods=['POST'])
def toggle(id):

    conn = sqlite3.connect('team.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET available = NOT available WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Updated"})

if __name__ == '__main__':
    app.run(debug=True)