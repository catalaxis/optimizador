# Usamos una imagen oficial de Python
FROM python:3.10

# Establecer el directorio de trabajo
RUN mkdir /app
RUN chmod -R a+rX /app

# Set the working directory inside the container
WORKDIR /app

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN chmod -R a+rX /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos al contenedor
COPY . /app/

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
