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

# Expone el puerto en el que corre FastAPI/Uvicorn
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]