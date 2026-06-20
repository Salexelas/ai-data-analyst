from agents.intent_detector import detect_intent
from core.observability import log_event


class IntentService:

    def __init__(self, llm):
        self.llm = llm

    def detect(self, question, semantic_layer):

        intent = detect_intent(
            question,
            self.llm,
            semantic_layer
        )

        log_event(
            "intent_detected",
            "system",
            intent=intent
        )

        return intent