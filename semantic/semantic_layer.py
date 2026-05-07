def build_semantic_layer(columns, aliases=None, metrics=None):
    return {
        "columns": columns,
        "aliases": aliases or {},
        "metrics": metrics or {}
    }

def detect_metric(q: str, semantic_layer):
    if not semantic_layer:
        return None

    metrics = semantic_layer.get("metrics", {})

    for metric_name, config in metrics.items():
        aliases = config.get("aliases", [])

        candidates = [metric_name] + aliases

        if any(alias in q for alias in candidates):
            return metric_name

    return None


def detect_dimension(q: str, semantic_layer):
    if not semantic_layer:
        return None

    # 🔥 1. intentar dimensions (si algún día lo agregás)
    dimensions = semantic_layer.get("dimensions", {})

    for dim_name, config in dimensions.items():
        aliases = config.get("aliases", [])
        candidates = [dim_name] + aliases

        if any(alias in q for alias in candidates):
            return dim_name

    # 🔥 2. fallback → aliases globales
    aliases = semantic_layer.get("aliases", {})

    for col, alias_list in aliases.items():
        if isinstance(alias_list, list):
            if any(a in q for a in alias_list):
                return col
        else:
            if alias_list in q:
                return col

    return None




def merge_semantic_layers(base_layer, extra_layer):
    # Si uno es None → devolver el otro
    if not base_layer:
        return extra_layer

    if not extra_layer:
        return base_layer

    merged = {
        "columns": list(set(base_layer.get("columns", []) + extra_layer.get("columns", []))),
        "aliases": {},
        "metrics": {}
    }

    # -------------------------
    # MERGE ALIASES
    # -------------------------
    merged["aliases"] = base_layer.get("aliases", {}).copy()

    for col, values in extra_layer.get("aliases", {}).items():

        existing = merged["aliases"].get(col, [])

        if isinstance(existing, str):
            existing = [existing]

        if isinstance(values, str):
            values = [values]

        merged["aliases"][col] = list(set(existing + values))

    # -------------------------
    # MERGE METRICS
    # -------------------------
    merged["metrics"] = base_layer.get("metrics", {}).copy()

    # 🔥 extra pisa base si hay conflicto
    merged["metrics"].update(extra_layer.get("metrics", {}))

    return merged