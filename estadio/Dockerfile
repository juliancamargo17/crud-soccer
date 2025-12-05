# Dockerfile para el microservicio de Equipos
FROM python:3.12

# Establecer directorio de trabajo
WORKDIR /code

# Copiar archivos de requirements
COPY /estadio/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY /estadio/app ./app

# Copiar los modelos y database desde el directorio raíz del proyecto
COPY /models ./models
COPY /database ./database

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

