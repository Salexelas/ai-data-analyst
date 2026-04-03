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
        """
        return self.execute(query)
    
    def preview(self, limit=10):
        query = f"SELECT * FROM information_schema.tables LIMIT 1"
        return self.execute(query)