import os
import re
import duckdb
import pandas as pd


def normalize_table_name(file_name: str):
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

    key = (
        left_df[left_col].is_unique,
        right_df[right_col].is_unique,
    )

    return RELATION_TYPES[key]

class MultiDatasetConnector:

    def __init__(self, dataset_ids, relations=None):

        self.conn = duckdb.connect()
        self.schemas = []
        self.tables = {}
        self.relations = relations or []

        for file_name in dataset_ids:

            path = os.path.join("data", file_name)

            if file_name.endswith(".csv"):
                df = pd.read_csv(path)

            elif file_name.endswith(".xlsx"):
                df = pd.read_excel(path)

            else:
                continue

            table_name = normalize_table_name(file_name)

            self.tables[file_name] = {
                "table_name": table_name,
                "df": df
            }

            self.conn.register(table_name, df)

            schema = self.conn.execute(
                f"DESCRIBE {table_name}"
            ).df()

            schema["table_name"] = table_name
            self.schemas.append(schema)

        self._enrich_relations()

    def _enrich_relations(self):

        enriched = []

        for rel in self.relations:

            left_df = self.tables[rel["left_dataset"]]["df"]
            right_df = self.tables[rel["right_dataset"]]["df"]

            cardinality = infer_relation_type(
                left_df,
                right_df,
                rel["left_column"],
                rel["right_column"]
            )

            rel["cardinality"] = cardinality

            rel["left_table"] = self.tables[
                rel["left_dataset"]
            ]["table_name"]

            rel["right_table"] = self.tables[
                rel["right_dataset"]
            ]["table_name"]

            enriched.append(rel)

        self.relations = enriched

    def execute(self, query: str):
        return self.conn.execute(query).df()

    def get_schema(self):
        return pd.concat(self.schemas, ignore_index=True)

    def get_relationships(self):
        return self.relations