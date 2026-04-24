import unicodedata
import re

def normalize(text):
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text


def is_match(q, term):
    return term in q or q in term


def token_overlap(a, b):
    a_tokens = set(a.split())
    b_tokens = set(b.split())
    return len(a_tokens & b_tokens) > 0


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

    terms = []

    terms += list(semantic_layer.get("metrics", {}).keys())

    for v in semantic_layer.get("aliases", {}).values():
        if isinstance(v, list):
            terms += v
        else:
            terms.append(v)

    q = normalize(question)
    terms = [normalize(t) for t in terms]

    return any(
        is_match(q, t) or token_overlap(q, t)
        for t in terms
    )

