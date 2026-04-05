'''
from agents.sql_agent import generate_sql

def route_question(question, connector):

    schema = connector.get_schema()
    sql = generate_sql(question, schema)

    try:
        return connector.execute(sql)
    except Exception as e:
        return f"SQL Error: {str(e)}"

'''





'''       cambio sugerido   ***** guardrail   **** evita "DROP", "DELETE", "UPDATE", "INSERT", "ALTER"  ******
'''
import os
import json
from agents.sql_agent import generate_sql


def save_query(dataset_id, question, sql):
    os.makedirs("query_history", exist_ok=True)

    path = f"query_history/{dataset_id}.json"

    data = []

    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)

    data.append({
        "question": question,
        "sql": sql
    })

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def route_question(question, connector, semantic_layer=None, dataset_id=None):

    schema = connector.get_schema()

    sql = generate_sql(
        question,
        schema,
        semantic_layer
    )

    try:
        result = connector.execute(sql)

        # 💾 guardar query
        if dataset_id:
            save_query(dataset_id, question, sql)

        return result

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