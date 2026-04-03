from connectors.duckdb import DuckDBConnector
from connectors.postgres import PostgresConnector
from connectors.mysql import MySQLConnector
from connectors.api import APIConnector
from connectors.excel import ExcelConnector
from connectors.csv import CSVConnector


def create_connector(source_type, config):

    if source_type == "duckdb":
        return DuckDBConnector(config["path"])

    elif source_type == "postgres":
        return PostgresConnector(config["uri"])

    elif source_type == "mysql":
        return MySQLConnector(config["uri"])

    elif source_type == "excel":
        return ExcelConnector(config["file"])

    elif source_type == "csv":
        return CSVConnector(config["file"])

    elif source_type == "api":
        return APIConnector(config["base_url"])

    else:
        raise ValueError("Unsupported data source")