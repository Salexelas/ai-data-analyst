from rapidfuzz import fuzz

MAX_ENTITY_VALUES = 100


def generate_abbreviations(text):
    words = str(text).split()
    if not words:
        return []

    initials = "".join(w[0].upper() for w in words if w)
    compact = "".join([w[0].upper() for w in words])

    return list(set([initials, compact]))


def resolve_entity(question, values, dataset_name=None, ctx=None):

    values = list(values)[:MAX_ENTITY_VALUES]
    question_upper = question.upper()
    question_lower = question.lower()

    candidates = []

    # =========================
    # 1. ABBREVIATIONS (HARD SIGNAL)
    # =========================
    for v in values:
        for abbr in generate_abbreviations(v):

            if abbr and abbr in question_upper:

                print("QUESTION:", question_upper)
                print("VALUE:", v)
                print("ABBR:", abbr)

                candidates.append({
                    "value": v,
                    "score": 100,
                    "method": "abbreviation",
                    "dataset": dataset_name
                })

    # =========================
    # 2. FUZZY MATCH (SOFT SIGNAL)
    # =========================
    for v in values:
        score = fuzz.partial_ratio(
            question_lower,
            str(v).lower()
        )

        candidates.append({
            "value": v,
            "score": score,
            "method": "fuzzy",
            "dataset": dataset_name
        })

    candidates = sorted(
        candidates,
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "candidates": candidates[:10],
        "best": candidates[0] if candidates else None
    }