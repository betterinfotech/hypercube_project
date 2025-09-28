import pandas as pd
from typing import Tuple
from .schemas import BMRSWindRow


def transform_linear_orders(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # TO DO - Check data and create Pydantic class if necessary for transform.
    return df.copy(), pd.DataFrame()


def transform_bmrc_forecast(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    This code makes use of Pydantic to validate and transform the BMRC data
    - ISO date transformation
    """
    clean_rows, error_rows = [], []

    for idx, row in df.iterrows():
        data = row.to_dict()
        try:
            obj = BMRSWindRow.model_validate(data)
            clean_rows.append(obj.model_dump())
        except Exception as e:
            bad = dict(data)
            bad["_row_index"] = idx
            bad["_error"] = str(e)
            error_rows.append(bad)

    clean = pd.DataFrame(clean_rows)
    errors = pd.DataFrame(error_rows)

    return clean, errors


def merge_lo_bmrs(
    linear_orders_pd: pd.DataFrame,
    bmrs_wind_forecast_pd: pd.DataFrame,
) -> pd.DataFrame:
    """
    - Merge linear_orders and BMRS forecast into one DataFrame.
    - Join on DeliveryStart (linear_orders) and outTurnPublishingPeriodCommencingTime (BMRS).
    - TO DO: Add error checking.
    """
    merged = pd.merge(
        linear_orders_pd,
        bmrs_wind_forecast_pd,
        left_on="DeliveryStart",
        right_on="outTurnPublishingPeriodCommencingTime",
        how="inner",
    )
    return merged
