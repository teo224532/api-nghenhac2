import os
import psutil
from flask import Flask, request, send_from_directory, redirect, url_for, render_template, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac'}
PASSWORD = 'titeo123'  # Đổi mật khẩu
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Đảm bảo thư mục uploads tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Kiểm tra file hợp lệ
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Lấy thông tin hệ thống (CPU, RAM, Disk)
def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    memory_available = memory.available / (1024 * 1024 * 1024)
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_free = disk.free / (1024 * 1024 * 1024)

    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory_percent,
        'memory_available': memory_available,
        'disk_percent': disk_percent,
        'disk_free': disk_free,
    }

@app.route('/')
def index():
    system_info = get_system_info()
    files = os.listdir(UPLOAD_FOLDER)  # Danh sách file đã upload
    return render_template('index.html', system_info=system_info, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Kiểm tra mật khẩu
    password = request.form.get('password')
    if password != PASSWORD:
        return jsonify({'status': 'error', 'message': 'Sai mật khẩu!'}), 403

    # Kiểm tra file upload
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'Không tìm thấy file!'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'File trống!'}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({'status': 'success', 'message': 'Upload thành công!', 'filename': file.filename}), 200

    return jsonify({'status': 'error', 'message': 'File không hợp lệ!'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
