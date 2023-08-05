""" Identify tags whose variance drifts continuously on daily average for a month.

<p>It is possible that over time a sensor starts to show more variation in it's measurements
due to wear and tear. An increase in variation can also be caused by underlying process issues
and inherent increase in variation in the system.</p>
<p><img src='../static/images/reporting/daily_variance_drift.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames containing increasing and decreasing variance. E.g. assume a total period being analyzed of 1 year and
2 event-frames, one increasing and one decreasing, of 1 month and 2 months respectively.
The score of this check will then be 75% = 1 - 3 / 12. Which means that in 75% of time no variance drift
is detected.</p>
<div class="ts-check-impact">
<p>
A drift in sensor variation is an indication of instrumentation issues or increased variability in the process.
The longer drift in sensor variation the more variability might be introduced into the system. This variability
typically progresses throughout production and finding the initial root cause after months can be very cumbersome.
Any type of anomaly detection based on normal behavior of the phyiscal ensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

from datetime import timedelta, datetime
from typing import Tuple

import numpy as np
import pandas as pd
import pymannkendall as mk

from pandas.api.types import is_string_dtype

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    DataType,
    EventFrame,
    ModuleParameterType,
)
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
    get_p_value_based_on_sensitivity,
)


META = {
    "checks": [
        {
            "name": "Daily variance drift (increasing)",
            "event_frames": ["Increasing variance"],
        },
        {
            "name": "Daily variance drift (decreasing)",
            "event_frames": ["Decreasing variance"],
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 4,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "parameters": [
        {
            "name": "sensitivity",
            "type": ModuleParameterType.HIDDEN,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Sensitivity influences the p-value for the Mann-Kendall test for slopes.",
        },
    ],
    "signature": "univariate",
}


def _merge_frames(frames: pd.DataFrame) -> pd.DataFrame:
    if len(frames) == 0:
        return frames

    merged_frame = pd.DataFrame(
        {
            "start_date": pd.Series(dtype="datetime64[ns, UTC]"),
            "end_date": pd.Series(dtype="datetime64[ns, UTC]"),
            "type": [],
            "open": [],
        }
    )

    current_start = frames.iloc[0]["start_date"]
    current_end = frames.iloc[0]["end_date"]
    current_type = frames.iloc[0]["type"]
    current_open = frames.iloc[0]["open"]
    for index, row in frames.reset_index(drop=True).iterrows():
        if current_end < row["start_date"]:
            merged_frame = pd.concat(
                [
                    merged_frame,
                    pd.DataFrame(
                        {
                            "start_date": [current_start],
                            "end_date": [current_end],
                            "type": [current_type],
                            "open": [current_open],
                        }
                    ),
                ]
            )
            current_start = row["start_date"]
        if index == len(frames) - 1:
            if current_end < row["start_date"]:
                merged_frame = pd.concat(
                    [
                        merged_frame,
                        pd.DataFrame(
                            {
                                "start_date": [row["start_date"]],
                                "end_date": [row["end_date"]],
                                "type": [row["type"]],
                                "open": [row["open"]],
                            }
                        ),
                    ]
                )
            else:
                merged_frame = pd.concat(
                    [
                        merged_frame,
                        pd.DataFrame(
                            {
                                "start_date": [current_start],
                                "end_date": [row["end_date"]],
                                "type": [current_type],
                                "open": row["open"],
                            }
                        ),
                    ]
                )

        current_end = row["end_date"]
        current_type = row["type"]
        current_open = row["open"]
    merged_frame["open"] = merged_frame["open"].astype("bool")
    return merged_frame


def _calculate_total_slope_time(frames: pd.DataFrame) -> timedelta:
    total_time = timedelta(0)
    for _, row in frames.iterrows():
        total_time = total_time + (
            row["end_date"] - (row["start_date"] + timedelta(days=28))
        )
    return total_time


def _get_global_outliers(df: pd.DataFrame) -> Tuple[float, float]:
    q25, q75 = np.quantile(df, [0.25, 0.75])
    iqr = q75 - q25
    upper = q75 + 1.5 * iqr
    lower = q25 - 1.5 * iqr
    return lower, upper


def _apply_mk(
    df: pd.DataFrame, lower: float, upper: float, alpha: float = 1e-5
) -> float:
    if any(df > upper) or any(df < lower):
        return 0

    values = df.values
    q25, q75 = np.quantile(values, [0.25, 0.75])
    iqr = q75 - q25
    values[(values > q75 + 1.5 * iqr) | (values < q25 - 1.5 * iqr)] = np.nan
    values = values[~np.isnan(values)]
    values = values[np.insert(np.diff(values).astype(bool), 0, True)]

    if len(values) <= 20:
        return 0
    result = mk.original_test(values, alpha=alpha)
    if result.trend == "no trend":
        return 0
    if result.trend == "increasing":
        return 1
    return -1


def _get_intervals(
    df: pd.DataFrame, anomalies: pd.Series, interval_type: str
) -> pd.DataFrame:
    anomaly_grp = (anomalies != anomalies.shift().bfill()).cumsum()
    intervals = (
        df.assign(anomaly_grp=anomaly_grp)[anomalies]
        .reset_index()
        .groupby(["anomaly_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["start_date"] = intervals["start_date"] - timedelta(days=27)
    intervals["type"] = interval_type
    return intervals


def _get_last_analyzed_point(df: pd.DataFrame) -> datetime | None:
    points_before_last_analysis = df.index[
        df.index <= df.index[-1] - timedelta(days=27)
    ]
    if len(points_before_last_analysis) <= 1:
        return None
    return points_before_last_analysis[-2].to_pydatetime()


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _get_slopes(analysis_input, df_daily, lower, upper):
    if "sensitivity" not in analysis_input.parameters:
        return df_daily.rolling(28).apply(lambda x: _apply_mk(x, lower, upper))

    return df_daily.rolling(28).apply(
        lambda x: _apply_mk(
            x,
            lower,
            upper,
            get_p_value_based_on_sensitivity(analysis_input.parameters["sensitivity"]),
        )
    )


def _run_drift_check(  # pylint: disable=too-many-locals
    analysis_input: AnalysisInput,
) -> tuple[list[EventFrame], datetime | None]:
    df = _clean_dataframe(analysis_input.data)

    df_daily = df.resample("1D").std()
    lower, upper = _get_global_outliers(df_daily)
    slopes = _get_slopes(analysis_input, df_daily, lower, upper)

    pos_slopes = slopes["value"] == 1
    neg_slopes = slopes["value"] == -1

    inc_intervals = _get_intervals(df_daily, pos_slopes, "Increasing variance")
    dec_intervals = _get_intervals(df_daily, neg_slopes, "Decreasing variance")
    inc_intervals = handle_open_intervals(df_daily, inc_intervals)
    dec_intervals = handle_open_intervals(df_daily, dec_intervals)

    minc = _merge_frames(inc_intervals)
    mdec = _merge_frames(dec_intervals)

    all_intervals = pd.concat((minc, mdec))

    all_frames = event_frames_from_dataframe(process_open_intervals(all_intervals))

    last_analyzed_point = _get_last_analyzed_point(df)

    return list(all_frames), last_analyzed_point


def _is_valid_input(data: pd.DataFrame) -> tuple[str, bool]:
    df = _clean_dataframe(data)
    if len(df) < 2:
        return "Not enough data", False
    if (df.index[-1] - df.index[0]) < timedelta(weeks=4):
        return "Not enough weeks of data", False
    if len(df["value"].unique()) <= 3:
        return "Not enough unique values", False
    if is_string_dtype(df["value"]):
        return "Can not be a string", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input.data)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    frames, last_analyzed_point = _run_drift_check(analysis_input)

    return AnalysisResult(
        event_frames=frames,
        last_analyzed_point=last_analyzed_point,
    )
