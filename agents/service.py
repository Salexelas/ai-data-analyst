from core.query_context import QueryContext
from core.pipeline import Pipeline
from agents.steps import (
    ValidateStep,
    DetectLanguageStep,  
    LoadSchemaStep,
    GenerateSQLStep,
    ExecuteSQLStep,
    InsightStep
)


def answer_question(question, connector, semantic_layer=None, llm=None):

    ctx = QueryContext(
        question=question,
        connector=connector,
        semantic_layer=semantic_layer,
        llm=llm
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
            "data": ctx.result,
            "explanation": ctx.insight,
            "language": ctx.language   # 👈 NUEVO
        }

    except Exception as e:
        return {
            "type": "error",
            "message": str(e)
        }