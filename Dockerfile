# Base image có Python và Chromium
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir pandas openpyxl

# Tạo thư mục làm việc trong container
WORKDIR /app

# Copy file script Python và Excel vào container
COPY check.py .          # <- tên file Python
COPY check.xlsx .               # <- file Excel input

# Mặc định chạy script khi container khởi động
CMD ["python", "check.py"]
