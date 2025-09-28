from src.extract import load_staging_frames
from src.transform import (
    transform_linear_orders,
    transform_bmrc_forecast,
    merge_lo_bmrs,
)
from src.load import load_to_sqlite, reset_sqlite


def main():
    reset_sqlite("etl.db")

    # TO DO: Remove hard coded paths
    linear_orders_path = "data/linear_orders_raw.json"
    bmrc_wind_forecast_path = "data/bmrs_wind_forecast_pair.csv"

    # Extract
    lo_raw, bmrc_raw = load_staging_frames(linear_orders_path, bmrc_wind_forecast_path)

    # Transform
    linear_orders_pd, linear_orders_errors_pd = transform_linear_orders(lo_raw)
    bmrs_wind_forecast_pd, bmrc_wind_forecast_errors_pd = transform_bmrc_forecast(
        bmrc_raw
    )
    # Merge
    lo_bmrs_merge_pd = merge_lo_bmrs(linear_orders_pd, bmrs_wind_forecast_pd)

    # Load
    load_to_sqlite(linear_orders_pd, "linear_orders")
    load_to_sqlite(linear_orders_errors_pd, "linear_orders_errors")
    load_to_sqlite(bmrs_wind_forecast_pd, "bmrs_wind_forecast")
    load_to_sqlite(bmrc_wind_forecast_errors_pd, "bmrc_wind_forecast_errors")
    load_to_sqlite(lo_bmrs_merge_pd, "lo_bmrs_merge")

    print("Done. Check etl.db for results.")


if __name__ == "__main__":
    main()
