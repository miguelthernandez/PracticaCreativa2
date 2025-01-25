FROM python:3.7.7-slim

# Indicar el puerto accesible
EXPOSE 5080

#Indicar la variable de entorno GROUP_NUMBER
ENV GROUP_NUMBER=15

# Cambiar directorio al de home
WORKDIR /home

# Ejecutar comandos de instalación
RUN apt-get update -y \
        && apt-get install -y python3-pip \
        && apt-get install -y git \
        && git clone https://github.com/CDPS-ETSIT/practica_creativa2.git \
        && cd practica_creativa2/bookinfo/src/productpage/ \
        && sed -i s/^requests==.*/requests/ requirements.txt \
        && pip3 install -r requirements.txt

# Cambiar el título de la app y lanzar app en el puerto 5080
CMD find ./ -type f -exec sed -i "s/Simple Bookstore App/GRUPO$GROUP_NUMBER/g" {} \; \
    && python3 practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 5080

# Indicar que se ha instalado correctamente
RUN echo "La imagen Docker de PRODUCT PAGE se ha instalado correctamente"
