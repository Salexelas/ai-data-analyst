from core.settings import SQLConfig
import pandas as pd
from connectors.base import BaseConnector
import duckdb

class CSVConnector(BaseConnector):

    def __init__(self, file):
        self.df = pd.read_csv(file)
        self.conn = duckdb.connect()
        self.conn.register("data", self.df)

    def execute(self, query: str):
        df = self.conn.execute(query).df()
        return df.head(SQLConfig.MAX_ROWS)

    def get_schema(self):
        return self.conn.execute("DESCRIBE data").df()

    def preview(self, limit=10):
        return self.df.head(limit)