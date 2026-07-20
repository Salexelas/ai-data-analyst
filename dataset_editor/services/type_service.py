import pandas as pd


TYPE_OPTIONS = [
    "auto",
    "text",
    "number",
    "datetime",
    "boolean",
    "category",
    "id"
]


class TypeService:

    DETECTION_RULES = [
        ("datetime", "datetime"),
        ("bool", "boolean"),
        ("int", "number"),
        ("float", "number"),
    ]

    CONVERTERS = {
        "datetime": (
            pd.to_datetime,
            {
                "dayfirst": True,
                "errors": "coerce",
            },
        ),
        "number": (
            pd.to_numeric,
            {
                "errors": "coerce",
            },
        ),
        "category": (
            pd.Series.astype,
            {
                "dtype": "category",
            },
        ),
        "text": (
            pd.Series.astype,
            {
                "dtype": "string",
            },
        ),
    }

    @staticmethod
    def detect(series):

        dtype = str(series.dtype)

        for pattern, detected_type in TypeService.DETECTION_RULES:

            if pattern in dtype:
                return detected_type

        return "text"

    @staticmethod
    def _to_boolean(series):

        return (
            series
            .astype("string")
            .str.strip()
            .str.lower()
            .map({
                "true": True,
                "false": False,
                "1": True,
                "0": False,
                "yes": True,
                "no": False,
            })
        )

@staticmethod
def apply(df, schema):

    df = df.copy()

    for col, dtype in schema.items():

        if col not in df.columns:
            continue

        TypeService._apply_column(df, col, dtype)

    return df


@staticmethod
def _apply_column(df, col, dtype):

    try:

        if dtype == "boolean":
            df[col] = TypeService._to_boolean(df[col])
            return

        converter = TypeService.CONVERTERS.get(dtype)

        if not converter:
            return

        func, kwargs = converter

        df[col] = func(df[col], **kwargs)

    except (ValueError, TypeError):
        pass