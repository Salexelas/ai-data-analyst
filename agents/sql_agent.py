'''
from core.llm import call_llm


def clean_sql(output: str) -> str:
    """
    Limpia la respuesta del modelo para quedarse solo con SQL.
    """
    if "```" in output:
        return output.split("```")[1].strip()

    if "SQL:" in output:
        return output.split("SQL:")[-1].strip()

    return output.strip()


def generate_sql(question, schema):
    prompt = f"""
You are a senior SQL expert.

ONLY return a valid SQL query.
Do not explain anything.
Do not add comments.
Do not add markdown.

Schema:
{schema}

Question:
{question}

SQL:
"""

    raw_output = call_llm(prompt)
    sql = clean_sql(raw_output)

    return sql

'''

'''  sugerencia ****** igualetne falta instrucciones de negocio
ejemplos (few-shot)
restricciones
validaciones

****************************************
******principio codigfo**********
'''
from core.llm import call_llm
import re


def clean_sql(output: str) -> str:
    match = re.search(r"(SELECT|WITH).*", output, re.IGNORECASE | re.DOTALL)
    return match.group(0).strip() if match else output.strip()


def generate_sql(question, schema, semantic_layer=None):

    semantic_text = ""

    if semantic_layer:
        semantic_text = f"""
Semantic Layer:
Aliases:
{semantic_layer.get('aliases')}

Metrics:
{semantic_layer.get('metrics')}
"""

    prompt = f"""
You are a senior SQL expert.

ONLY return a valid SQL query.
Do not explain anything.
Do not add comments.
Do not add markdown.

Schema:
{schema}

{semantic_text}

Question:
{question}

SQL:
"""

    raw_output = call_llm(prompt)
    sql = clean_sql(raw_output)

    return sql


   






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