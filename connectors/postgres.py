import pandas as pd
import sqlalchemy as sa
from connectors.base import BaseConnector

class PostgresConnector(BaseConnector):
    def __init__(self, uri):
        self.engine = sa.create_engine(uri)

    def execute(self, query):
        with self.engine.connect() as conn:
            result = conn.execute(sa.text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_schema(self):
        query = """
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name
        """
        return self.execute(query)
    
    def preview(self, limit=10):
        tables = self.get_tables()

        if not tables:
            return pd.DataFrame({"error": ["No hay tablas en schema public"]})

        table = tables[0]

        query = f"SELECT * FROM {table} LIMIT {limit}"
        return self.execute(query)
    
    def get_tables(self):
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        """
        df = self.execute(query)
        return df["table_name"].tolist()