#Usaremos las siguientes librerías
import logging # para registrar mensajes (información, advertencias, errores) y depurar problemas en Cloud Logging.
import json #para trabajar con datos en formato JSON. 
import functions_framework #librería específica de Google que facilita la escritura de Cloud Functions en Python.

# Configura el nivel de logging para que los mensajes de INFO sean visibles.
logging.basicConfig(level=logging.INFO)

# El decorador le indica al entorno de Google Cloud cómo invocar tu función cuando recibe un evento 
@functions_framework.cloud_event
def proceso_gcs_archivo(cloud_event): #Se recibe un evento desde Cloud
    """
    Función de Cloud que procesa eventos de Cloud Storage.
    Se activa cada vez que se sube, se crea o se actualiza un objeto en un bucket de Storage.

    Args:
        cloud_event: Objeto CloudEvent que contiene los datos del evento de Cloud Storage.
                     Estos datos incluyen metadatos como el nombre del bucket, el nombre del archivo,
                     el tamaño y el tipo de contenido.
    Returns:
        Una tupla con un mensaje de estado y un código HTTP.
        Retorna ("OK", 200) si el procesamiento fue exitoso.
        Retorna un mensaje de error y un código HTTP de error si ocurre un problema.
    """
    logging.info("Función activada por evento de Cloud Storage.")

    try:
        # Extrae los datos del evento CloudEvent.
        # Los datos pueden venir como bytes (JSON codificado) o directamente como un diccionario.
        if isinstance(cloud_event.data, bytes):
            data_str = cloud_event.data.decode('utf-8')
            data = json.loads(data_str) # Convierte la cadena JSON a un diccionario Python.
        elif isinstance(cloud_event.data, dict):
            data = cloud_event.data # Si ya es un diccionario, úsalo directamente.
        else:
            # Maneja tipos de datos de evento inesperados, registrando el error.
            logging.error(f"Tipo de datos de evento inesperado: {type(cloud_event.data)}")
            logging.error(f"Contenido completo del evento: {cloud_event.data}")
            return "Error: Tipo de datos inesperado", 500

        # Extrae metadatos específicos del archivo del diccionario de datos del evento.
        # Se usa .get() para evitar KeyError si alguna clave no está presente.
        source_bucket = data.get('bucket')
        file_name = data.get('name')
        file_size = data.get('size')
        file_content_type = data.get('contentType')

        # Verifica si alguna de las claves esperadas está ausente.
        # Si faltan claves, se lanza un KeyError para ser capturado por el bloque except.
        if not all([source_bucket, file_name, file_size, file_content_type]):
            missing_keys = []
            if not source_bucket: missing_keys.append('bucket')
            if not file_name: missing_keys.append('name')
            if not file_size: missing_keys.append('size')
            if not file_content_type: missing_keys.append('contentType')
            raise KeyError(f"Clave(s) faltante(s): {', '.join(missing_keys)}")

        # Registra los metadatos extraídos en los logs de Cloud Logging.
        logging.info(f"Archivo subido al bucket '{source_bucket}':")
        logging.info(f"  Nombre: {file_name}")
        logging.info(f"  Tamaño: {file_size} bytes")
        logging.info(f"  Tipo: {file_content_type}")
        logging.info("Metadatos registrados exitosamente.")

        # Indica que la función se ejecutó exitosamente.
        # Esto evita reintentos innecesarios por parte de Eventarc.
        return "OK", 200

    except KeyError as e:
        # Maneja errores por claves faltantes en los datos del evento.
        logging.error(f"Error, clave faltante en el evento: '{e}'")
        logging.error(f"Contenido del evento: {cloud_event.data}")
        return f"Error: Clave faltante - {e}", 400

    except json.JSONDecodeError as e:
        # Maneja errores si los datos del evento no son un JSON válido.
        logging.error(f"Error al decodificar JSON de los datos del evento: {e}")
        logging.error(f"Datos brutos del evento: {cloud_event.data}")
        return f"Error: JSON inválido - {e}", 400

    except Exception as e:
        # Captura cualquier otro error inesperado durante la ejecución de la función.
        logging.error(f"Ocurrió un error inesperado: {e}")
        logging.error(f"Detalles del evento: {cloud_event.data}")
        return f"Error interno del servidor: {e}", 500