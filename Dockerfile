# Sử dụng hình ảnh cơ bản của Python
FROM python:3.8-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cài đặt các công cụ cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt gdown để tải file từ Google Drive
RUN pip install --no-cache-dir gdown

# Tạo thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements vào container
COPY requirements.txt /app/

# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng vào container
COPY . /app/

# Đảm bảo thư mục uploads tồn tại và cấp quyền đầy đủ
RUN mkdir -p uploads && chmod -R 755 uploads

# Tải tất cả các file trong thư mục Google Drive về container
RUN gdown --folder --id 13QwarexfsSkSvyG_LPk9hVmQeptApzuN -O /temp_downloads

# Chuyển toàn bộ file đã tải về vào thư mục uploads
RUN mv /temp_downloads/* uploads/

# Xóa thư mục tạm
RUN rm -rf /temp_downloads

# Mở cổng 8000
EXPOSE 8000

# Lệnh chạy ứng dụng
CMD ["python", "app.py"]
