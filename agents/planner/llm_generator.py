from core.llm import call_llm


def generate_raw_plan(question, schema, semantic_layer=None):

    semantic_text = ""

    if semantic_layer:
        semantic_text = f"""
Semantic Layer:
Aliases: {semantic_layer.get("aliases")}
Metrics: {semantic_layer.get("metrics")}
"""

    prompt = f"""
You are a planning agent.

Return ONLY JSON inside <json></json>.

<json>
{{
  "valid": true/false,
  "related": true/false,
  "steps": [
    {{ "tool": "sql", "input": "SQL query" }},
    {{ "tool": "insight", "input": "user question" }}
  ]
}}
</json>

Rules:
- Only SELECT queries
- Table name is data
- Columns with spaces MUST be quoted

Schema:
{schema}

{semantic_text}

Question:
{question}
"""

    return call_llm(prompt, system_prompt="You are a strict data planner")