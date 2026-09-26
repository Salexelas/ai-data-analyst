import duckdb
import pandas as pd
from connectors.base import BaseConnector

class DuckDBConnector(BaseConnector):
    def __init__(self, path=None):
        self.con = duckdb.connect()
        self.table_name = "data"

        if path:  # CSV/Parquet subido
            self.con.execute(f"""
                CREATE OR REPLACE TABLE {self.table_name} AS
                SELECT * FROM read_csv_auto('{path}')
            """)
        else:  # Tabla demo
            self.con.execute(f"""
                CREATE OR REPLACE TABLE {self.table_name} AS
                SELECT * FROM (VALUES
                    ('Producto A', 10, 100),
                    ('Producto B', 5, 200),
                    ('Producto C', 8, 150)
                ) AS t(producto, cantidad, precio)
            """)

    def execute(self, query):
        return self.con.execute(query).df()

    def get_schema(self):
        return self.con.execute(f"DESCRIBE {self.table_name}").df()

    def preview(self, limit=10):
        return self.con.execute(f"SELECT * FROM {self.table_name} LIMIT {limit}").df()
