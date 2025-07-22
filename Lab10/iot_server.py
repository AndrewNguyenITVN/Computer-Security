# iot_server.py
import sqlite3
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('iot_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tempData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        temperature REAL,
        category TEXT
    )
    ''')
    conn.commit()
    conn.close()


@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json 
    timestamp = data.get('timestamp')
    temperature = data.get('temperature')
    category = data.get('category')
    

    conn = sqlite3.connect('iot_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tempData (timestamp, temperature, category) VALUES (?, ?, ?)",
                   (timestamp, temperature, category))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Data stored successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)