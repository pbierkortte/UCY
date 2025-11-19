# UCY

import math, re
from functools import lru_cache
from typing import Optional, Tuple
from skyfield import almanac
from skyfield.api import Loader

FAST_MODE = False  # Use a fixed constant for the mean year
FAST_MIN_YEAR, FAST_MAX_YEAR = 1843, 2243  # 1800 to 2200 AD
TROPICAL_YEAR_DAYS = 365.24224853515625  # octal 0o555.17402
DAY_NS = 86_400_000_000_000
WEEK_DAYS = 8.0
EPSILON = 1e-9

loader = Loader("~/.skyfield-data")
eph = loader("de431t.bsp")
ts = loader.timescale()
seasons = almanac.seasons(eph)


@lru_cache()
def get_equinox_by_year(ucy_year: int) -> float:
    """Return spring equinox TT (Julian days) for given UCY year."""
    gregorian_year = ucy_year - 43
    t0, t1 = ts.utc(gregorian_year, 3, 1), ts.utc(gregorian_year, 4, 1)
    times, codes = almanac.find_discrete(t0, t1, seasons, EPSILON)
    return min(time.tt for time, code in zip(times, codes) if code == 0)


# Datum: Spring equinox after Caesar's death (March 21, 44 BCE ~9:04 AM UTC)
DATUM_TT = get_equinox_by_year(0)


@lru_cache(maxsize=4096)
def is_short_year(ucy_year: int) -> Tuple[bool, float, int]:
    """Determine if UCY year is short (360d) or long (368d)"""
    if FAST_MODE and FAST_MIN_YEAR <= ucy_year <= FAST_MAX_YEAR:
        next_equinox = DATUM_TT + ((ucy_year + 1) * TROPICAL_YEAR_DAYS)
        threshold = 4.0 - (368 - TROPICAL_YEAR_DAYS)
    else:
        year_equinox = get_equinox_by_year(ucy_year)
        next_equinox = get_equinox_by_year(ucy_year + 1)
        actual_year = next_equinox - year_equinox
        threshold = 4.0 - (368 - actual_year)
    phase = (next_equinox - DATUM_TT) % WEEK_DAYS
    is_short = threshold <= phase < 4.0
    year_size = 360 if is_short else 368
    offset = 360 if phase > threshold else 368
    year_start_tt = next_equinox - phase - offset
    return is_short, year_start_tt, year_size


def to_parts(jd_tt: Optional[float] = None) -> Tuple[int, int, int, int]:
    """Convert TT (Julian days) to UCY parts"""
    jd_tt = jd_tt or ts.now().tt
    total_elapsed_days = jd_tt - DATUM_TT
    year = int(total_elapsed_days / TROPICAL_YEAR_DAYS)
    is_short, year_start_tt, _ = is_short_year(year)
    if jd_tt < year_start_tt:
        year -= 1
        is_short, year_start_tt, _ = is_short_year(year)
    elif jd_tt >= is_short_year(year + 1)[1]:
        year += 1
        is_short, year_start_tt, _ = is_short_year(year)
    days_into_year = jd_tt - year_start_tt
    week = math.floor(days_into_year / 8)
    if is_short and week < 45:
        week += 1
    if not is_short and year >= 0:
        if 0.0 < (360.0 - days_into_year) < (2.0 / 86400.0):
            week = 45
    week = min(week, 45)
    day = math.floor(total_elapsed_days % 8)
    nano = math.floor((total_elapsed_days % 1) * DAY_NS)
    return int(year), int(week), int(day), int(nano)


def to_ucy(tt: float) -> str:
    """Convert TT (Julian days) to UCY octal string format."""
    year, week, day, nano = to_parts(tt)
    frac = (nano * 8**4) // DAY_NS
    return f"{year:o}_{week:02o}_{day:o}.{frac:04o}".replace("-", "0")


def to_utc(ucy: str) -> str:
    """Convert a UCY octal string to a UTC ISO 8601 string"""
    year, week, day, frac = re.split(r"[_.]", ucy)
    year_abs, week, day, frac = map(lambda s: int(s, 8), [year, week, day, frac])
    year_int = -year_abs if year.startswith("0") else year_abs
    is_short, year_start_tt, _ = is_short_year(year_int)
    week_index = week - 1 if is_short and week > 0 else week
    base_days = (year_start_tt - DATUM_TT) + (week_index * 8)
    day_offset = (day - (base_days % 8)) % 8
    total_days = base_days + day_offset + (frac / 8**4)
    return ts.tt_jd(DATUM_TT + total_days).utc_iso()


if __name__ == "__main__":
    print("Now:", to_ucy(ts.now().tt), "UCY")
