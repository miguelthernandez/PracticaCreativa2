import os
import subprocess
import shutil

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

    # Crear un nuevo docker-compose a partir del base
    original_file = "docker-compose-base.yml"
    new_file = "docker-compose.yml"

    if not os.path.exists(new_file):  # Solo copiar si no existe el archivo destino
        if os.path.exists(original_file):
            shutil.copy(original_file, new_file)
        else:
            print(f"El archivo {original_file} no existe. Asegúrate de que está en el directorio actual.")
            return
    else:
        print(f"El archivo {new_file} ya existe. No se copiará de nuevo.")

    # Definir las variables en función de la versión
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
    current_dir = os.getcwd()
    subprocess.call(['docker', 'run', '--rm', '-u', 'root', '-v', f'{current_dir}:/home/gradle/project', '-w', '/home/gradle/project', 'gradle:4.8.1', 'gradle', 'clean', 'build'])
    subprocess.call(['docker', 'build', '-t', 'reviews/15', './reviews-wlpcfg'])

    # Construir y levantar los contenedores con docker-compose
    os.chdir('../../../..')  # Volver al directorio raíz del proyecto
    subprocess.call(['docker-compose', 'build'])
    subprocess.call(['docker-compose', 'up', '-d'])

if __name__ == "__main__":
    main()
