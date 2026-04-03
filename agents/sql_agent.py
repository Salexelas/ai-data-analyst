from core.llm import call_llm

def generate_sql(question, schema):

    prompt = f"""
    You are a senior data analyst.

    RULES:
    - Only generate valid SQL
    - Use only existing columns
    - Do not invent fields
    - Limit results to 100 rows

    SCHEMA:
    {schema}

    QUESTION:
    {question}

    SQL:
    """

    return call_llm(prompt)


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