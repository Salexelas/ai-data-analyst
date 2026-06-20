import json

import pandas as pd


class OCRService:

    @staticmethod
    def build_prompt(
        ocr_text,
        columns
    ):

        return f"""
You are an OCR parser.

Convert the OCR text into a valid JSON array.

Rules:
- use exactly the requested columns
- missing values must be null
- never invent data
- return JSON only
- no markdown
- no explanations

OCR Text:
{ocr_text}

Requested Columns:
{columns}
"""

    @staticmethod
    def generate_dataframe(
        ocr_text,
        columns,
        llm
    ):

        prompt = (
            OCRService.build_prompt(
                ocr_text,
                columns
            )
        )

        response = llm.generate(
            prompt=prompt,
            system_prompt=(
                "Convert OCR text "
                "to structured JSON"
            )
        )

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(
            response
        )

        return pd.DataFrame(
            data
        )