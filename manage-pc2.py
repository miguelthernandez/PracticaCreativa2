import logging, sys 
from lib_mv import mv_docker_compose, docker_destroy

def init_log():
    # Creacion y configuracion del logger
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('manage-pc2')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.propagate = False


def main():

    # Establecer la posición de la orden en la línea de argumentos
    orden = sys.argv[1]

    if orden == "parte3":
        if sys.argv[2] == "start":
                mv_docker_compose()
        else:
                docker_destroy()
    else:
        print(f"Orden no reconocida: {orden}")

if __name__ == "__main__":
    main()