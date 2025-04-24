from flask import Flask, render_template, request, jsonify
from datetime import datetime
import sqlite3
import ollama
import textstat
import time
import json

app = Flask(__name__, static_folder='static')

def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    # Ensure notes table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY,
                        content TEXT,
                        date TEXT)''')

    # Ensure evaluations table exists (legacy schema may have self_score)
    cursor.execute('''CREATE TABLE IF NOT EXISTS evaluations (
                        id INTEGER PRIMARY KEY,
                        question TEXT,
                        answer TEXT,
                        metrics TEXT,
                        date TEXT)''')
    # Add metrics column if missing
    cursor.execute("PRAGMA table_info(evaluations)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'metrics' not in cols:
        cursor.execute('ALTER TABLE evaluations ADD COLUMN metrics TEXT')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.form['question']
    model = 'bramvanroy/fietje-2b-chat:f16'

    # Generate answer and measure response time
    start_time = time.time()
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': question}]
    )
    elapsed = time.time() - start_time
    answer = response['message']['content']

    # Compute readability and complexity metrics
    readability = textstat.flesch_reading_ease(answer)
    tokens = answer.split()
    token_count = len(tokens)
    lexical_diversity = len(set(tokens)) / token_count if token_count > 0 else 0

    # Bundle metrics into JSON
    metrics = {
        'readability': readability,
        'response_time_s': elapsed,
        'token_count': token_count,
        'lexical_diversity': lexical_diversity
    }

    # Log evaluation in DB
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO evaluations (question, answer, metrics, date) VALUES (?, ?, ?, ?)',
        (question, answer, json.dumps(metrics), timestamp)
    )
    conn.commit()
    conn.close()

    return jsonify({
        'answer': answer,
        'metrics': metrics
    })

@app.route('/notes', methods=['POST'])
def add_note():
    content = request.form['content']
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (content, date) VALUES (?, ?)', (content, date))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 201

@app.route('/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, content, date FROM notes')
    notes = cursor.fetchall()
    conn.close()
    return jsonify({'notes': notes})

@app.route('/evaluations', methods=['GET'])
def get_evaluations():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, question, answer, metrics, date FROM evaluations')
    rows = cursor.fetchall()
    conn.close()
    # parse metrics JSON
    evals = []
    for _id, q, a, m, d in rows:
        data = {'id': _id, 'question': q, 'answer': a, 'date': d}
        if m:
            try:
                data['metrics'] = json.loads(m)
            except json.JSONDecodeError:
                data['metrics'] = {}
        evals.append(data)
    return jsonify({'evaluations': evals})

@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
