from core.query_context import QueryContext, InputContext
from core.pipeline import Pipeline
from agents.steps import *
from core.observability import new_trace_id, log_event

def answer_question(question, connector, semantic_layer=None, llm=None):

    trace_id = new_trace_id()

    ctx = QueryContext(
        input=InputContext(
            question=question,
            connector=connector,
            semantic_layer=semantic_layer,
            llm=llm
        ),
        trace_id=trace_id
    )

    # 🔴 START
    log_event(
        "request_start",
        trace_id,
        question=question
    )

    pipeline = Pipeline([
        ValidateStep(),
        DetectLanguageStep(),
        IntentStep(llm), 
        LoadSchemaStep(),
        GenerateSQLStep(llm),
        ExecuteSQLStep(),
        InsightStep(llm)
    ])

    try:
        ctx = pipeline.run(ctx)

        # 🟢 SUCCESS (ahora sí, después de ejecutar)
        log_event(
            "request_success",
            trace_id,
            rows=len(ctx.output.result) if ctx.output.result is not None else 0
        )

        return {
            "type": "table",
            "data": ctx.output.result,
            "explanation": ctx.output.insight,
            "language": ctx.exec.language
        }

    except Exception as e:

        # 🔴 ERROR (dentro del except)
        log_event(
            "request_error",
            trace_id,
            error=str(e)
        )

        error_msg = str(e).lower()

        print("❌ ERROR:", error_msg)

        # fallback amigable
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

        return {
            "type": "error",
            "message": str(e)
        }