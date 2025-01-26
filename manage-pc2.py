# Importación de módulos para registro y manejo del sistema
import logging, sys
# Importación de funciones específicas desde la librería lib_mv
from lib_mv import mv_docker_compose, mv_docker_compose_destroy

def init_log():
    # Creación y configuración del logger para registrar mensajes de depuración
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('manage-pc2')
    
    # Configuración del manejador de flujo para imprimir en consola
    ch = logging.StreamHandler(sys.stdout)
    
    # Definición del formato de los mensajes de log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    
    # Añadimos el manejador de flujo al logger
    log.addHandler(ch)
    
    # Desactivamos la propagación de mensajes a los manejadores padres
    log.propagate = False

def main():
    # Establecer la posición de la orden en la línea de argumentos (el primer argumento)
    orden = sys.argv[1]

    # Verificar si la orden es "parte3" y tomar acción según el siguiente argumento
    if orden == "parte3":
        if sys.argv[2] == "start":
            # Llamar a la función mv_docker_compose() para iniciar el servicio
            mv_docker_compose()
        else:
            # Llamar a la función mv_docker_compose_destroy() para destruir el servicio
            mv_docker_compose_destroy()
    else:
        # Si la orden no es reconocida, mostrar un mensaje de error
        print(f"Orden no reconocida: {orden}")

# Ejecutar la función principal si este archivo es ejecutado como script
if __name__ == "__main__":
    main()
