import psycopg2
import psycopg2.extras
import pandas as pd
import os

DB_CONFIG = {
    'dbname': 'fruitycert',
    'user': 'fruityadmin',
    'password': 'securepassword',
    'host': 'localhost',
    'port': 5432
}

TABLES = ['Inspection', 'Pallet', 'Sample', 'Parameter', 'CustomerAttributes', 'Lot', 'LotPallet']

BACKUP_DIR = 'backups'

def restore_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    for table in TABLES:
        backup_path = os.path.join(BACKUP_DIR, f"{table}.parquet")
        if os.path.exists(backup_path):
            df = pd.read_parquet(backup_path)
            # Borrar datos existentes
            cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
            conn.commit()
            # Inserción en lotes para mayor eficiencia
            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ','.join(list(df.columns))
            placeholders = ','.join(['%s'] * len(df.columns))
            query = f"INSERT INTO {table}({cols}) VALUES({placeholders})"
            psycopg2.extras.execute_batch(cursor, query, tuples)
            conn.commit()
            print(f"Restauración de {table} completada desde {backup_path}")
        else:
            print(f"No se encontró respaldo para {table}")
    conn.close()

if __name__ == '__main__':
    restore_tables()
