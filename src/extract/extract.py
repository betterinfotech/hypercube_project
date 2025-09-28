import json
import pandas as pd


def load_linear_orders_json(path: str) -> pd.DataFrame:
    """
    Load the API JSON and return a flat DataFrame of result.records.
    Super simple, no error handling.
    """
    with open(path, "r") as f:
        data = json.load(f)

    # Assume standard shape: {"result": {"records": [...]}}
    records = data["result"]["records"]

    df = pd.json_normalize(records)

    # SQL-safe column names
    safe_cols = []
    for c in df.columns:
        if c[0].isalpha() or c[0] == "_":
            safe_cols.append(c)
        else:
            safe_cols.append(f"col_{c}")
    df.columns = safe_cols

    return df


def load_bmrc_wind_forecast_csv(path: str) -> pd.DataFrame:
    # Explicitly name columns to avoid interpreting trailing comma as blank column
    cols = [
        "Column1",
        "recordType",
        "startTimeOfHalfHrPeriod",
        "settlementPeriod",
        "initialForecastPublishingPeriodCommencingTime",
        "initialForecastSpnGeneration",
        "latestForecastPublishingPeriodCommencingTime",
        "latestForecastSpnGeneration",
        "outTurnPublishingPeriodCommencingTime",
        "fuelTypeGeneration",
        "activeFlag",
        "EFA",
    ]
    return pd.read_csv(
        path, header=0, names=cols, usecols=range(len(cols)), keep_default_na=False
    )


def load_staging_frames(linear_orders_path: str, bmrc_wind_forecast_path: str):
    return (
        load_linear_orders_json(linear_orders_path),
        load_bmrc_wind_forecast_csv(bmrc_wind_forecast_path),
    )
