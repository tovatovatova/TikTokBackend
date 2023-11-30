from flask import Flask, request, jsonify
import os
from lib.text_handler import speech_to_text 
from flask_cors import CORS

from lib.video_handler import video_to_frames

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers='*')


app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded audios

@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    lang = request.form.get('lang', 'en')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    try:
        # Save the uploaded file file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) # type: ignore
        file.save(file_path)

        transcript_json = speech_to_text(file_path, lang)
        
        frames = video_to_frames(file_path)
        print(frames)
        # Delete the saved audio file after transcription
        os.remove(file_path)

        return transcript_json
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
