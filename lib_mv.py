#!/usr/bin/python3



import logging, subprocess, os, shutil

log = logging.getLogger('auto_p2')

# Despliegue de la aplicación en máquina virtual pesada
def mv_pesada (puerto):
  log.debug("mv_pesada ")
  subprocess.call(['git', 'clone', 'https://github.com/CDPS-ETSIT/practica_creativa2.git'])
  subprocess.run(['find', './', '-type', 'f', '-exec', 'sed', '-i', f's/Simple Bookstore App/GRUPO15/g', '{{}}', '\;'])
  os.chdir('practica_creativa2/bookinfo/src/productpage')
  subprocess.call(["sed", "-i", "s/^requests==.*/requests/", "requirements.txt"])
  subprocess.call(['pip3', 'install', '-r', 'requirements.txt'])
  subprocess.call(['sudo', 'apt', 'upgrade', 'requests'])
  subprocess.call(['python3', 'productpage_monolith.py', f'{puerto}'])

# Despliegue de la aplicación mediante Docker
def mv_docker ():
  log.debug("mv_docker ")
  subprocess.call(['sudo', 'docker', 'build', '-t', 'product-page/g15', '.'])
  subprocess.call(['sudo', 'docker', 'run', '--name', 'product-page-g15', '-p', '9080:5080', '-e', 'GROUP_NUM=15', '-d', 'product-page/g15'])

# Eliminar todas las imágenes y contenedores Docker
def docker_destroy():
  subprocess.call(['sudo docker stop product-page-g15'], shell=True)
  subprocess.call(['sudo docker rm product-page-g15'], shell=True)
  #subprocess.call(['sudo docker rmi --force $(sudo docker images -q)'], shell=True)

# Despliegue de la aplicación mediante Docker-Compose
def mv_docker_compose ():
   # Clonar repositorio de la app
    if not os.path.isdir('practica_creativa2'):
        subprocess.call(["git", "clone", "https://github.com/CDPS-ETSIT/practica_creativa2.git"])
    else:
        print("Repositorio ya clonado")
    # Escoger la version de la app
    version = input("Escoge una versión (v1, v2, v3): ").strip()
    if version not in ["v1", "v2", "v3"]:
        print("Versión no válida, se elegirá la versión v3 por defecto.")
        version = "v3"
    print(f"Ejecutando la versión {version}")
    # Crea un nuevo docker-compose a partir del base
    original_file = "docker-compose-base.yml"
    new_file = f"docker-compose.yml"
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
    container_name: \"reviews-15\"
    image: \"reviews/15\"
    """
    with open(new_file, "a") as file:
        file.write(reviews_service)

    # Crear la imagen de Reviews, ejecutando antes el comando requerido
    os.chdir('practica_creativa2/bookinfo/src/reviews')
    dir = os.getcwd()
    subprocess.call(['docker', 'run', '--rm', '-u', 'root', '-v', f'{dir}:/home/gradle/project', '-w', '/home/gradle/project', 'gradle:4.8.1', 'gradle', 'clean', 'build'])
    subprocess.call(['docker', 'build', '-t', 'reviews/15', './reviews-wlpcfg'])

    # Construir y levantar los contenedores con docker-compose
    subprocess.call([f'docker-compose', 'build'])
    subprocess.call([f'docker-compose', 'up', '-d'])

def config_cluster(cluster):
  # Configurar el cluster
  subprocess.call(['gcloud', 'container', 'clusters', 'resize', f'{cluster}', '--num-nodes=5', '--zone=europe-southwest1'])
  subprocess.call(['gcloud', 'container', 'clusters', 'update', f'{cluster}', '--no-enable-autoscaling', '--zone=europe-southwest1'])
  subprocess.call(['gcloud', 'auth', 'configure-docker', '-q'])

def mv_kubernetes(version):
  log.debug("mv_kubernetes ")
  # Desplegar el escenario
  subprocess.call(['kubectl', 'apply', '-f', f'./deployment-{version}.yaml'])
  # Mostrar información de los pods y los services
  subprocess.call(['kubectl', 'get', 'pods'])
  subprocess.call(['kubectl', 'get', 'services'])

def destroy_cluster():
  # Destruir el escenario de la parte 4
  subprocess.call(['kubectl', 'delete', '--all', 'pods'])
  subprocess.call(['kubectl', 'delete', '--all', 'deployments'])
  subprocess.call(['kubectl', 'delete', '--all', 'services'])

def info_cluster():
  # Mostrar información de los pods y los services
  subprocess.call(['kubectl', 'get', 'pods'])
  subprocess.call(['kubectl', 'get', 'services'])