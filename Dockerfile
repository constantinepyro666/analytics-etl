FROM python:3.11-slim

WORKDIR /app

# ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем проект
COPY . .

CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8503", "--server.address=0.0.0.0"]
