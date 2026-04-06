def build_semantic_layer(columns, aliases=None, metrics=None):
    return {
        "columns": columns,
        "aliases": aliases or {},
        "metrics": metrics or {}
    }


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
        if col in merged["aliases"]:
            merged["aliases"][col] = list(set(merged["aliases"][col] + values))
        else:
            merged["aliases"][col] = values

    # -------------------------
    # MERGE METRICS
    # -------------------------
    merged["metrics"] = base_layer.get("metrics", {}).copy()

    # 🔥 extra pisa base si hay conflicto
    merged["metrics"].update(extra_layer.get("metrics", {}))

    return merged