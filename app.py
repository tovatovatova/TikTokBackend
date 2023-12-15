import os
from dataclasses import asdict

from flask import Flask, jsonify, request
from flask_cors import CORS

from lib.main_handler import get_final_results
from lib.user_config import UserConfig

app = Flask(__name__)
CORS(
    app, resources={r"/*": {"origins": "*"}}, supports_credentials=True,
    allow_headers='*'
)





UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded audios


@app.route('/upload', methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    lang = request.form.get('lang', 'en')[:2].lower()
    platform = 'tiktok'
    user_config = UserConfig(lang=lang, platform=platform)

    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    assert file.filename is not None

    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        results = get_final_results(file_path, user_config)

        # Delete the saved audio file after transcription
        os.remove(file_path)
        results_dicts = [asdict(section) for section in results]
        return jsonify(results_dicts)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
