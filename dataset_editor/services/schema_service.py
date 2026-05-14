import os
import json

SCHEMA_PATH = "schemas"
os.makedirs(SCHEMA_PATH, exist_ok=True)


class SchemaService:

    @staticmethod
    def load(dataset_name):

        schema_file = os.path.join(
            SCHEMA_PATH,
            f"{dataset_name}.schema.json"
        )

        if not os.path.exists(schema_file):
            return {}

        try:
            with open(schema_file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception:
            return {}

    @staticmethod
    def save(dataset_name, schema):

        schema_file = os.path.join(
            SCHEMA_PATH,
            f"{dataset_name}.schema.json"
        )

        with open(schema_file, "w", encoding="utf-8") as f:
            json.dump(
                schema,
                f,
                indent=4,
                ensure_ascii=False
            )