import os
import re
import duckdb
import pandas as pd


def normalize_table_name(file_name: str) -> str:
    """Normaliza un nombre de archivo o dataset a un identificador SQL válido."""
    name = (
        file_name
        .replace(".csv", "")
        .replace(".xlsx", "")
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )
    return re.sub(r"[^a-z0-9_]", "_", name)


RELATION_TYPES = {
    (True, True): "one_to_one",
    (True, False): "one_to_many",
    (False, True): "many_to_one",
    (False, False): "many_to_many",
}


def infer_relation_type(left_df, right_df, left_col, right_col):
    """Infiere la cardinalidad entre dos tablas basándose en la unicidad de las columnas."""
    left_unique = left_df[left_col].is_unique if left_col in left_df.columns else False
    right_unique = right_df[right_col].is_unique if right_col in right_df.columns else False
    
    return RELATION_TYPES[(left_unique, right_unique)]


class MultiDatasetConnector:

    def __init__(self, dataset_ids, relations=None, inline_datasets=None):
        """
        :param dataset_ids: Lista de identificadores o nombres de archivo (ej: ["sales", "products.csv"])
        :param relations: Lista de relaciones entre tablas
        :param inline_datasets: Diccionario opcional con DataFrames o listas de dicts enviadas desde la API/CRM
        """
        self.conn = duckdb.connect()
        self.schemas = []
        self.tables = {}
        self.relations = relations or []
        inline_datasets = inline_datasets or {}

        # Mapeo normalizado de inline_datasets para coincidencia tolerante
        normalized_inline = {
            normalize_table_name(k): v for k, v in inline_datasets.items()
        }

        for dataset_id in dataset_ids:
            df = None
            norm_id = normalize_table_name(dataset_id)

            # 1. Prioridad: Cargar desde inline_datasets (coincidencia exacta o normalizada)
            if dataset_id in inline_datasets:
                raw_data = inline_datasets[dataset_id]
            elif norm_id in normalized_inline:
                raw_data = normalized_inline[norm_id]
            else:
                raw_data = None

            if raw_data is not None:
                if isinstance(raw_data, pd.DataFrame):
                    df = raw_data
                elif isinstance(raw_data, list):
                    df = pd.DataFrame(raw_data)

            # 2. Si no estaba en memoria, intentar leer desde la carpeta local 'data/'
            if df is None:
                path = os.path.join("data", dataset_id)

                if os.path.exists(path):
                    if dataset_id.endswith(".csv"):
                        df = pd.read_csv(path)
                    elif dataset_id.endswith(".xlsx"):
                        df = pd.read_excel(path)
                else:
                    if os.path.exists(f"{path}.csv"):
                        df = pd.read_csv(f"{path}.csv")
                    elif os.path.exists(f"{path}.xlsx"):
                        df = pd.read_excel(f"{path}.xlsx")

            # 3. Validar si se logró cargar un DataFrame no vacío
            if df is None or df.empty:
                continue

            table_name = norm_id

            table_entry = {
                "table_name": table_name,
                "df": df
            }

            # Mapeamos tanto por el ID original como por el nombre normalizado
            self.tables[dataset_id] = table_entry
            self.tables[table_name] = table_entry

            # Registramos la tabla virtual en DuckDB
            self.conn.register(table_name, df)

            # Extraemos el esquema con DuckDB
            schema = self.conn.execute(f"DESCRIBE {table_name}").df()
            schema["table_name"] = table_name
            self.schemas.append(schema)

        self._enrich_relations()

    def _enrich_relations(self):
        """Enriquece y valida las relaciones enviadas entre los datasets cargados."""
        enriched = []

        for rel in self.relations:
            # Compatibilidad con distintas llaves del payload JSON
            left_id = rel.get("left_dataset") or rel.get("left_table")
            right_id = rel.get("right_dataset") or rel.get("right_table")
            left_col = rel.get("left_column") or rel.get("left_col")
            right_col = rel.get("right_column") or rel.get("right_col")

            if not left_id or not right_id:
                continue

            norm_left = normalize_table_name(left_id)
            norm_right = normalize_table_name(right_id)

            if norm_left not in self.tables or norm_right not in self.tables:
                continue

            left_df = self.tables[norm_left]["df"]
            right_df = self.tables[norm_right]["df"]

            # Evita fallos si las columnas especificadas no existen
            if left_col not in left_df.columns or right_col not in right_df.columns:
                continue

            cardinality = infer_relation_type(
                left_df,
                right_df,
                left_col,
                right_col
            )

            rel_enriched = {
                "left_dataset": left_id,
                "right_dataset": right_id,
                "left_table": norm_left,
                "right_table": norm_right,
                "left_column": left_col,
                "right_column": right_col,
                "cardinality": cardinality
            }

            enriched.append(rel_enriched)

        self.relations = enriched

    def execute(self, query: str):
        """Ejecuta una consulta SQL en DuckDB sobre las tablas registradas."""
        return self.conn.execute(query).df()

    def get_schema(self):
        """Devuelve el esquema consolidado de todas las tablas registradas."""
        if not self.schemas:
            return pd.DataFrame(columns=["column_name", "column_type", "null", "key", "default", "extra", "table_name"])
        return pd.concat(self.schemas, ignore_index=True)

    def get_relationships(self):
        """Devuelve la lista de relaciones enriquecidas."""
        return self.relations