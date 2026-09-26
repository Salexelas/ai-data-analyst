MAX_UNIQUE_VALUES = 100

MIN_RELATION_SCORE = 0.8

TEXT_BLACKLIST = {
    "description",
    "comment",
    "text",
    "notes",
    "summary"
}


def normalize_values(values):
    return {
        str(v).strip().lower()
        for v in values
        if str(v).strip()
    }


def relation_score(left_values, right_values):
    """
    Relationship score based on exact overlap.

    1.0 = all values from the smaller set
          exist in the larger set.

    Example:

    {1,2,3}
    {1,2,3,4,5}

    overlap = 3
    score = 3 / min(3,5) = 1.0
    """

    left = normalize_values(left_values)
    right = normalize_values(right_values)

    if not left or not right:
        return 0.0

    overlap = len(left & right)

    denominator = min(
        len(left),
        len(right)
    )

    if denominator == 0:
        return 0.0

    return overlap / denominator


def is_candidate_column(series, column_name):
    """
    Filter obvious text fields and unsuitable columns.
    """

    if column_name.lower() in TEXT_BLACKLIST:
        return False

    if series.dtype != "object":
        return False

    unique_count = series.nunique(dropna=True)

    if unique_count <= 1:
        return False

    if unique_count > 500:
        return False

    avg_len = (
        series.astype(str)
        .str.len()
        .mean()
    )

    return avg_len <= 40


def detect_relationships(datasets):
    """
    Detect relationships between datasets using
    exact value overlap.

    Returns:

    [
        {
            "left_dataset": "...",
            "right_dataset": "...",
            "left_column": "...",
            "right_column": "...",
            "score": 0.95
        }
    ]
    """

    relationships = []

    dataset_names = list(datasets.keys())

    for i in range(len(dataset_names)):

        for j in range(i + 1, len(dataset_names)):

            left_dataset = dataset_names[i]
            right_dataset = dataset_names[j]

            left_df = datasets[left_dataset]["df"]
            right_df = datasets[right_dataset]["df"]

            for lc in left_df.columns:

                if not is_candidate_column(
                    left_df[lc],
                    lc
                ):
                    continue

                left_values = (
                    left_df[lc]
                    .dropna()
                    .astype(str)
                    .unique()[:MAX_UNIQUE_VALUES]
                )

                for rc in right_df.columns:

                    if not is_candidate_column(
                        right_df[rc],
                        rc
                    ):
                        continue

                    right_values = (
                        right_df[rc]
                        .dropna()
                        .astype(str)
                        .unique()[:MAX_UNIQUE_VALUES]
                    )

                    score = relation_score(
                        left_values,
                        right_values
                    )

                    if score >= MIN_RELATION_SCORE:

                        relationships.append({
                            "left_dataset": left_dataset,
                            "right_dataset": right_dataset,
                            "left_column": lc,
                            "right_column": rc,
                            "score": round(score, 2)
                        })

    relationships.sort(
        key=lambda r: r["score"],
        reverse=True
    )

    return relationships