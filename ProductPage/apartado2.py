#!usr/bin/python3
from subprocess import call
import os

# Instalamos Docker
call(['sudo', 'apt-get', 'update'])
call(['sudo', 'apt-get', 'upgrate'])
call(['sudo', 'apt-get', 'install', '-y', 'docker.io'])
call(['sudo', 'apt-get', 'install', '-y', 'docker-compose'])

# Eliminamos el contenedor y la imagen si lo hubiera 
os.system('sudo docker stop product-page-g15')
os.system('sudo docker rm product-page-g15')
os.system('sudo docker rmi product-page/g15')

#Crea la imagen con nombre 10/product-page
call(['sudo','docker', 'build', '-t', 'product-page/g15', '.'])

#Inicia un contenedor llamado "g10-product-page" a partir de la imagen "10/product-page"
os.system('sudo docker run --name product-page-g15 -p 9080:5080 -e GRUPO_NUMERO=10 -d 10/product-page')
