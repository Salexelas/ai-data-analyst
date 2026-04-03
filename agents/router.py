from agents.sql_agent import generate_sql

def route_question(question, connector):

    schema = connector.get_schema()
    sql = generate_sql(question, schema)

    try:
        return connector.execute(sql)
    except Exception as e:
        return f"SQL Error: {str(e)}"



'''
👉 Problema:

Todo va a SQL → no hay “inteligencia”
No distingue:
preguntas analíticas vs descriptivas
preguntas imposibles
preguntas que requieren múltiples pasos

👉 Resultado:

Se rompe con preguntas complejas
No podés venderlo como “AI Analyst”, es solo un SQL wrapper con LLM

✅ Solución:
Necesitás un router real:

if is_sql_question(question):
    ...
elif is_metadata_question(question):
    ...
elif is_impossible(question):
    ...
'''