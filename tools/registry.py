from tools.sql_tool import SQLTool
from tools.insight_tool import InsightTool

TOOLS = {
    "sql": SQLTool(),
    "insight": InsightTool()
}


def get_tool(name):
    if name not in TOOLS:
        raise ValueError(f"Tool {name} not found")
    return TOOLS[name]