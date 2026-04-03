import pandas as pd
import sqlalchemy as sa
from connectors.base import BaseConnector
import duckdb

class GoogleSheetsConnector(BaseConnector):

    def __init__(self, url):
        csv_url = convert_to_csv_url(url)

        self.df = pd.read_csv(csv_url)
        self.conn = duckdb.connect()
        self.conn.register("data", self.df)

    def execute(self, query):
        return self.conn.execute(query).df()

    def get_schema(self):
        return self.conn.execute("DESCRIBE data").df()

    def preview(self, limit=10):
        return self.df.head(limit)
    
    def convert_to_csv_url(url: str) -> str:
        if "docs.google.com/spreadsheets" not in url:
            raise ValueError("No es un link válido de Google Sheets")

        try:
            sheet_id = url.split("/d/")[1].split("/")[0]
            return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
        except:
            raise ValueError("No se pudo parsear el link")
        
def convert_to_csv_url(url: str) -> str:
    sheet_id = url.split("/d/")[1].split("/")[0]

    if "gid=" in url:
        gid = url.split("gid=")[1]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"