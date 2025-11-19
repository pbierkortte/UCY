"""UCY reference table generator - produces comprehensive CSV mapping UCY dates to TT/UTC"""

import math
from dataclasses import dataclass
from skyfield import almanac
from skyfield.api import Loader

DAY_NS = 86_400_000_000_000
TROPICAL_YEAR_DAYS = 365.2421875
WEEK_DAYS = 8.0
EPSILON = 1e-9

loader = Loader("~/.skyfield-data")
eph = loader("de431t.bsp")
ts = loader.timescale()
seasons = almanac.seasons(eph)


@dataclass
class UCYGenerator:
    """UCY calendar reference table generator.

    Attributes:
        num_years: Number of years to generate (3000 for >1 million days)
        output_file: Output filename for the reference table
    """

    num_years: int = 3000
    output_file: str = "one_million_days.txt"

    def __post_init__(self):
        UCYGenerator._equinox_cache: dict = {}

    def _get_equinox_by_year(self, ucy_year: int) -> float:
        """Get spring equinox TT for a given UCY year."""
        if ucy_year in UCYGenerator._equinox_cache:
            return UCYGenerator._equinox_cache[ucy_year]

        gregorian_year = ucy_year - 43
        t0 = ts.utc(gregorian_year, 3, 1)
        t1 = ts.utc(gregorian_year, 4, 1)
        times, codes = almanac.find_discrete(t0, t1, seasons, EPSILON)
        result = min(time.tt for time, code in zip(times, codes) if code == 0)

        UCYGenerator._equinox_cache[ucy_year] = result
        return result

    def _is_short_year(self, ucy_year: int) -> bool:
        """Determine if UCY year is short (360 days) or long (368 days)."""
        year_equinox = self._get_equinox_by_year(ucy_year)
        next_equinox = self._get_equinox_by_year(ucy_year + 1)
        actual_year = next_equinox - year_equinox
        threshold = 4.0 - (368 - actual_year)
        datum_tt = self._get_equinox_by_year(0)
        phase = (next_equinox - datum_tt) % WEEK_DAYS
        return threshold <= phase < 4.0

    def generate(self) -> None:
        """Generate UCY reference table CSV."""
        lines = []
        lines.append(
            "day_index,start_tt,end_tt,ucy_year,ucy_week,ucy_day,start_nano,end_nano,start_ucy,end_ucy,start_utc,end_utc\n"
        )

        year_start_day = 0

        for ucy_year in range(0, self.num_years):
            is_short = self._is_short_year(ucy_year)
            year_size = 360 if is_short else 368

            for ucy_week in range(0, 46):
                if is_short and ucy_week == 0:
                    continue

                for ucy_day in range(0, 8):
                    if is_short:
                        day_in_year = (ucy_week - 1) * 8 + ucy_day
                    else:
                        day_in_year = ucy_week * 8 + ucy_day

                    total_days = year_start_day + day_in_year - EPSILON
                    end_nano_actual = math.floor((total_days % 1) * DAY_NS)
                    start_nano_actual = 0

                    datum_tt = self._get_equinox_by_year(0)
                    day_boundary = year_start_day + day_in_year
                    start_tt = datum_tt + day_boundary
                    end_tt = datum_tt + day_boundary + 1 - EPSILON

                    week_oct = f"{ucy_week:02o}"
                    day_oct = f"{ucy_day:o}"

                    start_nano = 0
                    frac_start = (start_nano * 8**4) // DAY_NS
                    nano_oct_start = f"{frac_start:04o}"
                    start_ucy = (
                        f"{ucy_year:o}_{week_oct}_{day_oct}.{nano_oct_start}".replace(
                            "-", "0"
                        )
                    )

                    end_nano = DAY_NS - 1
                    frac_end = (end_nano * 8**4) // DAY_NS
                    nano_oct_end = f"{frac_end:04o}"
                    end_ucy = (
                        f"{ucy_year:o}_{week_oct}_{day_oct}.{nano_oct_end}".replace(
                            "-", "0"
                        )
                    )

                    start_utc = ts.tt_jd(start_tt).utc_iso()
                    end_tt_adjusted = end_tt - (1.0 / 86400.0)
                    end_utc = ts.tt_jd(end_tt_adjusted).utc_iso()

                    day_index = year_start_day + day_in_year

                    lines.append(
                        f"{day_index},{start_tt:.9f},{end_tt:.9f},{ucy_year},{ucy_week},{ucy_day},"
                        f"{start_nano_actual},{end_nano},{start_ucy},{end_ucy},{start_utc},{end_utc}\n"
                    )

            year_start_day += year_size

        with open(self.output_file, "w") as f:
            f.writelines(lines)

        print(
            f"Done. Generated {self.num_years} years ({year_start_day} days) to {self.output_file}"
        )


if __name__ == "__main__":
    generator = UCYGenerator(num_years=3000, output_file="3000_years_bedrock_data.txt")
    generator.generate()
