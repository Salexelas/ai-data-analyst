from connectors.duckdb import DuckDBConnector
from connectors.postgres import PostgresConnector
from connectors.mysql import MySQLConnector
from connectors.api import APIConnector
from connectors.excel import ExcelConnector
from connectors.csv import CSVConnector
from connectors.googleSheets import GoogleSheetsConnector


def create_connector(source_type, config):

    # 🔹 helper: prioriza file_path sobre file
    def get_file_source(config):
        if "file_path" in config:
            return config["file_path"]
        elif "file" in config:
            return config["file"]
        else:
            raise ValueError("Missing file or file_path in config")

    # -------------------------
    # 📁 FILE-BASED CONNECTORS
    # -------------------------
    if source_type == "duckdb":
        return DuckDBConnector(config.get("file_path") or config.get("file"))

    elif source_type == "excel":
        source = get_file_source(config)
        return ExcelConnector(source)

    elif source_type == "csv":
        source = get_file_source(config)
        return CSVConnector(source)

    # -------------------------
    # 🗄️ DATABASES
    # -------------------------
    elif source_type == "postgres":
        return PostgresConnector(config["uri"])

    elif source_type == "mysql":
        return MySQLConnector(config["uri"])

    # -------------------------
    # 🌐 EXTERNAL
    # -------------------------
    elif source_type == "api":
        return APIConnector(config["base_url"])

    elif source_type == "google_sheets":
        return GoogleSheetsConnector(config["url"])

    else:
        raise ValueError(f"Unsupported data source: {source_type}")