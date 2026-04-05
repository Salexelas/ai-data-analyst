from core.llm import call_llm
import json
import re


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return "{}"


def generate_semantic_suggestions(columns):

    prompt = f"""
You are a data analyst.

Given these columns:
{columns}

Generate business-friendly aliases and useful metrics.

Return ONLY valid JSON.
"""

    raw = call_llm(prompt)

    # 🔥 DEBUG ACÁ
    print("RAW LLM:", raw)

    cleaned = extract_json(raw)

    try:
        return json.loads(cleaned)
    except:
        return {"aliases": {}, "metrics": {}}