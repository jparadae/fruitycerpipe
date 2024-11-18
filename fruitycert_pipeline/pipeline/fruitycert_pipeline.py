import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import boto3
import pandas as pd
import fastavro
import os
from io import BytesIO

# Configuración de S3
S3_BUCKET = 'prueba-fruitycert'
S3_FILES = {
    'AtributosCliente': 'AtributosCliente.csv',
    'TablonInspecciones': 'TablonInspecciones.csv',
    'ParametrosInspeccion': 'ParametrosInspeccion.csv',
    'AtributosLotes': 'AtributosLotes.csv'
}
AVRO_OUTPUT_DIR = '../avro'

# Descarga archivos desde S3
def download_from_s3():
    s3 = boto3.client('s3', region_name='us-east-1')
    if not os.path.exists(AVRO_OUTPUT_DIR):
        os.makedirs(AVRO_OUTPUT_DIR)
    
    downloaded_files = {}
    for key, file_name in S3_FILES.items():
        file_path = os.path.join(AVRO_OUTPUT_DIR, f"{key}.avro")
        response = s3.get_object(Bucket=S3_BUCKET, Key=file_name)
        data = pd.read_csv(BytesIO(response['Body'].read()))
        schema = {
            "doc": f"Schema for {key}",
            "name": key,
            "namespace": "fruitycert",
            "type": "record",
            "fields": [{"name": col, "type": ["null", "string"]} for col in data.columns]
        }
        with open(file_path, 'wb') as out:
            fastavro.writer(out, schema, data.to_dict('records'))
        downloaded_files[key] = file_path
        print(f"Archivo {key} descargado y convertido a Avro en {file_path}")
    
    return downloaded_files

# Limpieza de datos
class CleanData(beam.DoFn):
    def process(self, element):
        # Manejo de valores nulos y tipos de datos
        element = {k: (v if v != "" else None) for k, v in element.items()}
        yield element

# Escribe en PostgreSQL
class WriteToPostgres(beam.DoFn):
    def __init__(self, db_config, table_name, insert_query):
        self.db_config = db_config
        self.table_name = table_name
        self.insert_query = insert_query

    def start_bundle(self):
        import psycopg2
        self.conn = psycopg2.connect(**self.db_config)
        self.cursor = self.conn.cursor()

    def process(self, element):
        try:
            self.cursor.execute(self.insert_query, list(element.values()))
            self.conn.commit()
        except Exception as e:
            print(f"Error al insertar en {self.table_name}: {e}")

    def finish_bundle(self):
        self.conn.close()

# Pipeline principal que inserta datos como output en PostgreSQL
def run_pipeline(avro_files, db_config):
    pipeline_options = PipelineOptions()

    with beam.Pipeline(options=pipeline_options) as p:
        for table_name, avro_path in avro_files.items():
            (
                p
                | f'Read {table_name}' >> beam.io.ReadFromAvro(avro_path)
                | f'Clean {table_name}' >> beam.ParDo(CleanData())
                | f'Write {table_name} to PostgreSQL' >> beam.ParDo(WriteToPostgres(
                    db_config,
                    table_name,
                    f"""
                    INSERT INTO {table_name} ({', '.join(avro_files[table_name].columns)})
                    VALUES ({', '.join(['%s'] * len(avro_files[table_name].columns))})
                    ON CONFLICT DO NOTHING
                    """
                ))
            )

if __name__ == '__main__':
    # Descarga y convierte los archivos de S3
    avro_files = download_from_s3()

    # Configuración de la base de datos
    db_config = {
        'dbname': 'fruitycert',
        'user': 'fruityadmin',
        'password': 'securepassword',
        'host': 'localhost',
        'port': 5432
    }

    # Ejecuta el pipeline
    run_pipeline(avro_files, db_config)
