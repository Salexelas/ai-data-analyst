from core.llm import call_llm

class LLMService:
    def generate(self, prompt: str, system_prompt: str) -> str:
        return call_llm(prompt, system_prompt)