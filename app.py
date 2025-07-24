from flask import Flask, request, jsonify, render_template, session
from werkzeug.utils import secure_filename
import os

from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, OPENROUTER_API_KEY, WHISPER_API_URL, LLM_API_URL, LLM_MODEL
from rag_utils import process_document, query_llm, transcribe_audio

app = Flask(__name__)
app.secret_key = 'rag_secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload document
@app.route('/upload', methods=['POST'])
def upload_doc():
    file = request.files.get('file')
    if file and file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        text = process_document(path)
        session['doc_text'] = text
        return render_template('chat.html')  # Or redirect as needed
    return 'Invalid file', 400

# Upload voice (audio) file
@app.route('/voice', methods=['POST'])
def upload_voice():
    audio = request.files.get('audio')
    if audio:
        filename = secure_filename(audio.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio.save(path)
        transcript = transcribe_audio(path)
        # You may want to store/transmit the transcript to front end or session
        return jsonify({'transcript': transcript})
    return jsonify({'error': 'No audio file provided'}), 400

# Handle chat query/question
@app.route('/chat', methods=['POST'])
def chat_post():
    question = request.form.get('query')
    doc_text = session.get("doc_text", "")
    answer = query_llm(doc_text, question)
    return render_template('chat.html', answer=answer)  # Adjust for your template

# (Optional) If you have API endpoints for JS fetch calls, keep them as well
@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json()
    question = data.get('question')
    doc_text = session.get("doc_text", "")
    answer = query_llm(doc_text, question)
    return jsonify({'answer': answer})

@app.route('/api/transcribe', methods=['POST'])
def api_transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    audio = request.files['audio']
    filename = secure_filename(audio.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio.save(path)
    transcript = transcribe_audio(path)
    return jsonify({'transcript': transcript})
@app.route('/health')
def health_check():
    return "OK", 200


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
