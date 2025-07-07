# Ejecución

### Prerrequisitos

- Docker  
- Docker Compose

Este proyecto se encuentra dockerizado, para su ejecución basta con los siguientes comandos:

```bash
# Construir la imagen Docker
docker build -t optimizador-django .

# Levantar el contenedor (recompila si hay cambios)
docker compose up --build
```

Se puede acceder a través de:

http://localhost:8000/



# Optimizador

El optimizador cumple con los requerimientos, es posible tanto cargar el archivo csv como ingresar los parámetros manualmente a través de la página.

# Proyecto

### data_loader.py
    Verifica columnas requeridas, tipos numéricos y valores positivos.

### optimizer.py
    Define la clase Optimizer que modela y resuelve el problema, a través de una sencilla solución utilizando numpy y programación lineal.

### result.py
    Clase ResultsHandler para formatear resultados y generar un gráfico embebido en base64 a partir de gráfico con matplotlib.

### views.py
    Solo la vista index que:

    Recibe CSV o datos manuales.

    Crea el optimizador y obtiene la solución.

    Usa ResultsHandler para preparar contexto y plantilla.

# Pruebas

Actualmente no existen pruebas, si existe un júpiter a través de lo cuál se probaron algunas de las funcionalidades, sin definir casos ni estudiar en mayor profunidad los problemas que podrían surgir.



