from flask import Flask, render_template, request, jsonify
import sqlite3
import ollama

app = Flask(__name__, static_folder='static')

def init_db():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        question = request.form['question']
        response = ollama.chat(model='GEITje-7B-chat-v2', messages=[{'role': 'user', 'content': question}])
        answer = response['message']['content']
        return jsonify({'answer': answer})

@app.route('/notes', methods=['POST'])
def add_note():
    content = request.form['content']
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'}), 201

@app.route('/notes', methods=['GET'])
def get_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes')
    notes = cursor.fetchall()
    conn.close()
    return jsonify({'notes': notes})

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
