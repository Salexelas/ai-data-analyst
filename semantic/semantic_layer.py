def build_semantic_layer(columns, aliases=None, metrics=None):

    return {
        "columns": columns,
        "aliases": aliases or {},
        "metrics": metrics or {}
    }