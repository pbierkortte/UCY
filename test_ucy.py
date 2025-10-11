# Tests For UCY

import pytest, random
from datetime import datetime
from ucy import DAY_NS, ts, is_short_year, to_parts, to_ucy, to_utc
from test_cases import TEST_CASES, YEAR_LENGTH_CASES

random.seed(45)


@pytest.mark.parametrize("test_name", TEST_CASES.keys())
def test_ucy_conversions(test_name):
    """Test UCY calendar conversions"""
    jd, exp_year, exp_week, exp_day, exp_nano = TEST_CASES[test_name]

    year, week, day, nano = to_parts(jd.tt)
    ucy_string = to_ucy(jd.tt)
    iso_string = jd.utc_iso(places=9)
    unix_seconds = round((jd.tt - 2440587.5) * 86400)

    columns = [
        "ucy_string",
        "desc",
        "ucy",
        "tt",
        "iso",
        "unix",
        "year",
        "week",
        "day",
        "nano",
    ]
    values = [
        ucy_string,
        test_name,
        ucy_string,
        jd.tt,
        iso_string,
        unix_seconds,
        year,
        week,
        day,
        nano,
    ]

    print()
    for column, value in zip(columns, values):
        print(f"  {column}: {value}")

    assert year == exp_year, f"Year mismatch for {test_name}"
    assert week == exp_week, f"Week mismatch for {test_name}"
    assert day == exp_day, f"Day mismatch for {test_name}"

    error_msg = f"Nano mismatch for {test_name}: got {nano}, expected {exp_nano}"
    assert nano == exp_nano, error_msg


@pytest.mark.parametrize("year_num,expected_days", YEAR_LENGTH_CASES)
def test_year_lengths(year_num, expected_days):
    """Test that years are correctly identified as 360 or 368 days"""
    is_short, _, _ = is_short_year(year_num)

    expected_short = expected_days == 360

    year_type = "short (360)" if is_short else "long (368)"
    print(f"\nYear {year_num}: {year_type}, expected {expected_days} days")

    error_msg = f"Year {year_num} should be {expected_days} days (short={expected_short}) but is_short_year returned {is_short}"
    assert is_short == expected_short, error_msg


def test_valid_parts():
    """Test parts remain within valid bounds"""
    for i in range(4096):
        current_tt = TEST_CASES["Datum Exact"][0].tt + i + random.random()
        ucy_year, week, day, nano = to_parts(current_tt)
        is_within_bounds = 0 <= week <= 45 and 0 <= day <= 7 and 0 <= nano < DAY_NS
        error_msg = f"UCY year {ucy_year}: week={week} day={day} nano={nano} out of bounds at TT={current_tt:.9f}"
        assert is_within_bounds, error_msg


@pytest.mark.slow
def test_consecutive_years():
    """Test for no consecutive 360 day years occur"""

    consecutive_pairs = []

    for ucy_year in range(-250, 251):
        this_is_short, _, _ = is_short_year(ucy_year)
        next_is_short, _, _ = is_short_year(ucy_year + 1)

        if this_is_short and next_is_short:
            consecutive_pairs.append((ucy_year, ucy_year + 1))

    error_msg = f"Found {len(consecutive_pairs)} consecutive short year pairs: {consecutive_pairs}"
    assert len(consecutive_pairs) == 0, error_msg


@pytest.mark.slow
def test_generational_stability():
    """Validates that all LLS pattern runs are at least 27 years long."""
    lls_count = 0
    ucy_year = 16

    while ucy_year < 4096:
        n0, _, _ = is_short_year(ucy_year)
        n1, _, _ = is_short_year(ucy_year + 1)
        n2, _, _ = is_short_year(ucy_year + 2)

        is_lls = not n0 and not n1 and n2

        if lls_count == 0:
            lls_count += 27
            ucy_year += 27
        elif is_lls:
            lls_count += 3
            ucy_year += 3
        elif lls_count >= 27:
            lls_count = 0
            ucy_year += 2
        else:
            error_msg = f"Found LLS run of only {lls_count} years"
            pytest.fail(error_msg)


def test_round_trip():
    """Round-trip diff should be within 30 seconds"""
    tt = 2222222.222222222
    ucy = to_ucy(tt)
    utc_str = to_utc(ucy)
    dt_obj = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    out_tt = ts.from_datetime(dt_obj).tt
    diff_seconds = abs((tt - out_tt) * 86400.0)
    error_msg = f"Roundtrip difference is {diff_seconds} seconds"
    assert diff_seconds < 30.0, error_msg
