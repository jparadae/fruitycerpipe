# Proyecto FruityCert

Este repositorio contiene el desarrollo que resuelve el deafio de Microsystem en relación a la gestión de inspecciones de calidad y condición de frutas para la empresa FruityCert. 

Incluye:

- Diseño del Diagrama Entidad-Relación (DER) y normalización de las tablas.
- Implementación de la base de datos en PostgreSQL utilizando Docker.
- Pipeline de datos con Apache Beam que extrae datos desde un bucket de S3, los transforma y los   carga en PostgreSQL.
-Procesos de Respaldo y Recuperación ante Desastres (DR) utilizando el formato Parquet.

# Contenido del Repositorio 

- fruitycert_db/  : Configuración de la base de datos PostgreSQL con Docker.
 - Dockerfile
 - sql/create_tables.sql
- fruitycert_pipeline/ : Código del pipeline y carpeta para los archivos Avro generados.
 - pipeline/fruitycert_pipeline.py
 - avro/ (carpeta que almacena un ejemplo de data con formato Avro generado del pipeline)
- fruitycert_dr/: Scripts para respaldo y recuperación.
  backup.py
  restore.py
- backups/ (carpeta para almacenar los respaldos)
- README.md: Este archivo con instrucciones detalladas.

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

--

Nota: El script descargará automáticamente los archivos CSV desde el bucket de S3, los convertirá a formato Avro y los procesará para cargarlos en PostgreSQL.

