def is_valid_question_basic(question: str):
    q = question.strip().lower()

    if len(q) < 3:
        return False

    if not any(c.isalpha() for c in q):
        return False

    return True


def is_question_related_fast(question, semantic_layer):

    if not semantic_layer:
        return True

    q = question.lower()

    terms = []

    terms += list(semantic_layer.get("metrics", {}).keys())

    for v in semantic_layer.get("aliases", {}).values():
        if isinstance(v, list):
            terms += v
        else:
            terms.append(v)

    return any(t.lower() in q for t in terms)