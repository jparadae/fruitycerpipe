import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import psycopg2
import csv

class CleanCustomerAttributes(beam.DoFn):
    def process(self, element):
        # Limpieza para AtributosCliente.csv
        element = {k: (v if v != "" else None) for k, v in element.items()}
        yield element

class CleanInspectionData(beam.DoFn):
    def process(self, element):
        # Limpieza para TablonInspecciones.csv
        element = {k: (v if v != "" else None) for k, v in element.items()}
        if "inspection_date" in element:
            element["inspection_date"] = element["inspection_date"][:10]  # Formato YYYY-MM-DD
        yield element

class CleanParameterData(beam.DoFn):
    def process(self, element):
        # Limpieza para ParametrosInspeccion.csv
        element = {k: (v if v != "" else None) for k, v in element.items()}
        yield element

class CleanLotData(beam.DoFn):
    def process(self, element):
        # Limpieza para AtributosLotes.csv
        element = {k: (v if v != "" else None) for k, v in element.items()}
        yield element

class WriteToPostgres(beam.DoFn):
    def __init__(self, db_config, table_name, insert_query):
        self.db_config = db_config
        self.table_name = table_name
        self.insert_query = insert_query

    def start_bundle(self):
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


def run_pipeline(input_paths, db_config):
    pipeline_options = PipelineOptions()

    with beam.Pipeline(options=pipeline_options) as p:
        # AtributosCliente.csv
        customer_attributes = (
            p
            | 'Read CustomerAttributes' >> beam.io.ReadFromText(input_paths['AtributosCliente'], skip_header_lines=1)
            | 'Parse CustomerAttributes' >> beam.Map(lambda line: dict(zip(
                ["customer_id", "analysis1", "analysis2", "analysis3", "analysis4", "analysis5"],
                csv.reader([line]).__next__()
            )))
            | 'Clean CustomerAttributes' >> beam.ParDo(CleanCustomerAttributes())
            | 'Write CustomerAttributes to PostgreSQL' >> beam.ParDo(WriteToPostgres(
                db_config,
                'CustomerAttributes',
                """
                INSERT INTO CustomerAttributes (customer_id, analysis1, analysis2, analysis3, analysis4, analysis5)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """
            ))
        )

        # TablonInspecciones.csv
        inspections = (
            p
            | 'Read Inspections' >> beam.io.ReadFromText(input_paths['TablonInspecciones'], skip_header_lines=1)
            | 'Parse Inspections' >> beam.Map(lambda line: dict(zip(
                ["inspection_date", "port", "inspector_name"],
                csv.reader([line]).__next__()
            )))
            | 'Clean Inspections' >> beam.ParDo(CleanInspectionData())
            | 'Write Inspections to PostgreSQL' >> beam.ParDo(WriteToPostgres(
                db_config,
                'Inspection',
                """
                INSERT INTO Inspection (inspection_date, port, inspector_name)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                """
            ))
        )

        # ParametrosInspeccion.csv
        parameters = (
            p
            | 'Read Parameters' >> beam.io.ReadFromText(input_paths['ParametrosInspeccion'], skip_header_lines=1)
            | 'Parse Parameters' >> beam.Map(lambda line: dict(zip(
                ["parameter_name", "description"],
                csv.reader([line]).__next__()
            )))
            | 'Clean Parameters' >> beam.ParDo(CleanParameterData())
            | 'Write Parameters to PostgreSQL' >> beam.ParDo(WriteToPostgres(
                db_config,
                'Parameter',
                """
                INSERT INTO Parameter (parameter_name, description)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """
            ))
        )

        # AtributosLotes.csv
        lots = (
            p
            | 'Read Lots' >> beam.io.ReadFromText(input_paths['AtributosLotes'], skip_header_lines=1)
            | 'Parse Lots' >> beam.Map(lambda line: dict(zip(
                ["lot_name"],
                csv.reader([line]).__next__()
            )))
            | 'Clean Lots' >> beam.ParDo(CleanLotData())
            | 'Write Lots to PostgreSQL' >> beam.ParDo(WriteToPostgres(
                db_config,
                'Lot',
                """
                INSERT INTO Lot (lot_name)
                VALUES (%s)
                ON CONFLICT DO NOTHING
                """
            ))
        )


if __name__ == "__main__":
    input_paths = {
        'AtributosCliente': 'path/to/AtributosCliente.csv',
        'TablonInspecciones': 'path/to/TablonInspecciones.csv',
        'ParametrosInspeccion': 'path/to/ParametrosInspeccion.csv',
        'AtributosLotes': 'path/to/AtributosLotes.csv'
    }
    db_config = {
        'dbname': 'fruitycert',
        'user': 'fruityadmin',
        'password': 'securepassword',
        'host': 'localhost',
        'port': 5432
    }

    run_pipeline(input_paths, db_config)
