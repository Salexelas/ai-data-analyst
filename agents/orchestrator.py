from agents.planner import create_plan
from agents.executor import execute_plan


def run(question, connector, semantic_layer=None, dataset_id=None):

    schema = connector.get_schema()

    plan = create_plan(question, schema, semantic_layer)

    result = execute_plan(plan, connector)

    return result