# Proyecto FruityCert

Este repositorio contiene el desarrollo que resuelve el deafio de Microsystem en relación a la gestión de inspecciones de calidad y condición de frutas para la empresa FruityCert. 

Incluye:

- Diseño del Diagrama Entidad-Relación (DER) y normalización de las tablas.
- Implementación de la base de datos en PostgreSQL utilizando Docker.
- Pipeline de datos que extrae datos desde un bucket de S3, los transforma y los   carga en PostgreSQL.
- Procesos de Respaldo y Recuperación ante Desastres (DR) utilizando el formato Parquet.
- Capa de analitica de data
- Ejemplos con la implementación de infrestructua como codigo

# Contenido del Repositorio 

- fruitycert_db/  : Tiene la configuración de la base de datos PostgreSQL en el archivo sql/create_tables.sql con Docker.
- fruitycert_dr/: Scripts para respaldo y recuperación.
  backup.py
  restore.py
- backups/ (carpeta para almacenar los respaldos)
- fruitycert_pipeline/ : Código del pipeline y carpeta para los archivos Avro generados a partir de la extracción desde S3, por un tema de capacity se muestra 1 registro en github
   - avro/ (carpeta que almacena un ejemplo de data con formato Avro generado del pipeline)
   - pipeline/fruitycert_pipeline.py
   - pipeline/analytics/ : Carpeta que contiene la data analitica generada con la fruitcert_analytics.py
- img/: Carpeta que contiene las imagenes que solicita el desafio para que pueda ser legible por todos.
- infra/: Carpeta que contiene ejemplos de la implementación de infraestructura como código

- README.md: Este archivo con instrucciones detalladas.
- requirements.txt : Contiene las dependencias utilizadas en el proyecto
--

## Diagrama Entidad-Relación (DER)

![Diagrama ER](https://github.com/jparadae/fruitycerpipe/blob/main/img/DiagramaER.png)

Este diagrama representa la estructura de la base de datos, detallando las entidades, atributos y relaciones utilizadas en el sistema.

---

## Tablas Normalizadas

![Tablas Normalizadas](https://github.com/jparadae/fruitycerpipe/blob/main/img/normalizadas.png)

Las tablas han sido normalizadas para cumplir con la **3FN**, garantizando la integridad y eliminación de redundancias.


# Cómo Probar el Repositorio desde Cero

- Prerrequisitos: 
   1. Docker instalado en tu sistema.
   2. Python 3.7 o superior.
   3. Virtualenv (opcional, pero recomendado).
   4. Git para clonar el repositorio.
   5. Herramienta de gestión de bases de datos como DBeaver o el cliente psql.
--

# Pasos Detallados:
1. Clonar el Repositorio
- Abre una terminal y ejecuta: ´https://github.com/jparadae/fruitycerpipe.git´
- Accede al directorio con : ´cd fruitycert´

2. Configurar y Ejecutar la Base de Datos con Docker
- Navega al directorio de la base de datos: ´cd fruitycert_db´
- Construye la imagen de Docker: ´docker build -t fruitycert-db . ´
- Ejecuta el contenedor: ´docker run -d --name fruitycert-db -p 5432:5432 fruitycert-db´
- Verifica que el contenedor esté corriendo: ´docker ps´

3. Configurar el Entorno Virtual para Python
- Vuelve al directorio principal: ´cd ..´
- Crea y activa un entorno virtual: ´python3 -m venv venv´
  ´source venv/bin/activate´
4. Instalar Dependencias: ´pip install -r requirements.txt´
5. Ejecutar el Pipeline de Datos
- Navega al directorio del pipeline: ´cd fruitycert_pipeline/pipeline´
- Ejecuta el script del pipeline:´python fruitycert_pipeline.py´ 

## Diseño de Arquitectura de Datos Escalable

![Arquitectura](https://github.com/jparadae/fruitycerpipe/blob/main/img/arquitectura.jpeg)

Se presenta el diseño de la arquitectura propuesta de acuerdo a la escalabilidad

--

## Infraestructura como Código

![Infra](https://github.com/jparadae/fruitycerpipe/blob/main/img/infrae.png)

Se presenta la implementación como codigo propuesta, para mas detalle puedes revisar el código

--

Nota: El script descargará automáticamente los archivos CSV desde el bucket de S3, los convertirá a formato Avro y los procesará para cargarlos en PostgreSQL.



