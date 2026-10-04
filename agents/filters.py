def is_valid_question(question: str) -> bool:
    """Validación mínima de longitud e intención de texto."""
    q = question.strip()
    return len(q) >= 3 and any(c.isalpha() for c in q)