def build_semantic_layer(
    columns,
    aliases=None,
    metrics=None,
    dimensions=None,
):
    return {
        "columns": columns,
        "aliases": aliases or {},
        "metrics": metrics or {},
        "dimensions": dimensions or {},
    }


def normalize_aliases(values):
    if values is None:
        return []

    if isinstance(values, str):
        return [values]

    return values


def aliases_match(query, aliases):
    return any(
        alias in query
        for alias in normalize_aliases(aliases)
    )


def find_by_alias(query, items):
    for name, config in items.items():
        candidates = [name] + normalize_aliases(
            config.get("aliases")
        )

        if aliases_match(query, candidates):
            return name

    return None


def detect_metric(query, semantic_layer):
    if not semantic_layer:
        return None

    return find_by_alias(
        query,
        semantic_layer.get("metrics", {}),
    )


def detect_dimension(query, semantic_layer):
    if not semantic_layer:
        return None

    dimension = find_by_alias(
        query,
        semantic_layer.get("dimensions", {}),
    )

    if dimension:
        return dimension

    aliases = {
        column: {
            "aliases": normalize_aliases(values)
        }
        for column, values in semantic_layer.get(
            "aliases", {}
        ).items()
    }

    return find_by_alias(query, aliases)


def merge_aliases(base_aliases, extra_aliases):
    merged = base_aliases.copy()

    for column, values in extra_aliases.items():
        existing = normalize_aliases(
            merged.get(column)
        )

        merged[column] = list(
            dict.fromkeys(
                existing
                + normalize_aliases(values)
            )
        )

    return merged


def merge_semantic_layers(base_layer, extra_layer):
    if not base_layer:
        return extra_layer

    if not extra_layer:
        return base_layer

    return {
        "columns": list(
            dict.fromkeys(
                base_layer.get("columns", [])
                + extra_layer.get("columns", [])
            )
        ),
        "aliases": merge_aliases(
            base_layer.get("aliases", {}),
            extra_layer.get("aliases", {}),
        ),
        "metrics": {
            **base_layer.get("metrics", {}),
            **extra_layer.get("metrics", {}),
        },
        "dimensions": {
            **base_layer.get("dimensions", {}),
            **extra_layer.get("dimensions", {}),
        },
    }