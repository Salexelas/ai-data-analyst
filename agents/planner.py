from core.llm import call_llm
import json
import re


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else "{}"


def create_plan(question, schema, semantic_layer=None):

    semantic_text = ""
    if semantic_layer:
        semantic_text = f"""
Semantic Layer:
Aliases: {semantic_layer.get("aliases")}
Metrics: {semantic_layer.get("metrics")}
"""

    prompt = f"""
You are a planning agent.

Return ONLY JSON:

{{
  "valid": true/false,
  "related": true/false,
  "steps": [
    {{
      "tool": "sql",
      "input": "SQL query"
    }},
    {{
      "tool": "insight",
      "input": "user question"
    }}
  ]
}}

Rules:
- If question is nonsense → valid = false
- If not related to schema → related = false
- Only SELECT queries
- Column names with spaces MUST be wrapped in double quotes
- NEVER use columns without quotes if they contain spaces
- Table name is data

Schema:
{schema}

{semantic_text}

Question:
{question}
"""

    raw = call_llm(prompt, system_prompt="You are a data planning agent")

    cleaned = extract_json(raw)

    try:
        plan = json.loads(cleaned)
    except:
        raise ValueError("Planner failed")

    if not plan.get("valid"):
        raise ValueError("No pude entender la consulta.")

    if not plan.get("related"):
        raise ValueError("La consulta no está relacionada con los datos.")

    return plan