# Usar imagen oficial ligera de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (bash, curl, git si fueran necesarios)
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad (Best Practice en GCP)
RUN useradd -m -u 1000 neuraforge
USER neuraforge

# Copiar solo el archivo de dependencias primero (para aprovechar caché)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código (respetando .dockerignore)
COPY . .

# Dar permisos de ejecución a los scripts .sh
RUN chmod +x *.sh

# Variables de entorno por defecto
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Puerto que usa Cloud Run
EXPOSE 8080

# Comando de entrada (Ajusta esto según tu script principal)
# Opción A: Si es un servidor web (FastAPI/Flask)
# CMD ["python", "core_estructure.py"]

# Opción B: Si es un script que se ejecuta y termina (Task)
# Para Cloud Run Jobs o Cron, se puede sobreescribir al desplegar
CMD ["python", "core_estructure.py"]
