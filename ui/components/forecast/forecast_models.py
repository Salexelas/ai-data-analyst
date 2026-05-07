import pandas as pd


def simple_forecast(df, y_col, periods):

    last_value = df[y_col].iloc[-1]

    future = pd.DataFrame({

        y_col: [last_value] * periods
    })

    return future