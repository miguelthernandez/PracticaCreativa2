#!/usr/bin/python3

import logging, subprocess, os, shutil

# Configuración del logger para el script
log = logging.getLogger('manage-pc2')

# Función para eliminar todas las imágenes y contenedores Docker
def mv_docker_compose_destroy():
    # Detener los contenedores especificados
    subprocess.call(['sudo docker stop details-15 productpage-15 ratings-15 reviews-15'], shell=True)
    # Eliminar los contenedores detenidos
    subprocess.call(['sudo docker rm details-15 productpage-15 ratings-15 reviews-15'], shell=True)
    # Eliminar todas las imágenes de Docker (comentado para evitar eliminación accidental)
    # subprocess.call(['sudo docker rmi --force $(sudo docker images -q)'], shell=True)

# Función para desplegar la aplicación mediante Docker-Compose
def mv_docker_compose():
    # Clonar el repositorio de la aplicación si no está presente
    if not os.path.isdir('practica_creativa2'):
        subprocess.call(["git", "clone", "https://github.com/CDPS-ETSIT/practica_creativa2.git"])
    else:
        print("Repositorio ya clonado")

    # Solicitar al usuario que elija una versión de la aplicación
    version = input("Escoge una versión (v1, v2, v3): ").strip()
    # Validar la versión seleccionada, y si es inválida, elegir v3 por defecto
    if version not in ["v1", "v2", "v3"]:
        print("Versión no válida, se elegirá la versión v3 por defecto.")
        version = "v3"
    print(f"Ejecutando la versión {version}")

    # Gestionar el archivo docker-compose.yml (copiar y preparar el archivo)
    original_file = "docker-compose-base.yml"
    new_file = "docker-compose.yml"
    if os.path.exists(new_file):
        os.remove(new_file)  # Eliminar el archivo existente si lo hay
    shutil.copy(original_file, new_file)

    # Definir las variables necesarias según la versión seleccionada
    star_color = "red"
    enable_ratings = "true"
    if version == "v1":
        enable_ratings = "false"
    elif version == "v2":
        star_color = "black"

    # Añadir el servicio de "reviews" al archivo docker-compose
    reviews_service = f"""
  reviews:
    environment:
        SERVICE_VERSION: {version}
        ENABLE_RATINGS: "{enable_ratings}"
        STAR_COLOR: {star_color}
    container_name: "reviews-15"
    image: "reviews/15"
    """
    with open(new_file, "a") as file:
        file.write(reviews_service)

    # Crear la imagen de "reviews" mediante Gradle
    os.chdir('practica_creativa2/bookinfo/src/reviews')
    dir = os.getcwd()
    subprocess.call(['docker', 'run', '--rm', '-u', 'root', '-v', f'{dir}:/home/gradle/project', '-w', '/home/gradle/project', 'gradle:4.8.1', 'gradle', 'clean', 'build'])
    subprocess.call(['docker', 'build', '-t', 'reviews/15', './reviews-wlpcfg'])

    # Eliminar cualquier contenedor existente para evitar conflictos al desplegar
    subprocess.call(['docker', 'compose', 'down'], shell=True)

    # Construir y levantar los contenedores con Docker Compose
    subprocess.call(['docker-compose', 'build'])
    subprocess.call(['docker-compose', 'up', '-d'])
