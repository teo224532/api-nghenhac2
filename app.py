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

@app.route('/')
def index():
    # Giao diện cho phép upload file, không yêu cầu mật khẩu ở trang chủ
    return render_template_string("""
        <h1>Upload và Nghe Nhạc</h1>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            Mật khẩu: <input type="password" name="password" required><br><br>
            Chọn file nhạc: <input type="file" name="file" required><br><br>
            <input type="submit" value="Upload">
        </form>
        <h2>Danh sách bài nhạc đã tải lên</h2>
        <ul>
        {% for filename in os.listdir('uploads') %}
            <li><a href="{{ url_for('uploaded_file', filename=filename) }}">{{ filename }}</a></li>
        {% endfor %}
        </ul>
    """)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Kiểm tra mật khẩu khi upload
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
    # Nếu file là nhạc, hiển thị trình phát nhạc
    if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return render_template_string("""
            <h1>Nghe nhạc</h1>
            <audio controls>
                <source src="{{ url_for('uploaded_file', filename=filename) }}" type="audio/mpeg">
                Trình duyệt của bạn không hỗ trợ phát âm thanh.
            </audio>
        """, filename=filename)
    else:
        # Nếu không phải file nhạc, tải xuống
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
