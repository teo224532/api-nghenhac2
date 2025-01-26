# Sử dụng hình ảnh cơ bản
FROM python:3.8-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Cài đặt các công cụ cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /usr/share/doc/* /usr/share/man/* /tmp/*

# Cài đặt gdown để tải file từ Google Drive
RUN pip install --no-cache-dir gdown

# Tạo thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements và cài đặt thư viện
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn ứng dụng vào container
COPY . /app/

# Tạo thư mục uploads
RUN mkdir -p uploads && chmod -R 755 uploads

# Tải file Google Drive vào thư mục uploads trực tiếp
RUN gdown --folder --id 14RPTFfwQBsWPr9XeCaBfi9zZtwiVe9VV -O uploads && \
    find uploads -type f -name '*.tmp' -delete

# Xóa file không cần thiết để giảm dung lượng
RUN rm -rf /temp_downloads && \
    apt-get remove -y build-essential gcc libffi-dev wget && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Mở cổng 8000
EXPOSE 8000

# Lệnh chạy ứng dụng
CMD ["python", "app.py"]
