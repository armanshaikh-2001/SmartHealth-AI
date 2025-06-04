import sqlite3
from datetime import datetime

DB_NAME = 'health.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS health_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                gender TEXT,
                blood_group TEXT,
                ethnicity TEXT,
                symptoms TEXT,
                body_parts TEXT,
                description TEXT,
                conditions TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()

def save_user_data(user_input, conditions):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO health_data (
                name, email, phone, gender, blood_group, ethnicity,
                symptoms, body_parts, description, conditions, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_input.get('name'),
            user_input.get('email'),
            user_input.get('phone'),
            user_input.get('gender'),
            user_input.get('bloodGroup'),
            user_input.get('ethnicity'),
            ','.join(user_input.get('symptoms', [])),
            ','.join(user_input.get('body_parts', [])),
            user_input.get('description'),
            ','.join([c['name'] for c in conditions]),
            datetime.now().isoformat()
        ))
        conn.commit()

def fetch_all_data():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM health_data')
        return c.fetchall()

# Initialize DB when module is imported
init_db()
