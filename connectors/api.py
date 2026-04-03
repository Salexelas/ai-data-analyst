import requests
import pandas as pd
from connectors.base import BaseConnector

class APIConnector(BaseConnector):
    def __init__(self, base_url):
        self.base_url = base_url

    def execute(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        data = response.json()
        return pd.DataFrame(data)

    def get_schema(self):
        return {"type": "api", "note": "Schema depends on endpoint"}
    
    def preview(self, limit=10):
        data = self.execute("")
        return data.head(limit)
