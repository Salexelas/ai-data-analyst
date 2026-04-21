#from core.llm import call_llm


class InsightTool:

    def __init__(self, llm):
        self.llm = llm

    def run(self, question, context):

        df = context.get("last_result")

        if df is None or df.empty:
            return "No hay datos para analizar."

        preview = df.head(20).to_string()

        prompt = f"""
Explain the result in simple business terms.

Question:
{question}

Data:
{preview}

Rules:
- Be concise
- No SQL
- Focus on insights
"""

        return self.llm.generate(
            prompt,
            system_prompt="You are a senior business data analyst"
        )