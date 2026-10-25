def apply_aggregation(
    df,
    x_col,
    y_col,
    aggregation,
    group_col
):

    # ==================================================
    # NO AGG
    # ==================================================
    if aggregation == "none":

        return df, y_col

    # ==================================================
    # COUNT
    # ==================================================
    if aggregation == "count":

        if group_col != "Sin grupo":

            result = (
                df
                .groupby([x_col, group_col])
                .size()
                .reset_index(name="count")
            )

        else:

            result = (
                df
                .groupby(x_col)
                .size()
                .reset_index(name="count")
            )

        return result, "count"

    # ==================================================
    # OTHER AGGS
    # ==================================================
    if group_col != "Sin grupo":

        result = (
            df
            .groupby([x_col, group_col])[y_col]
            .agg(aggregation)
            .reset_index()
        )

    else:

        result = (
            df
            .groupby(x_col)[y_col]
            .agg(aggregation)
            .reset_index()
        )

    return result, y_col