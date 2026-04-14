import logging
from agents.planner.planner import create_plan
from agents.executor import execute_plan

logger = logging.getLogger(__name__)


def answer_question(question, connector, semantic_layer=None):

    try:
        schema = connector.get_schema()

        plan = create_plan(question, schema, semantic_layer)

        logger.info("Plan generado", extra={
            "question": question,
            "plan": plan
        })

        return execute_plan(plan, connector)

    except ValueError as e:
        return {"type": "error", "message": str(e)}

    except Exception as e:
        return {"type": "error", "message": f"Error inesperado: {str(e)}"}