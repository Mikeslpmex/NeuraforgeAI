# Imagen base ligera con Python 3.11
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV=production

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt /app/

# Instalar dependencias del sistema y Python
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean

# Copiar el código fuente
COPY . /app/

# Exponer el puerto de la aplicación
EXPOSE 8000

# Comando de arranque con Gunicorn (4 workers)
CMD ["gunicorn", "main:app", "--workers", "4", "--bind", "0.0.0.0:8000", "--timeout", "120"]

# Firma del equipo
# Equipo NeuraforgeAI & AI colaborativa
