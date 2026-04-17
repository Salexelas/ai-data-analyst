from agents.filters import (
    is_valid_question_basic,
    is_question_related_fast
)

from agents.sql_retry import generate_sql_with_retry
from tools.insight_tool import InsightTool


def answer_question(question, connector, semantic_layer=None, llm=None):

    try:
        # -------------------------
        # 1. BASIC FILTER
        # -------------------------
        if not is_valid_question_basic(question):
            raise ValueError("Pregunta inválida")

        # -------------------------
        # 2. SEMANTIC FILTER
        # -------------------------
        if not is_question_related_fast(question, semantic_layer):
            raise ValueError("Pregunta no relacionada con los datos")

        # -------------------------
        # 3. SCHEMA
        # -------------------------
        schema = connector.get_schema()
        columns = schema["column_name"].tolist()

        # -------------------------
        # 4. SQL (con retry)
        # -------------------------
        sql = generate_sql_with_retry(
            question,
            schema,
            semantic_layer,
            columns,
            llm=llm
        )

        # -------------------------
        # 5. EXECUTE
        # -------------------------
        result = connector.execute(sql)

        if result is None or len(result) == 0:
            raise ValueError("Sin resultados")

        # -------------------------
        # 6. INSIGHT
        # -------------------------
        insight = None

        try:
            insight = InsightTool().run(
                question,
                connector,
                {"last_result": result}
            )
        except:
            pass

        return {
            "type": "table",
            "data": result,
            "explanation": insight
        }

    except ValueError as e:
        return {"type": "error", "message": str(e)}

    except Exception as e:
        return {"type": "error", "message": f"Error inesperado: {str(e)}"}