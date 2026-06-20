class FileTypeDetector:

    @staticmethod
    def detect(
        filename: str
    ):

        if filename.endswith(".csv"):
            return "csv"

        if filename.endswith(".xlsx"):
            return "excel"

        return None