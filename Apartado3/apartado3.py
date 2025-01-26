import os
import subprocess

def main():
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

    # Definir las variables en función de la versión
    star_color = "red"
    enable_ratings = "true"
    if version == "v1":
        enable_ratings = "false"
    elif version == "v2":
        star_color = "black"

    # Archivo docker-compose.yml
    new_file = "docker-compose.yaml"

    # Verificar si el servicio reviews ya está configurado
    with open(new_file, "r") as file:
        content = file.read()
        if "reviews:" in content:
            print("El servicio 'reviews' ya está configurado en docker-compose.yaml. No se realizarán cambios.")
            return

    # Bloque del servicio reviews
    reviews_service = f"""
  reviews:
    build:
      context: ./practica_creativa2/bookinfo/src/reviews
      dockerfile: Dockerfile_reviews
    environment:
      SERVICE_VERSION: {version}
      ENABLE_RATINGS: "{enable_ratings}"
      STAR_COLOR: {star_color}
    ports:
      - "9084:9080"
    container_name: "reviews-15"
    image: "reviews/15"
    """

    # Añadir el bloque de configuración al archivo existente
    with open(new_file, "a") as file:
        file.write(reviews_service)

    print("Servicio 'reviews' añadido a docker-compose.yaml.")

    # Crear la imagen de Reviews
    os.chdir('practica_creativa2/bookinfo/src/reviews')
    current_dir = os.getcwd()
    subprocess.call(['docker', 'run', '--rm', '-u', 'root', '-v', f'{current_dir}:/home/gradle/project', '-w', '/home/gradle/project', 'gradle:4.8.1', 'gradle', 'clean', 'build'])
    subprocess.call(['docker', 'build', '-t', 'reviews/15', './reviews-wlpcfg'])

    # Construir y levantar los contenedores con docker-compose
    os.chdir('../../../..')  # Volver al directorio raíz del proyecto
    subprocess.call(['docker-compose', 'build'])
    subprocess.call(['docker-compose', 'up', '-d'])

if __name__ == "__main__":
    main()
