# Usa una imagen ligera de Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia primero las dependencias para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instala las dependencias sin guardar caché en pip para mantener la imagen liviana
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto (informativo para Docker)
EXPOSE 8000

# Ejecuta Alembic para aplicar migraciones en la BD de Render y luego arranca Uvicorn usando $PORT
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]