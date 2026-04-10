from tools.registry import get_tool


def execute_plan(plan, connector):

    context = {}
    explanation = None

    for step in plan["steps"]:
        tool = get_tool(step["tool"])

        result = tool.run(step["input"], connector, context)

        if step["tool"] == "insight":
            explanation = result

    return {
        "type": "table",
        "data": context.get("last_result"),
        "explanation": explanation
    }