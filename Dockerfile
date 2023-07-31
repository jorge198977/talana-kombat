# Usa la imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor (este Dockerfile debe ubicarse en el mismo directorio que main.py)
COPY main.py data.json /app/

# Instala las dependencias del proyecto (si tienes algún archivo de requerimientos, cámbialo aquí)
# RUN pip install <tus_dependencias>

# Ejecuta el script principal cuando el contenedor se inicie
CMD ["python", "main.py"]
