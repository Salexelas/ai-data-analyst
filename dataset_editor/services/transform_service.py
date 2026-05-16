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

    def _transform_values(
        self,
        values,
        column,
        instruction,
        llm
    ):

        prompt = f"""
Transformá valores de una columna.

COLUMNA:
{column}

VALORES:
{values}

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

        return json.loads(cleaned)

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

        try:

            transformed = self._transform_values(
                sample,
                column,
                instruction,
                llm
            )

            return pd.DataFrame({
                "original": sample,
                "transformado": transformed
            })

        except Exception as e:

            return pd.DataFrame({
                "error": [str(e)]
            })

    def apply_transform(
        self,
        df,
        column,
        instruction,
        llm
    ):

        df = df.copy()

        values = (
            df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        transformed = self._transform_values(
            values,
            column,
            instruction,
            llm
        )

        mapping = dict(zip(values, transformed))

        df[column] = (
            df[column]
            .astype(str)
            .replace(mapping)
        )

        return df


