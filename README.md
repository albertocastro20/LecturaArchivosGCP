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

-Cuenta de GCP.

-Python 3.13.

-pip instalado

Configuración del Proyecto GCP (Paso a Paso):

1. Crear un nuevo proyecto de GCP:

  -Accede a la Consola de Google Cloud.
  
  -Haz clic en "Seleccionar un proyecto" en la barra superior > "Nuevo proyecto".
  
  -Nombra tu proyecto, por ejemplo, mi-proyecto-infra-gcp. Anota el ID del proyecto.

2. Habilitar APIs necesarias:

Desde la "Biblioteca de APIs y Servicios" en la consola de GCP, habilita las siguientes APIs:

  -Cloud Storage API
  
  -Cloud Functions API
  
  -Cloud Pub/Sub API
  
  -Cloud Logging API
  
  -Cloud Build API (Opcional, pero recomendado)

3. Asignar roles:
   Para asginar roles necesitamos crear una nueva cuenta que funcionará como un "empleado", a ella le asignamos los roles que se nos indicaron

4. Creación de Bucket:
   Navegamos a la opcion de Cloud Storaged > Buckets, y configuramos uno nuevo personalizandolo con permisos y un ciclo de vida

5. Creación de una Cloud function:
  Navegamos hasta Cloud Run para crear la función, esta tiene que estar alojada en la misma región de nuestro bucket, al igual especificamos que actuará sobre el bucket creado.
  Una vez creado, le pegaremos nuestro código de python (adjuntado en nuestra carpeta del proyecto) a main.py
  
Pruebas:

Verificar la activación de la función:

1. Sube un archivo de prueba (ej. mi-archivo.txt) a tu bucket de Cloud Storage
2. Verificar los registros en Cloud Logging:
  Ve al "Menú de Navegación" (☰) > "Operaciones" > "Explorador de registros" (Logs Explorer).
  Filtra por "Recurso" > "Cloud Function" y selecciona procesar-archivos-storage.
  Deberías ver los mensajes INFO y WARNING generados por la función, así como los ERROR si subiste un archivo que causó una excepción.
<img width="1265" height="147" alt="image" src="https://github.com/user-attachments/assets/4d7369e0-bdc6-4bfb-adc0-75d4747ba731" />

Decisiones Técnicas y Configuraciones Aplicadas:
Elección de Python: Se optó por Python debido a su legibilidad, amplia adopción en el ecosistema de GCP para funciones serverless y la disponibilidad de librerías robustas (google-cloud-storage). 

Reglas de Ciclo de Vida en Cloud Storage: Implementadas para optimizar costos y gestionar la retención de datos. Los archivos se mueven a una clase de almacenamiento más económica (Nearline) después de 7 días y se eliminan automáticamente después de 30 días, asegurando que solo los datos relevantes y recientes permanezcan en almacenamiento Standard.

Principio de Privilegio Mínimo (IAM): La cuenta de servicio usuario-prueba-produccion fue configurada con los roles más restrictivos posibles que le permiten realizar sus tareas específicas (leer/escribir objetos, invocar funciones, escribir logs) sin otorgar permisos innecesarios que podrían representar un riesgo de seguridad.

Manejo de Errores y Logging Detallado: La Cloud Function incluye bloques try-except para capturar y registrar excepciones inesperadas. El uso de logging.error(..., exc_info=True) asegura que los tracebacks completos se envíen a Cloud Logging, lo cual es fundamental para una depuración eficiente en entornos de producción. Los mensajes INFO y WARNING proporcionan visibilidad sobre el flujo normal y las condiciones atípicas.

Conclusión:
Este proyecto demuestra la capacidad de diseñar, implementar y desplegar una solución de procesamiento de archivos basada en eventos en GCP, priorizando la seguridad (IAM), la eficiencia (reglas de ciclo de vida) y la observabilidad (logging, pruebas unitarias). La arquitectura serverless de Cloud Functions permite una escalabilidad automática y un modelo de pago por uso, ideal para cargas de trabajo variables.

