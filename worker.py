# worker.py
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Worker iniciado...")
    while True:
        # Aquí iría tu lógica de procesamiento en segundo plano
        logger.info("Procesando tareas...")
        time.sleep(60)
