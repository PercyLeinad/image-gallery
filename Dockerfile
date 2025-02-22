FROM python:3.9-slim-buster

WORKDIR /app

# Install system dependencies
RUN apt update && apt install -y nano && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY frontend /app/frontend/
COPY backend /app/backend/
COPY start.sh /app/

# Ensure start.sh is executable
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
