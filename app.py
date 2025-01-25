from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    """API để upload file"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return jsonify({"message": "File uploaded successfully", "file": file.filename}), 200

@app.route('/files', methods=['GET'])
def list_files():
    """API để liệt kê tất cả file nhạc"""
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    music_files = [f for f in files if f.endswith(('.mp3', '.wav'))]
    return jsonify(music_files)

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    """API để tải file nhạc"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
