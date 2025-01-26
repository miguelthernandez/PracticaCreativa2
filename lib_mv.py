#!/usr/bin/python3

import logging, subprocess, os, shutil

log = logging.getLogger('manage-pc2')

# Eliminar todas las imágenes y contenedores Docker
def mv_docker_compose_destroy():
  subprocess.call(['sudo docker stop details-15 productpage-15 ratings-15 reviews-15'], shell=True)
  subprocess.call(['sudo docker rm details-15 productpage-15 ratings-15 reviews-15'], shell=True)
  #subprocess.call(['sudo docker rmi --force $(sudo docker images -q)'], shell=True)

# Despliegue de la aplicación mediante Docker-Compose
def mv_docker_compose():
    # Clonar repositorio de la app
    if not os.path.isdir('practica_creativa2'):
        subprocess.call(["git", "clone", "https://github.com/CDPS-ETSIT/practica_creativa2.git"])
    else:
        print("Repositorio ya clonado")

    # Escoger la versión de la app
    version = input("Escoge una versión (v1, v2, v3): ").strip()
    if version not in ["v1", "v2", "v3"]:
        print("Versión no válida, se elegirá la versión v3 por defecto.")
        version = "v3"
    print(f"Ejecutando la versión {version}")

    # Gestionar el archivo docker-compose.yml
    original_file = "docker-compose-base.yml"
    new_file = "docker-compose.yml"
    if os.path.exists(new_file):
        os.remove(new_file)  # Eliminar si ya existe
    shutil.copy(original_file, new_file)

    # Define las variables en función de la versión
    star_color = "red"
    enable_ratings = "true"
    if version == "v1":
        enable_ratings = "false"
    elif version == "v2":
        star_color = "black"

    # Añadir el servicio de reviews al docker-compose
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

    # Crear la imagen de Reviews
    os.chdir('practica_creativa2/bookinfo/src/reviews')
    dir = os.getcwd()
    subprocess.call(['docker', 'run', '--rm', '-u', 'root', '-v', f'{dir}:/home/gradle/project', '-w', '/home/gradle/project', 'gradle:4.8.1', 'gradle', 'clean', 'build'])
    subprocess.call(['docker', 'build', '-t', 'reviews/15', './reviews-wlpcfg'])

    # Eliminar contenedores existentes para evitar conflictos
    subprocess.call(['docker', 'compose', 'down'], shell=True)

    # Construir y levantar los contenedores con docker-compose
    subprocess.call(['docker-compose', 'build'])
    subprocess.call(['docker-compose', 'up', '-d'])
