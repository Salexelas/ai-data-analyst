from agents.planner.llm_generator import generate_raw_plan
from agents.planner.parser import parse_plan
from agents.planner.validator import validate_plan


def create_plan(question, schema, semantic_layer=None):

    for _ in range(2):  # retry SOLO si falla LLM output

        raw = generate_raw_plan(question, schema, semantic_layer)

        try:
            plan = parse_plan(raw)
        except:
            continue  # si el LLM devuelve basura → retry

        validate_plan(plan)

        return plan

    raise ValueError("Planner failed after retries")