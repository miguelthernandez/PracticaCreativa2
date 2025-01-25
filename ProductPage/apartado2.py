#!usr/bin/python3
from subprocess import call
import os

# Instalamos Docker
call(['sudo', 'apt-get', 'update'])
call(['sudo', 'apt-get', 'upgrate'])
call(['sudo', 'apt-get', 'install', '-y', 'docker.io'])
call(['sudo', 'apt-get', 'install', '-y', 'docker-compose'])

# Eliminamos el contenedor y la imagen si lo hubiera 
#os.system('sudo docker stop 10-product-page')
#os.system('sudo docker rm 10-product-page')
#os.system('sudo docker rmi 10/product-page')

#Crea la imagen con nombre 10/product-page
call(['sudo','docker', 'build', '-t', 'product-page/g15', '.'])

#Inicia un contenedor llamado "g10-product-page" a partir de la imagen "10/product-page"
os.system('sudo docker run --name product-page-g15 -p 5080:5080 -e GRUPO_NUMERO=15 -d product-page/g15')