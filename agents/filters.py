import unicodedata
import re

def normalize_query_for_intent(text: str):
    text = normalize(text)  # ya tenés esto

    replacements = {
        "más": "mas",
        "top": "top",
        "mayores": "top",
        "mejores": "top",
        "peores": "bottom",
        "menos": "bottom"
    }

    tokens = text.split()
    tokens = [replacements.get(t, t) for t in tokens]

    return " ".join(tokens)


def fuzzy_match_score(q, term):
    q_tokens = set(q.split())
    t_tokens = set(term.split())

    if not t_tokens:
        return 0

    overlap = len(q_tokens & t_tokens)
    return overlap / len(t_tokens)

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

    q = normalize(question)

    terms = []

    # metrics
    terms += list(semantic_layer.get("metrics", {}).keys())

    # aliases
    for v in semantic_layer.get("aliases", {}).values():
        if isinstance(v, list):
            terms += v
        else:
            terms.append(v)

    # 🔥 fallback real
    terms += semantic_layer.get("columns", [])

    terms = [normalize(t) for t in terms]

    def match_score(q, term):
        q_tokens = set(q.split())
        t_tokens = set(term.split())

        if not t_tokens:
            return 0

        coverage = len(q_tokens & t_tokens) / len(t_tokens)
        substring = 1 if term in q else 0

        return coverage + 0.3 * substring

    return any(match_score(q, t) >= 0.5 for t in terms)


def detect_language_fast(text):
    text = text.lower()

    scores = {
        "es": 0,
        "en": 0,
        "pt": 0,
        "de": 0,
        "fr": 0,
        "it": 0
    }

    lang_keywords = {
        "es": ["el", "la", "los", "las", "de", "que", "en", "y", "para", "con", "por", "estadisticas", "equipo"],
        "en": ["the", "is", "are", "of", "and", "in", "for", "with", "stats", "team"],
        "pt": ["o", "a", "os", "as", "de", "que", "em", "para", "com", "estatisticas", "equipe"],
        "de": ["der", "die", "das", "und", "ist", "in", "für", "mit", "statistik", "mannschaft"],
        "fr": ["le", "la", "les", "de", "et", "est", "dans", "pour", "avec", "statistiques", "equipe"],
        "it": ["il", "lo", "la", "gli", "le", "di", "e", "è", "per", "con", "statistiche", "squadra"]
    }

    tokens = text.split()

    for lang, keywords in lang_keywords.items():
        for token in tokens:
            if token in keywords:
                scores[lang] += 1

    best_lang = max(scores, key=scores.get)

    if scores[best_lang] == 0:
        return "en"

    return best_lang
