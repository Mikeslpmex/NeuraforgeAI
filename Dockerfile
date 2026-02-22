FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Exponer el puerto que Google Cloud Run exige
EXPOSE 8080
# Ejecutar el monetizador
CMD ["python", "monetizador.py"]
