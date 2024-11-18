import psycopg2
import pandas as pd

# Configuración de la base de datos
DB_CONFIG = {
    'dbname': 'fruitycert',
    'user': 'fruityadmin',
    'password': 'securepassword',
    'host': 'localhost',
    'port': 5432
}

def execute_query(query):
    """Ejecuta una consulta SQL y devuelve el resultado como un DataFrame."""
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def save_to_csv(df, output_path):
    """Guarda un DataFrame como archivo CSV."""
    df.to_csv(output_path, index=False)
    print(f"Archivo guardado en: {output_path}")

def analytics_pipeline():
    # Ejercicio 1: Cálculo de Calificaciones Promedio por Lote y Pallet
    query1 = """
    SELECT 
        l.lot_name AS lote,
        p.pallet_id AS pallet,
        i.inspection_id AS inspeccion,
        AVG(s.quality_score) AS NotaLoteQ,
        AVG(s.condition_score) AS NotaLoteC,
        AVG(s.quality_score) OVER (PARTITION BY p.pallet_id) AS NotaPalletQ,
        AVG(s.condition_score) OVER (PARTITION BY p.pallet_id) AS NotaPalletC,
        AVG(s.quality_score) OVER (PARTITION BY i.inspection_id) AS NotaInspQ,
        AVG(s.condition_score) OVER (PARTITION BY i.inspection_id) AS NotaInspC
    FROM Lot l
    INNER JOIN LotPallet lp ON l.lot_id = lp.lot_id
    INNER JOIN Pallet p ON lp.pallet_id = p.pallet_id
    INNER JOIN Inspection i ON p.inspection_id = i.inspection_id
    INNER JOIN Sample s ON p.pallet_id = s.pallet_id
    GROUP BY l.lot_name, p.pallet_id, i.inspection_id, s.quality_score, s.condition_score;
    """
    df1 = execute_query(query1)
    save_to_csv(df1, "../analytics/CalificacionesPromedio.csv")

    # Ejercicio 2: Análisis de Rendimiento por Variedad y Mercado
    query2 = """
    SELECT 
        p.market AS Market,
        p.variety AS Variety,
        AVG(s.quality_score) AS calidad_promedio,
        RANK() OVER (PARTITION BY p.market ORDER BY AVG(s.quality_score) DESC) AS rank
    FROM Pallet p
    INNER JOIN Sample s ON p.pallet_id = s.pallet_id
    GROUP BY p.market, p.variety;
    """
    df2 = execute_query(query2)
    save_to_csv(df2, "../analytics/RendimientoPorVariedadMercado.csv")

    # Ejercicio 3: Monitoreo de Desempeño de Parámetros Específicos
    query3 = """
    SELECT 
        pi.parameter_id AS CodigoParametroInspeccion,
        pi.parameter_name AS NombreParametro,
        s.inspection_id,
        EXTRACT(WEEK FROM i.inspection_date) AS semana,
        AVG(s.quality_score) AS ValorParametroInspeccion,
        LAG(AVG(s.quality_score)) OVER (PARTITION BY pi.parameter_id ORDER BY EXTRACT(WEEK FROM i.inspection_date)) AS valor_anterior,
        AVG(s.quality_score) - LAG(AVG(s.quality_score)) OVER (PARTITION BY pi.parameter_id ORDER BY EXTRACT(WEEK FROM i.inspection_date)) AS diferencia,
        CASE 
            WHEN (AVG(s.quality_score) - LAG(AVG(s.quality_score)) OVER (PARTITION BY pi.parameter_id ORDER BY EXTRACT(WEEK FROM i.inspection_date))) > 5 THEN 'ALERTA'
            ELSE 'NORMAL'
        END AS alerta_variacion
    FROM Parameter pi
    INNER JOIN Sample s ON pi.parameter_id = s.sample_id
    INNER JOIN Inspection i ON s.inspection_id = i.inspection_id
    WHERE p.variety = 'UVAS' AND p.package = 'PACK' AND p.grower = 'GreenHarvest Exports'
    GROUP BY pi.parameter_id, pi.parameter_name, s.inspection_id, i.inspection_date;
    """
    df3 = execute_query(query3)
    save_to_csv(df3, "../analytics/MonitoreoDesempeno.csv")

    # Ejercicio 4: Identificación de Outliers en Parámetros de Inspección
    query4 = """
    WITH Stats AS (
        SELECT 
            pi.parameter_id AS CodigoParametroInspeccion,
            AVG(s.quality_score) AS media,
            STDDEV(s.quality_score) AS desviacion
        FROM Parameter pi
        INNER JOIN Sample s ON pi.parameter_id = s.sample_id
        GROUP BY pi.parameter_id
    )
    SELECT 
        s.sample_id AS CodigoParametroInspeccion,
        s.quality_score AS ValorParametro,
        (s.quality_score - st.media) / st.desviacion AS z_score,
        CASE 
            WHEN ABS((s.quality_score - st.media) / st.desviacion) > 3 THEN 'OUTLIER'
            ELSE 'NORMAL'
        END AS estado
    FROM Sample s
    INNER JOIN Stats st ON s.sample_id = st.CodigoParametroInspeccion;
    """
    df4 = execute_query(query4)
    save_to_csv(df4, "../analytics/OutliersParametros.csv")


if __name__ == '__main__':
    analytics_pipeline()
