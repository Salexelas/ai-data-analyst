ALLOWED_TOOLS = {"sql", "insight"}

TOOL_SEQUENCE_RULES = {
    "sql": {
        "max": 1,
        "required": True
    },
    "insight": {
        "allowed_after": ["sql"]
    }
}


def validate_plan_structure(plan):

    if not isinstance(plan, dict):
        raise ValueError("Plan must be dict")

    steps = plan.get("steps")

    if not isinstance(steps, list) or len(steps) == 0:
        raise ValueError("Steps must be non-empty list")

    used_tools = []

    for step in steps:

        if not isinstance(step, dict):
            raise ValueError("Step must be dict")

        tool = step.get("tool")
        input_data = step.get("input")

        if tool not in ALLOWED_TOOLS:
            raise ValueError(f"Invalid tool: {tool}")

        if not isinstance(input_data, str):
            raise ValueError("Step input must be string")

        used_tools.append(tool)

    # 🔥 reglas de negocio
    if used_tools.count("sql") != 1:
        raise ValueError("Must contain exactly 1 SQL step")

    if "insight" in used_tools and used_tools[-1] != "insight":
        raise ValueError("Insight must be last step")

    return True
