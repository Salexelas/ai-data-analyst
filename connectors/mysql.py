import pandas as pd
import sqlalchemy as sa
from connectors.base import BaseConnector

class MySQLConnector(BaseConnector):
    def __init__(self, uri=None):
        if uri:  # conexión real
            self.engine = sa.create_engine(uri)
            self.demo = False
        else:  # demo
            self.demo = True
            self.df = pd.DataFrame({
                "producto": ["Producto A", "Producto B", "Producto C"],
                "cantidad": [10, 5, 8],
                "precio": [100, 200, 150]
            })

    def execute(self, query):
        if self.demo:
            return self.df  # simple: devuelve todo
        else:
            with self.engine.connect() as conn:
                result = conn.execute(sa.text(query))
                return pd.DataFrame(result.fetchall(), columns=result.keys())

    def get_schema(self):
        if self.demo:
            return pd.DataFrame({
                "column_name": self.df.columns,
                "data_type": [str(dt) for dt in self.df.dtypes]
            })
        else:
            query = """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            """
            return self.execute(query)
    
    def preview(self, limit=10):
        if self.demo:
            return self.df.head(limit)
        else:
            query = f"SELECT * FROM information_schema.tables LIMIT 1"
            return self.execute(query)