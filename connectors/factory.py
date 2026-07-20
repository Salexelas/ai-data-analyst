from connectors.api import APIConnector
from connectors.csv import CSVConnector
from connectors.duckdb import DuckDBConnector
from connectors.excel import ExcelConnector
from connectors.googleSheets import GoogleSheetsConnector
from connectors.mysql import MySQLConnector
from connectors.postgres import PostgresConnector


def get_file_source(config):
    """Return the configured file source."""

    source = config.get("file_path") or config.get("file")

    if source is None:
        raise ValueError(
            "Missing 'file_path' or 'file' in config."
        )

    return source


def create_duckdb(config):
    return DuckDBConnector(get_file_source(config))


def create_excel(config):
    return ExcelConnector(get_file_source(config))


def create_csv(config):
    return CSVConnector(get_file_source(config))


def create_postgres(config):
    return PostgresConnector(config["uri"])


def create_mysql(config):
    return MySQLConnector(config["uri"])


def create_api(config):
    return APIConnector(config["base_url"])


def create_google_sheets(config):
    return GoogleSheetsConnector(config["url"])


CONNECTOR_FACTORIES = {
    "duckdb": create_duckdb,
    "excel": create_excel,
    "csv": create_csv,
    "postgres": create_postgres,
    "mysql": create_mysql,
    "api": create_api,
    "google_sheets": create_google_sheets,
}


def create_connector(source_type, config):
    """Create the requested connector."""

    try:
        factory = CONNECTOR_FACTORIES[source_type]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported data source: {source_type}"
        ) from exc

    return factory(config)