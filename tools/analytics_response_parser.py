import json


def parse_analytics_response(text: str):

    try:
        return json.loads(text)

    except Exception:

        return {
            "markdown": text,
            "chart_type": None,
            "metrics": {},
            "severity": "info"
        }