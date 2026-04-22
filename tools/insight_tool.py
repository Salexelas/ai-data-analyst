#from core.llm import call_llm


class InsightTool:

    def __init__(self, llm):
        self.llm = llm

    def run(self, question, context):

        if "language" not in context:
            raise ValueError("Language not provided in context")

        df = context.get("last_result")

        if df is None or df.empty:
            return "No hay datos para analizar."

        lang = context["language"]

        preview = df.head(20).to_string()

        prompt = f"""
You are analyzing query results.

Question:
{question}

Data:
{preview}

Instructions:
- Provide a concise business insight
- Do not mention SQL
- Focus on key patterns, trends, or anomalies

IMPORTANT:
- The response MUST be written in language: {lang}
- Do NOT use any other language
"""

        return self.llm.generate(
            prompt,
            system_prompt=f"""
You are a senior business data analyst.

CRITICAL RULE:
- You ALWAYS respond in language: {lang}
- You NEVER switch language
"""
        )