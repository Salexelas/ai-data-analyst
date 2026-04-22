from core.llm_service import LLMService


def generate_sql(question, schema, semantic_layer, llm, language="en"):

    semantic_text = ""

    if semantic_layer:
        semantic_text = f"""
Semantic Layer:
Aliases: {semantic_layer.get("aliases")}
Metrics: {semantic_layer.get("metrics")}
"""

    prompt = f"""
Generate a SQL query.

Rules:
- Only SELECT
- Table name is data
- Use correct columns
- No explanation

Schema:
{schema}

{semantic_text}

Question:
{question}
"""

    return llm.generate(
        prompt,
        system_prompt=f"You are a senior data analyst. The user speaks {language}"
    )