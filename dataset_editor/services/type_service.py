import pandas as pd


TYPE_OPTIONS = [
    "auto",
    "text",
    "number",
    "datetime",
    "boolean",
    "category",
    "id"
]


class TypeService:

    @staticmethod
    def detect(series):

        dtype = str(series.dtype)

        if "datetime" in dtype:
            return "datetime"

        if "int" in dtype or "float" in dtype:
            return "number"

        if "bool" in dtype:
            return "boolean"

        return "text"

    @staticmethod
    def apply(df, schema):

        df = df.copy()

        for col, dtype in schema.items():

            if col not in df.columns:
                continue

            try:

                if dtype == "datetime":
                    df[col] = pd.to_datetime(
                        df[col],
                        dayfirst=True,
                        errors="coerce"
                    )

                elif dtype == "number":
                    df[col] = pd.to_numeric(
                        df[col],
                        errors="coerce"
                    )

                elif dtype == "boolean":
                    df[col] = df[col].astype("bool")

                elif dtype == "category":
                    df[col] = df[col].astype("category")

                elif dtype == "text":
                    df[col] = df[col].astype("string")

            except Exception:
                pass

        return df