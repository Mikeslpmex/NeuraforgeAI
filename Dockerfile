# Imagen base ligera
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .

# Actualizar pip y limpiar caché
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto que Render usa por defecto
EXPOSE 10000

# Comando de inicio
CMD ["python", "main_prod.py"]