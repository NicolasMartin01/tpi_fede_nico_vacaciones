FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py archivos.py constantes.py ./

CMD ["python", "main.py"]
