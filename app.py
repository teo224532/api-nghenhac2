import psutil
from flask import Flask, request, send_from_directory, redirect, url_for, render_template_string
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Đảm bảo thư mục uploads tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Hàm lấy thông tin server (CPU, bộ nhớ, ổ đĩa)
def get_system_info():
    # Lấy thông tin về CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    # Lấy thông tin về bộ nhớ
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    memory_available = memory.available / (1024 * 1024 * 1024)  # Đổi về GB
    # Lấy thông tin về ổ đĩa
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_free = disk.free / (1024 * 1024 * 1024)  # Đổi về GB

    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory_percent,
        'memory_available': memory_available,
        'disk_percent': disk_percent,
        'disk_free': disk_free
    }

@app.route('/')
def index():
    system_info = get_system_info()  # Lấy thông tin hệ thống
    files = os.listdir('uploads')  # Lấy danh sách các file trong thư mục uploads
    return render_template_string("""
        <h1>Upload và Nghe Nhạc</h1>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            Mật khẩu: <input type="password" name="password" required><br><br>
            Chọn file nhạc: <input type="file" name="file" required><br><br>
            <input type="submit" value="Upload">
        </form>
        
        <h2>Danh sách bài nhạc đã tải lên</h2>
        <ul>
        {% for filename in files %}
            <li><a href="{{ url_for('uploaded_file', filename=filename) }}">{{ filename }}</a></li>
        {% endfor %}
        </ul>

        <h3>Thông tin Server</h3>
        <ul>
            <li>CPU: {{ system_info.cpu_percent }}% sử dụng</li>
            <li>Bộ nhớ: {{ system_info.memory_percent }}% sử dụng (Còn {{ system_info.memory_available }} GB)</li>
            <li>Ổ đĩa: {{ system_info.disk_percent }}% sử dụng (Còn {{ system_info.disk_free }} GB)</li>
        </ul>
    """, system_info=system_info, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    password = request.form.get('password')
    if password != 'titeo123':
        return 'Mật khẩu sai!'

    if 'file' not in request.files:
        return 'Không có file để upload!'
    file = request.files['file']
    if file.filename == '':
        return 'Chưa chọn file!'

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('uploaded_file', filename=file.filename))
    else:
        return 'File không hợp lệ!'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return render_template_string("""
            <h1>Nghe nhạc</h1>
            <audio controls>
                <source src="{{ url_for('uploaded_file', filename=filename) }}" type="audio/mpeg">
                Trình duyệt của bạn không hỗ trợ phát âm thanh.
            </audio>
        """, filename=filename)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
