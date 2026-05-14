import pandas as pd


class PandasAdapter:

    def load_preview(self, file_path, limit=1000):

        if file_path.endswith(".csv"):
            return pd.read_csv(file_path, nrows=limit)

        if file_path.endswith(".xlsx"):
            return pd.read_excel(file_path, nrows=limit)

        raise ValueError("Formato no soportado")

    def save(self, df, file_path):

        if file_path.endswith(".csv"):
            df.to_csv(file_path, index=False)

        elif file_path.endswith(".xlsx"):
            df.to_excel(file_path, index=False)

        else:
            raise ValueError("Formato no soportado")