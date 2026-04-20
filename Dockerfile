FROM python:3.11-slim

WORKDIR /app
ENV PIP_NO_CACHE_DIR=1
COPY . .

# ускоряем установку
RUN pip install --no-cache-dir \
    pandas \
    streamlit \
    psycopg2-binary

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8503", "--server.address=0.0.0.0"]
