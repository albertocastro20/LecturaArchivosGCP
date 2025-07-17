# LecturaArchivosGCP
Título: Lectura de archivos en GCP

Introducción: Se nos solicitó crear una infraestructur de GCP, la cual contendría APIs y configuración de roles. Asi mismo creamos un bucket en el cual subiríamos los archivos. Por ultimo se creó una Cloud Function en la cual introduciremos nuestro código 

Objetivo: Crear un entorno seguro y escalable en GCP

Arquitectura:
El proceso se basa en el siguiente flujo de trabajo:

1. Cloud Storage: Un bucket dedicado (tu-nombre-bucket-gcp-uploads) actúa como punto de entrada para los archivos. Está configurado con reglas de ciclo de vida para gestionar la retención y el almacenamiento eficiente.

2. Cloud Function: Una función serverless (procesar-archivos-storage), escrita en Python, se activa automáticamente cada vez que se sube un nuevo archivo al bucket de Cloud Storage.

3. Cloud Logging: La función extrae metadatos esenciales del archivo (nombre, tamaño, tipo de contenido) y registra estos eventos, junto con cualquier error, en Cloud Logging para facilitar la monitorización y depuración.

Pre-requisitos:

Cuenta de GCP.
Python 3.13.
pip instalado

Configuración del Proyecto GCP (Paso a Paso):

Crear un nuevo proyecto de GCP:

Accede a la Consola de Google Cloud.

Haz clic en "Seleccionar un proyecto" en la barra superior > "Nuevo proyecto".

Nombra tu proyecto, por ejemplo, mi-proyecto-infra-gcp. Anota el ID del proyecto.

gcloud projects create mi-proyecto-infra-gcp --name="Mi Proyecto Infra GCP"

gcloud config set project mi-proyecto-infra-gcp

Habilitar APIs necesarias:

Desde la "Biblioteca de APIs y Servicios" en la consola de GCP, habilita las siguientes APIs:

Cloud Storage API

Cloud Functions API

Cloud Pub/Sub API

Cloud Logging API

Cloud Build API (Opcional, pero recomendado)
Pruebas:

Cómo ejecutar las pruebas unitarias.

Resultados esperados.

Verificación y Monitoreo:

Cómo verificar que la función se activó (subiendo un archivo al bucket).

Cómo ver los registros en Cloud Logging.

Decisiones Técnicas y Configuraciones Aplicadas:

Explica por qué elegiste Python/Node.js.

Justifica el uso de reglas de ciclo de vida.

Explica el principio de privilegio mínimo en IAM.

Menciona el manejo de errores y logging detallado.

Conclusión: Un breve resumen de lo logrado.
