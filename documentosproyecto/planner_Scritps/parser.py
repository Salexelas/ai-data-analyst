import json
import re

def extract_json(text: str):

    match = re.search(r"<json>(.*?)</json>", text, re.DOTALL)

    if not match:
        raise ValueError("No JSON found")

    return match.group(1)


def parse_plan(raw: str):

    cleaned = extract_json(raw)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON from LLM")