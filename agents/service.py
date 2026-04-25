from core.query_context import QueryContext, InputContext
from core.pipeline import Pipeline
from agents.steps import *

def answer_question(question, connector, semantic_layer=None, llm=None):

    ctx = QueryContext(
        input=InputContext(
            question=question,
            connector=connector,
            semantic_layer=semantic_layer,
            llm=llm
        )
    )

    pipeline = Pipeline([
        ValidateStep(),
        DetectLanguageStep(),
        LoadSchemaStep(),
        GenerateSQLStep(llm),
        ExecuteSQLStep(),
        InsightStep(llm)
    ])

    try:
        ctx = pipeline.run(ctx)

        return {
            "type": "table",
            "data": ctx.output.result,
            "explanation": ctx.output.insight,
            "language": ctx.exec.language
        }

    except Exception as e:
        error_msg = str(e).lower()

        print("❌ ERROR:", error_msg)

        # errores esperables → fallback amigable
        if any(x in error_msg for x in [
            "sin resultados",
            "columnas inválidas",
            "sql inválido"
        ]):
            return {
                "type": "table",
                "data": [],
                "explanation": "No encontré resultados claros. Probá reformular la pregunta.",
                "language": "es"
            }

        # errores graves → mostrar error real
        return {
            "type": "error",
            "message": str(e)
        }