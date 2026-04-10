from core.llm import call_llm
import json
import re


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else "{}"


def analyze_question(question, schema, semantic_layer=None):

    semantic_text = ""

    if semantic_layer:
        semantic_text = f"""
Semantic Layer:
Aliases: {semantic_layer.get("aliases")}
Metrics: {semantic_layer.get("metrics")}
"""

    prompt = f"""
You are a senior data analyst.

Return ONLY JSON:

{{
  "valid": true/false,
  "related": true/false,
  "sql": "SQL query"
}}

Rules:
- Only SELECT queries
- Table name is: data
- Do not hallucinate columns
- ALWAYS wrap column names with spaces using double quotes

Schema:
{schema}

{semantic_text}

Question:
{question}
"""

    raw = call_llm(prompt)
    cleaned = extract_json(raw)

    try:
        return json.loads(cleaned)
    except:
        return {"valid": False, "related": False, "sql": ""}



'''
2. ❌ Prompt extremadamente débil (core del producto)
You are a SQL expert.
Schema:
{schema}
Question:
{question}
Generate only SQL.

👉 Problemas graves:

No hay:
instrucciones de negocio
ejemplos (few-shot)
restricciones
validaciones

👉 Resultado:

SQL incorrecto
joins mal hechos
columnas inventadas
errores silenciosos

💥 Esto es el mayor cuello de botella hoy.
'''