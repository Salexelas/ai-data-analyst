from agents.planner.schema import validate_plan_structure


def validate_plan(plan):

    validate_plan_structure(plan)

    if not plan.get("valid"):
        raise ValueError("No pude entender la consulta.")

    if not plan.get("related"):
        raise ValueError("La consulta no está relacionada con los datos.")

    return True