import os
import json
import pandas as pd

#from agents.sql_agent import analyze_question



# -------------------------
# UTILIDADES
# -------------------------

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


'''def normalize_df(df):
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame({"result": [str(df)]})

    df = df.copy()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str)

    return df
'''

# -------------------------
# PIPELINE
# -------------------------
'''
def run_pipeline(question, connector, semantic_layer=None, dataset_id=None):

    # 1️⃣ SCHEMA
    schema = connector.get_schema()

    # 2️⃣ ANALYSIS (TODO en una llamada)
    analysis = analyze_question(question, schema, semantic_layer)

    if not analysis["valid"]:
        raise ValueError("No pude entender la consulta.")

    if not analysis["related"]:
        raise ValueError("La consulta no está relacionada con los datos.")

    sql = analysis["sql"]

    # 3️⃣ VALIDACIÓN SQL (local, sin LLM)
    sql_upper = sql.upper()

    if not sql_upper.startswith(("SELECT", "WITH")):
        raise ValueError("SQL inválido")

    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT"]

    if any(word in sql_upper for word in forbidden):
        raise ValueError("SQL peligroso")

    # 4️⃣ EJECUCIÓN
    result = connector.execute(sql)
    result = normalize_df(result)

    # 5️⃣ SAVE
    if dataset_id:
        save_query(dataset_id, question, sql)

    return {
        "type": "table",
        "data": result,
        "sql": sql
    }

    
    '''
# -------------------------
# ROUTER (ENTRYPOINT)
# -------------------------

from agents.orchestrator import run


def route_question(question, connector, semantic_layer=None, dataset_id=None):

    try:
        return run(question, connector, semantic_layer, dataset_id)

    except ValueError as e:
        return {"type": "error", "message": str(e)}

    except Exception as e:
        return {"type": "error", "message": f"Error: {str(e)}"}
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

