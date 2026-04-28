import json

def detect_intent(question: str, llm):

    prompt = f"""
Classify the user intent.

Return ONLY JSON:

{{
  "intent": "top | bottom | average | total | comparison | distribution | unknown",
  "metric": "string or null",
  "dimension": "string or null"
}}

Question:
{question}
"""

    raw = llm.generate(prompt, system_prompt="Intent classifier")

    try:
        return json.loads(raw)
    except:
        return {
            "intent": "unknown",
            "metric": None,
            "dimension": None
        }