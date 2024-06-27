import sqlite3
import html

def clean_text(text):
    # Convert HTML entities to text
    text = html.unescape(text)
    # Additional cleaning can be done here if necessary
    return text

# Connect to the SQLite database
conn = sqlite3.connect('TriviaData.db')
cursor = conn.cursor()

# Retrieve all questions from the database
cursor.execute("SELECT question_id, question FROM questions")
rows = cursor.fetchall()

# Update each row
for row in rows:
    cleaned_question = clean_text(row[1])
    # Update the question in the database
    cursor.execute("UPDATE questions SET question = ? WHERE question_id = ?", (cleaned_question, row[0]))

# Commit the changes and close the connection
conn.commit()
conn.close()
