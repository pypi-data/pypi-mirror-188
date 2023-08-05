"""The series should have upper operating limits.

<p>Each sensor or lab measuring equipment has an inherent measurement range. Outside of this range
the readings from the sensor can't be relied on. This information is typically present in the
sensor specification sheet.
Traditional historians also allow setting limits (often Low-Low, Low, High and High-High limits).
These limits are often based on process safety concerns or indeed taken from the normal operating range.
In all cases having access to these limits is essential for interpreting readings from the equipment.</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).
This check belongs to the score group Unit.
If this check is True, it means that the score for group Unit will be 0%.</p>
<div class="ts-check-impact">
<p>Missing or badly configured limits can cause missing warning signs of abnormal situations both
in the process as well as with the instrumentation.
</p>
</div>
"""

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.metadata import fields

_CHECK_NAME = "Upper limit is present"
_EVENT_FRAME_NAME = "Upper limit is present"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "group": "Limits - Physical",
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [
        {"min_series": 1, "data_type": [DataType.FLOAT32, DataType.FLOAT64]}
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    limit_high = analysis_input.metadata.get_field(fields.LimitHighPhysical)

    event_frames = []
    if limit_high is None:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=None,
            )
        )
    return AnalysisResult(event_frames=event_frames)
