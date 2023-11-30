from flask import Flask, request, jsonify
import os
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers='*')

API_KEY = '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'
client = OpenAI(api_key=API_KEY)

app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded audios

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    try:
        # Save the uploaded file file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Open the uploaded file and pass it to the OpenAI client for transcription
        with open(file_path, 'rb') as uploaded_file:
            transcript = client.audio.transcriptions.create(file=uploaded_file, model='whisper-1', language='he')

        # Delete the saved audio file after transcription
        os.remove(file_path)

        return transcript.model_dump_json()
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
