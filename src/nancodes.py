"""Provides unified not-a-number codes for the indicators.

Currently requires a manual sync between the covidcast-indicators
and the utils repos.
* in cmu-delphi/covidcast-indicators: _delphi_utils_python/delphi_utils/
* in cmu-delphi/utils: src/
"""

from enum import IntEnum

class Nans(IntEnum):
    """An enum of not-a-number codes for the indicators."""

    NOT_MISSING = 0
    NOT_APPLICABLE = 1
    REGION_EXCEPTION = 2
    DATA_INSUFFICIENT = 3
    PRIVACY = 4
    UNKNOWN = 5
