import pandas as pd
from connectors.base import BaseConnector
import duckdb

class CSVConnector(BaseConnector):

    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.conn = duckdb.connect()
        self.conn.register("data", self.df)

    def execute(self, query: str):
        return self.conn.execute(query).df()

    def get_schema(self):
        return self.conn.execute("DESCRIBE data").df()

    def preview(self, limit=10):
        return self.df.head(limit)