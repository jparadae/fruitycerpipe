import boto3
import pandas as pd
import os
import psycopg2
from io import BytesIO

# Configuración de S3
S3_BUCKET = 'prueba-fruitycert'
S3_FILES = {
    'AtributosCliente': 'AtributosCliente.csv',
    'TablonInspecciones': 'TablonInspecciones.csv',
    'ParametrosInspeccion': 'ParametrosInspeccion.csv',
    'AtributosLotes': 'AtributosLotes.csv'
}
CSV_OUTPUT_DIR = '../csv'  # Directorio de salida para CSVs

# Configuración de la base de datos
DB_CONFIG = {
    'dbname': 'fruitycert',
    'user': 'fruityadmin',
    'password': 'securepassword',
    'host': 'localhost',
    'port': 5432
}

# Descarga archivos desde S3 y guarda las primeras 10 filas como CSV
def download_from_s3():
    s3 = boto3.client('s3', region_name='us-east-1')
    if not os.path.exists(CSV_OUTPUT_DIR):
        os.makedirs(CSV_OUTPUT_DIR)
    
    downloaded_files = {}
    for key, file_name in S3_FILES.items():
        file_path = os.path.join(CSV_OUTPUT_DIR, f"{key}.csv")
        response = s3.get_object(Bucket=S3_BUCKET, Key=file_name)
        
        # Leer datos en pandas
        data = pd.read_csv(BytesIO(response['Body'].read()), low_memory=False, dtype=str)
        
        # Tomar las primeras 10 filas
        top_10_rows = data.iloc[:10]
        
        # Guardar como CSV
        top_10_rows.to_csv(file_path, index=False)
        
        print(f"Archivo {key} descargado y guardado como CSV con las primeras 10 filas en {file_path}")
        downloaded_files[key] = file_path
    
    return downloaded_files

# Función para cargar datos a PostgreSQL
def load_csv_to_postgres(csv_files, db_config):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    for table_name, csv_file in csv_files.items():
        # Leer el archivo CSV en pandas
        data = pd.read_csv(csv_file)
        
        # Generar consulta de inserción
        columns = ', '.join(data.columns)
        values = ', '.join(['%s'] * len(data.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) ON CONFLICT DO NOTHING"
        
        # Insertar registros fila por fila
        for _, row in data.iterrows():
            cursor.execute(insert_query, tuple(row))
        
        conn.commit()
        print(f"Datos cargados en la tabla {table_name} desde {csv_file}")
    
    cursor.close()
    conn.close()

# Pipeline principal
def run_pipeline():
    # Descargar y procesar archivos CSV
    csv_files = download_from_s3()
    
    # Cargar los CSV a la base de datos PostgreSQL
    load_csv_to_postgres(csv_files, DB_CONFIG)

if __name__ == '__main__':
    run_pipeline()
