# Usa una imagen base ligera de Python
FROM python:3.7.7-slim

# Preparamos el entorno (Instalaciones)
RUN apt-get update && \
    apt-get install -y git && \
    git clone https://github.com/CDPS-ETSIT/practica_creativa2.git && \
    apt-get update && \
    apt-get install -y python3-pip

# Instalamos las dependencias de requirements.txt
RUN sed -i s/^requests==.*/requests/ practica_creativa2/bookinfo/src/productpage/requirements.txt && \
    pip install -r practica_creativa2/bookinfo/src/productpage/requirements.txt

# Expone el puerto 9080 en el contenedor
EXPOSE 9080

# Pasa la variable de entorno GROUP_NUMBER al contenedor
ARG GROUP_NUMBER
ENV GROUP_NUMBER 15

# Cambiamos el título y ejecutamos la aplicación con el script productpage_monolith.py
CMD sed -i "s/{{ product.title }}/{{ product.title }} ${GROUP_NUMBER}/g" practica_creativa2/bookinfo/src/productpage/templates/productpage.html && \
    python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 9080
