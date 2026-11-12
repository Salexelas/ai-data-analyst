from abc import ABC, abstractmethod
import pandas as pd

class BaseConnector(ABC):

    @abstractmethod
    def execute(self, query: str) -> pd.DataFrame:
        """Ejecuta una consulta y devuelve un DataFrame."""
        pass
    
    @abstractmethod
    def get_schema(self, table_name: str = None) -> pd.DataFrame:
        """Obtiene la estructura de las tablas."""
        pass

    @abstractmethod
    def preview(self, table_name: str, limit: int = 10) -> pd.DataFrame:
        """Obtiene una muestra de una tabla."""
        pass

    def close(self):
        """Libera los recursos del conector."""
        pass