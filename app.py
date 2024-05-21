from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        question = request.form['question']
        response = ollama.chat(model='nous-hermes2', messages=[{'role': 'user', 'content': question}])
        answer = response['message']['content']
        return jsonify({'answer': answer})

if __name__ == '__main__':
        app.run(debug=True)
