import logging
import json
import uuid
from datetime import datetime

def get_logger():
    logger = logging.getLogger("ai_data_analyst")

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger


def log_event(event_type: str, trace_id: str, **kwargs):
    logger = get_logger()

    payload = {
        "ts": datetime.utcnow().isoformat(),
        "trace_id": trace_id,
        "event": event_type,
        **kwargs
    }

    logger.info(json.dumps(payload, default=str))


def new_trace_id():
    return str(uuid.uuid4())