import pandas as pd
import json
import re


class OCRLLMParserService:

    def clean_json(self, response):

        response = response.strip()
        response = response.replace("```json", "")
        response = response.replace("```", "")

        match = re.search(
            r"\[.*\]",
            response,
            re.DOTALL
        )

        if match:
            return match.group(0)

        return response

    def parse_to_dataframe(
        self,
        raw_text,
        columns,
        examples,
        context,
        llm
    ):

        if not columns:
            return pd.DataFrame({
                "error": ["No columns"]
            })

        prompt = f"""
Extraé dataset estructurado.

CONTEXTO:
{context}

TEXTO OCR:
{raw_text}

COLUMNAS:
{", ".join(columns)}

EJEMPLOS:
{examples}

REGLAS:
- devolver SOLO JSON
- no inventar
- null si falta
"""

        response = llm.generate(
            prompt=prompt,
            system_prompt="OCR parser"
        )

        cleaned = self.clean_json(response)

        try:
            return pd.DataFrame(json.loads(cleaned))

        except Exception:
            return pd.DataFrame({
                "raw_output": [response]
            })