# Usa una imagen base con Python
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto al iniciar el contenedor
CMD ["python", "src/main.py"]
