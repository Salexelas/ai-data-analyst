import os
from dotenv import load_dotenv

load_dotenv()

class SQLConfig:
    MAX_ROWS = int(os.getenv("MAX_ROWS", 1000))
    MAX_JOINS = int(os.getenv("MAX_JOINS", 3))

class LLMConfig:
    TIMEOUT = int(os.getenv("QUERY_TIMEOUT", 10))
    MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile") 
    TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))