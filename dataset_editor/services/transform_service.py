import pandas as pd
import json
import re


class TransformService:

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

    def preview_transform(
        self,
        df,
        column,
        instruction,
        llm
    ):

        sample = (
            df[column]
            .dropna()
            .astype(str)
            .head(20)
            .tolist()
        )

        prompt = f"""
Transformá valores de una columna.

COLUMNA:
{column}

VALORES:
{sample}

INSTRUCCIÓN:
{instruction}

REGLAS:
- aplicar la instrucción a cada valor
- devolver SOLO JSON array
- misma cantidad de elementos
- mismo orden
- sin explicación
"""

        response = llm.generate(
            prompt=prompt,
            system_prompt="data transformer"
        )

        cleaned = self.clean_json(response)

        try:

            transformed = json.loads(cleaned)

            return pd.DataFrame({
                "original": sample,
                "transformado": transformed
            })

        except Exception:

            return pd.DataFrame({
                "error": [response]
            })

    def apply_transform(
        self,
        df,
        column,
        preview_df
    ):

        mapping = dict(
            zip(
                preview_df["original"],
                preview_df["transformado"]
            )
        )

        df = df.copy()

        df[column] = (
            df[column]
            .astype(str)
            .replace(mapping)
        )

        return df