#from agents.registry import REGISTRY

'''
def execute_plan(plan, connector):

    context = {}

    for step in plan["steps"]:

        tool_name = step["tool"]

        if tool_name not in REGISTRY:
            raise ValueError(f"Tool {tool_name} no registrada")

        entry = REGISTRY[tool_name]

        handler = entry["handler"]
        tool = entry["tool"]

        handler(step, context, connector, tool)

    if "last_result" not in context:
        raise ValueError("No hubo ejecución SQL")

    print("CONTEXT FINAL:", context)
    return {
        "type": "table",
        "data": context["last_result"],
        "explanation": context.get("explanation")
    }

'''
'''
def execute_plan(plan, connector):

    context = {}

    # -------------------------
    # 1. Ejecutar pasos normales
    # -------------------------
    for step in plan["steps"]:

        tool_name = step["tool"]

        if tool_name not in REGISTRY:
            raise ValueError(f"Tool {tool_name} no registrada")

        entry = REGISTRY[tool_name]

        handler = entry["handler"]
        tool = entry["tool"]

        handler(step, context, connector, tool)

    # -------------------------
    # 2. Validar que hubo SQL
    # -------------------------
    if "last_result" not in context:
        raise ValueError("No hubo ejecución SQL")

    # -------------------------
    # 3. 🔥 FORZAR INSIGHT (modo test)
    # -------------------------
    if "explanation" not in context:

        insight_tool = REGISTRY["insight"]["tool"]

        try:
            result = insight_tool.run(
                "Explain the result",
                connector,
                context
            )

            context["explanation"] = result

        except Exception as e:
            context["explanation"] = f"No se pudo generar insight: {str(e)}"

    # -------------------------
    # 4. DEBUG
    # -------------------------
    print("CONTEXT FINAL:", context)

    # -------------------------
    # 5. Response
    # -------------------------
    return {
        "type": "table",
        "data": context["last_result"],
        "explanation": context.get("explanation")
    }'''