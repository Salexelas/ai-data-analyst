import pandas as pd
from sqlalchemy import create_engine, inspect
from connectors.base import BaseConnector

class SQLDatabaseConnector(BaseConnector):
    def __init__(
        self,
        connection_url: str,
        schema: str = None
    ):
        self.connection_url = connection_url
        self.schema = schema
        self.engine = create_engine(
            connection_url,
            pool_pre_ping=True,
            pool_recycle=1800
        )

    def test_connection(self) -> bool:
        with self.engine.connect() as connection:
            connection.exec_driver_sql("SELECT 1")
        return True

    def execute(self, query: str) -> pd.DataFrame:
        """Ejecuta una consulta SQL en la BD externa y devuelve un DataFrame."""
        with self.engine.connect() as connection:
            return pd.read_sql_query(query, connection)

    def get_schema(self, table_name: str = None) -> pd.DataFrame:
        """Obtiene la estructura de las tablas del esquema configurado."""
        inspector = inspect(self.engine)
        tables = inspector.get_table_names(schema=self.schema)
        
        schema_data = []
        for t in tables:
            if table_name and t != table_name:
                continue
            columns = inspector.get_columns(t, schema=self.schema)
            for col in columns:
                schema_data.append({
                    "table_name": t,
                    "column_name": col["name"],
                    "data_type": str(col["type"])
                })
        return pd.DataFrame(schema_data)

    def preview(self, table_name: str, limit: int = 10) -> pd.DataFrame:
        """Obtiene una muestra de una tabla de forma segura."""
        schema_prefix = f'"{self.schema}".' if self.schema else ''
        query = f"SELECT * FROM {schema_prefix}{table_name} LIMIT {limit}"
        return self.execute(query)

    def close(self):
        """Libera los recursos del engine."""
        if self.engine:
            self.engine.dispose()