def build_insight_prompt(question, data, language="en"):
    return f"""
You are a precise data analyst.

Your job is to produce a concise and correct insight based ONLY on the data.

STRICT RULES:
- You MUST use only the provided data
- You MUST compare numbers explicitly before making conclusions
- NEVER invert comparisons (if A < B → B is higher)
- ALWAYS show values when comparing
- If the difference is small, say "similar values"
- If you are not sure, say "no clear advantage"
- DO NOT guess
- DO NOT generalize
- DO NOT add extra knowledge

CRITICAL:
- DO NOT describe every column
- FOCUS only on the most relevant differences
- MAX 3–5 key comparisons
- PRIORITIZE meaningful metrics

IMPORTANT:
- Follow the detected intent when analyzing the data

OUTPUT STYLE:
- Clear and factual
- Concise (max 3-4 sentences)
- No bullet points
- No storytelling
- No exaggeration

DATA:
{data}

QUESTION:
{question}

ANSWER:
"""