from core.llm import call_llm
from core.llm_hf import call_hf

class LLMService:

    def generate(self, prompt: str, system_prompt: str) -> str:

        full_prompt = system_prompt + "\n\n" + prompt

        # 🔥 1. intento Groq (rápido)
        try:
            return call_llm(prompt, system_prompt)
        except Exception as e:
            print("⚠️ Groq falló:", e)

        # 🔥 2. fallback HuggingFace
        try:
            return call_hf(full_prompt)
        except Exception as e:
            print("⚠️ HF falló:", e)

        # 🔥 3. fallback final
        return "No pude responder en este momento."