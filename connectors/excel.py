import pandas as pd
from connectors.base import BaseConnector
import duckdb

class ExcelConnector(BaseConnector):

    def __init__(self, file):
        self.df = pd.read_excel(file)
        self.conn = duckdb.connect()
        self.conn.register("data", self.df)

    def execute(self, query: str):
        return self.conn.execute(query).df()

    def get_schema(self):
        return self.conn.execute("DESCRIBE data").df()

    def preview(self, limit=10):
        return self.df.head(limit)


'''
7. ❌ Excel connector mal diseñado
self.df.query(query)

👉 Problema:

.query() ≠ SQL
El LLM va a generar SQL, no pandas syntax

💀 Esto directamente no va a funcionar bien
'''