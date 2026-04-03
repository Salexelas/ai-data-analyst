import duckdb
import pandas as pd
from connectors.base import BaseConnector

class DuckDBConnector(BaseConnector):

    def __init__(self, path):
        self.con = duckdb.connect()
        self.table_name = "data"

        self.con.execute(f"""
        CREATE OR REPLACE TABLE {self.table_name} AS
        SELECT * FROM read_csv_auto('{path}')
        """)

    def execute(self, query):
        return self.con.execute(query).df()

    def get_schema(self):
        return self.con.execute(f"DESCRIBE {self.table_name}").fetchdf()

    def preview(self, limit=10):
        return self.con.execute(f"SELECT * FROM {self.table_name} LIMIT {limit}").df()




'''
5. ❌ Schema crudo (muy difícil para el LLM)

Ejemplo:

return self.con.execute(f"DESCRIBE {self.table_name}").fetchdf()

👉 Problema:

El LLM recibe:
tablas sin contexto
sin relaciones
sin significado de negocio

👉 Resultado:

malas queries

'''