import os
from datetime import datetime

from services.ocr.loader import load_ocr
from services.ocr.llm_parser_service import OCRLLMParserService
from services.ocr.validator_service import OCRValidatorService
from connectors.factory import create_connector


class OCRPipeline:

    @staticmethod
    def extract(uploaded_file):
        ocr = load_ocr()
        return ocr.extract_text(uploaded_file.getvalue())

    @staticmethod
    def build_dataframe(
        raw_text,
        columns,
        context,
        examples,
        llm
    ):

        cols = [
            c.strip()
            for c in columns.split(",")
            if c.strip()
        ]

        parser = OCRLLMParserService()

        return parser.parse_to_dataframe(
            raw_text=raw_text,
            columns=cols,
            context=context,
            examples=examples,
            llm=llm
        )

    @staticmethod
    def validate(df):
        validator = OCRValidatorService()
        return validator.validate_dataframe(df)

    @staticmethod
    def save(df, prefix="ocr"):

        DATA_PATH = "data"
        os.makedirs(DATA_PATH, exist_ok=True)

        filename = f"{prefix}_{datetime.now():%Y%m%d_%H%M%S}.csv"
        path = os.path.join(DATA_PATH, filename)

        df.to_csv(path, index=False)

        connector = create_connector(
            "csv",
            {"file_path": path}
        )

        return {
            "file_path": path,
            "dataset_id": filename,
            "connector": connector
        }