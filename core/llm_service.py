from core.observability import log_event
from core.llm import call_llm

class LLMService:
    def generate(self, prompt: str, system_prompt: str, trace_id: str = None) -> str:

        if trace_id:
            log_event(
                "llm_request",
                trace_id,
                prompt=prompt[:500],
                system_prompt=system_prompt
            )

        result = call_llm(prompt, system_prompt)

        if trace_id:
            log_event(
                "llm_response",
                trace_id,
                response=result[:500]
            )

        return result