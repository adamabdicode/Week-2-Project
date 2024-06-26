import json
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('trivia.db')
cursor = conn.cursor()

# Create the questions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    difficulty TEXT,
    question TEXT
);
''')

# Load JSON data from file
with open('data.json', 'r') as file:
    data = json.load(file)

# Insert data into the database
for entry in data:
    for item in entry['results']:
        cursor.execute('''
        INSERT INTO questions (difficulty, question)
        VALUES (?, ?)
        ''', (item['difficulty'], item['question']))

# Commit changes and close the connection
conn.commit()
conn.close()
