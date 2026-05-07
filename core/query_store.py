import os
import json
import time

QUERIES_PATH = "data_queries/queries.json"


def load_queries():
    if not os.path.exists(QUERIES_PATH):
        return []

    try:
        with open(QUERIES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_query(question, dataset_id=None, intent=None, response=None):

    print("🔥 SAVE QUERY EJECUTADO")

    queries = []

    if os.path.exists(QUERIES_PATH):
        try:
            with open(QUERIES_PATH, "r", encoding="utf-8") as f:
                queries = json.load(f)
        except:
            queries = []

    new_query = {
        "question": question,
        "dataset": dataset_id,
        "intent": intent,
        "ts": time.time(),
        "response": response
    }

    queries = [q for q in queries if q["question"] != question]
    queries.insert(0, new_query)
    queries = queries[:50]

    # 🔥 ESTA ES LA LÍNEA QUE TE FALTABA
    os.makedirs(os.path.dirname(QUERIES_PATH), exist_ok=True)

    print("📁 Path:", QUERIES_PATH)

    with open(QUERIES_PATH, "w", encoding="utf-8") as f:
        json.dump(queries, f, indent=2, ensure_ascii=False)

    print("✅ ARCHIVO GUARDADO")