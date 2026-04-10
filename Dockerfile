FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    DASHBOARD_DATA_SOURCE=auto

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data ./data

EXPOSE 8080

CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8080", "--server.address=0.0.0.0"]
