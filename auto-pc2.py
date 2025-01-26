import logging, sys, os
from lib_mv import init_app_docker_compose, mv_pesada, mv_docker, mv_docker_compose, mv_kubernetes, destroy_cluster, config_cluster, docker_destroy, info_cluster

def init_log():
    # Creacion y configuracion del logger
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('auto_p2')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.propagate = False

def pause():
    programPause = input("Press the <ENTER> key to continue...")

def main():

    # Establecer la posición de la orden en la línea de argumentos
    orden = sys.argv[1]

    if orden == "parte1":
        puerto = sys.argv[2]
        mv_pesada(puerto)
    #python3 auto-pc2.py parte1 9080

    elif orden == "parte2":
        if sys.argv[2] == "start":
            mv_docker()
        elif sys.argv[2] == "destruir":
            docker_destroy()
    #python3 auto-pc2.py parte2 start
    #python3 auto-pc2.py parte2 destruir

    elif orden == "parte3":
        order2 = sys.argv[2]
        if order2 == "start":
            print("Despliegue de la aplicación multiservicio mediante docker-compose")
            init_app_docker_compose()
        elif order2 == "destroy":
            print("Eliminación de todas las imágenes y contenedores Docker")
            docker_destroy()
    #python3 auto-pc2.py parte3 v1
    #python3 auto-pc2.py parte3 v2
    #python3 auto-pc2.py parte3 v3
    #python3 auto-pc2.py parte3 destruir

    elif orden == "parte4":
        if sys.argv[2] == "destruir":
            destroy_cluster()
        elif sys.argv[2] == "info":
            info_cluster()
        else:
            cluster = sys.argv[2]
            if sys.argv[3] == "configurar":
                config_cluster(cluster)
            else:
                version = sys.argv[3]
                mv_kubernetes(version)
    #python3 auto-pc2.py parte4 nombre-cluster configurar
    #python3 auto-pc2.py parte4 nombre-cluster v1     
    #python3 auto-pc2.py parte4 nombre-cluster v2
    #python3 auto-pc2.py parte4 nombre-cluster v3 
    #python3 auto-pc2.py parte4 info
    #python3 auto-pc2.py parte4 destruir

    else:
        print(f"Orden no reconocida: {orden}")

if __name__ == "__main__":
    main()