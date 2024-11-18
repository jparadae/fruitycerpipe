import psycopg2
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

def backup_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    for table in TABLES:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        backup_path = os.path.join(BACKUP_DIR, f"{table}.parquet")
        df.to_parquet(backup_path, index=False)
        print(f"Respaldo de {table} completado en {backup_path}")
    conn.close()

if __name__ == '__main__':
    backup_tables()
