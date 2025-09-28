from typing import Optional, Any
from pydantic import BaseModel, conint, field_validator
import pandas as pd


class BMRSWindRow(BaseModel):
    Column1: Optional[Any] = None
    recordType: Optional[Any] = None

    # These get normalized to ISO 8601 strings
    startTimeOfHalfHrPeriod: str
    initialForecastPublishingPeriodCommencingTime: Optional[str] = None
    latestForecastPublishingPeriodCommencingTime: Optional[str] = None
    outTurnPublishingPeriodCommencingTime: str  # REQUIRED & must not be NaT

    settlementPeriod: conint(gt=0)

    initialForecastSpnGeneration: Optional[int] = None
    latestForecastSpnGeneration: Optional[Any] = None
    fuelTypeGeneration: Optional[Any] = None
    activeFlag: Optional[Any] = None
    EFA: Optional[Any] = None

    # Hard rule: reject "NULL"/"NaN" and coerce to int
    @field_validator("initialForecastSpnGeneration", mode="before")
    @classmethod
    def _initial_forecast_int(cls, v):
        if v in ("NULL", "NaN"):
            raise ValueError('initialForecastSpnGeneration must not be "NULL"/"NaN"')
        return int(v)

    # outTurn must not be empty or NaT (literal or pandas NaT)
    @field_validator("outTurnPublishingPeriodCommencingTime", mode="before")
    @classmethod
    def _require_outturn(cls, v):
        # Reject blank
        if isinstance(v, str) and v.strip() == "":
            raise ValueError("outTurnPublishingPeriodCommencingTime is required")
        # Reject literal "NaT"
        if isinstance(v, str) and v.strip().upper() == "NAT":
            raise ValueError('outTurnPublishingPeriodCommencingTime must not be "NaT"')
        # Reject pandas NaT
        if v is pd.NaT:
            raise ValueError("outTurnPublishingPeriodCommencingTime must not be NaT")
        return v

    # Normalize the 4 datetime fields to ISO 8601
    @field_validator(
        "startTimeOfHalfHrPeriod",
        "initialForecastPublishingPeriodCommencingTime",
        "latestForecastPublishingPeriodCommencingTime",
        "outTurnPublishingPeriodCommencingTime",
        mode="before",
    )
    @classmethod
    def _to_iso(cls, v):
        # v is guaranteed non-empty for outTurn by the validator above
        dt = pd.to_datetime(v, dayfirst=True, errors="raise")
        # Be sure to refuse NaT if pandas returns it without raising
        if pd.isna(dt):
            raise ValueError("Invalid datetime (NaT)")
        return dt.isoformat()
