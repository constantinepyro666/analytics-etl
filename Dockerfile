FROM python:3.11-slim

WORKDIR /app

COPY dashboard /app/dashboard

RUN pip install --no-cache-dir streamlit pandas psycopg2-binary

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8503", "--server.address=0.0.0.0"]
