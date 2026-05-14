class OCRValidatorService:

    def validate_dataframe(self, df):

        errors = []

        if df.empty:
            errors.append("DataFrame vacío")

        if "raw_output" in df.columns:
            errors.append("Error parseando JSON")

        return errors