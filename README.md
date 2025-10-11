 # UCY: A More Humane Calendar Hiding in Plain Sight

*Last modified: 4024_31_6.1751 UCY*

**UCY** is an alternative calendar system that solves the Gregorian calendar's fractional week problem using 8-day weeks and octal notation. Anchored to astronomical reality while maintaining perfect computational regularity.

## What is UCY?

A calendar system that:
- Contains **complete weeks** in every year (no fractional weeks)
- Uses **8-day weeks** (0-7 in octal notation)
- Creates years of **360 days** (45 weeks) or **368 days** (46 weeks)
- Follows a natural **368-368-360 pattern** (~365.24 day average)
- Anchors to **spring equinoxes** (not arbitrary dates)
- Employs a **measurement-based algorithm** instead of fixed leap year rules
- Exhibits **stability** (repeating 27+ year pattern)

## The Problem UCY Solves

The Gregorian calendar divides 365.2421875 days by 7-day weeks = **52.177... weeks per year**—an eternally fractional value that creates:
- Dates drifting through weekdays
- Complex leap year algorithms
- Irregular months (28/29/30/31 days)
- Week numbers that don't align with year boundaries
- Computational complexity in date arithmetic

**UCY asks**: What if we designed a calendar from mathematical first principles?

## Key Features

### Mathematical Elegance
- **8-day weeks**: Optimal week length enabling complete-week years while tracking the tropical year
- **Octal notation**: Base-8 matches 8-day structure naturally
- **Clean division**: 360÷8=45 weeks, 368÷8=46 weeks (no remainder)
- **No special cases**: No months, no leap day insertions, no irregular patterns

### Astronomical Grounding
- **Datum**: Spring equinox after Julius Caesar's death (March 21, 44 BCE = Year 0)
- **Equinox alignment**: Year starts stay within ~4 days of the equinox and align to 8-day boundaries via a measurement-based threshold (no lookup tables)
- **Dynamic determination**: Measurement-based threshold algorithm (no lookup tables)
- **Deep-time accuracy**: Algorithm tested against astronomical data spanning millennia

### Pattern Stability
- **Natural**: Following astronomical math instead of fixed rules yields a remarkable generational stability
- **Generational**: A simple pattern holds for over 27 years at a time
- **Predictable**: Reducing the cognitive load of calendar tracking from an annual check to a generational one
- **Validated**: Empirical analysis across millennia validates the stability pattern
- **Consistent**: Zero unexpected calendar changes within generational runs

### Computational Efficiency
- **Constant-time calculations**: No iteration through previous years required
- **No lookup tables**: Algorithm adapts dynamically to actual tropical year
- **Clean implementation**: <100 lines of Python

## Installation

```bash
pip install -r requirements.txt
```

**Requirements**: `skyfield`, `pytest`

Note: On first run, Skyfield will download the NASA JPL DE431t ephemeris (~3.5 GB) to ~/.skyfield-data. See [ucy.md](ucy.md) for implementation details and optimization options.

## Usage

```python
from ucy import to_ucy, to_parts, to_utc
import skyfield.api as sf

# Get current UCY date
ts = sf.load.timescale()
now = ts.now()
ucy_date = to_ucy(now.tt)
print(ucy_date)  # e.g., "4024_31_6.1751"

# Get UCY components
year, week, day, nano = to_parts(now.tt)
print(f"Year {year:o}, Week {week:02o}, Day {day:o}")

# Convert UCY back to UTC
utc_iso = to_utc("4024_31_6.1751")
print(utc_iso)  # e.g., 2025-10-11T14:55:34Z
```

## Date Format

UCY dates use octal notation: `year_week_day.fraction`

**Example**: `4024_31_6.1751`
- Year: 4024 (2068 in decimal)
- Week: 31 (25 in decimal)  
- Day: 6
- Fraction: .1751 (position within day)

## Project Structure

```
├── ucy.py                    # Core implementation
├── test_ucy.py               # Test suite
├── test_cases.py             # Test case data
├── generator.py              # Reference table generator
├── ucy.md                    # Main documentation
├── MEDITATION.md             # Philosophical exploration
├── requirements.txt          # Dependencies
└── LICENSE                   # GPL v3
```

## Running Tests

```bash
# Quick check
pytest

# Full suite (include slow tests)
pytest -m ""
```

Tests validate:
- Historical dates
- Deep time accuracy
- Year boundary alignment
- No consecutive short
- Generational stability

## Technical Specifications

| Property | Value |
|----------|-------|
| Week length | 8 days (0-7 octal) |
| Short year | 45 weeks / 360 days |
| Long year | 46 weeks / 368 days |
| Average year | ~365.24 days |
| Notation | Base-8 (octal) throughout |
| Datum | Spring equinox, 44 BCE |
| Algorithm | Measurement-based threshold |
| Pattern stability | 100% of runs ≥27 years long

## Documentation

- **[ucy.md](ucy.md)**: Main documentation with four layers—poetic rules, historical context, technical specs, and philosophical Q&A
- **[MEDITATION.md](MEDITATION.md)**: Deep exploration of time, mathematics, and human systems

## Acknowledgments
- Astronomy computations use Skyfield by Brandon Rhodes
- Ephemerides from NASA JPL (DE431t) accessed via Skyfield
- This project is unaffiliated with NASA/JPL; names are used for attribution

## Comparison: UCY vs Gregorian

| Feature | UCY | Gregorian |
|---------|-----|-----------|
| Complete weeks | ✓ Always | ✗ Never |
| Year length calculation | Constant-time | Algorithm required |
| Month lengths | N/A (no months) | 28/29/30/31 (irregular) |
| Pattern stability | 27 years | Check annually |
| Year length rules | Measurement-based | Complex (÷4, ×100, ÷400) |
| Astronomical anchor | Spring equinox | Arbitrary (Jan 1) |
| Notation | Octal (matches structure) | Decimal |
| Cognitive load | Check once per generation | Check every year |


## Contributing

This is a complete, self-contained reference implementation. To explore:

1. Read the [main documentation](ucy.md)
2. Examine the [implementation](ucy.py)
3. Run the [tests](test_ucy.py)
4. Reflect on the [meditation](MEDITATION.md)

## License

GPL v3 - See [LICENSE](LICENSE) for details.

## Citation

```bibtex
@software{ucy,
  author = {Pat Bierkortte},
  title = {UCY: A More Humane Calendar Hiding in Plain Sight},
  year = {2025},
  url = {https://github.com/pbierkortte/UCY},
  email = {hello@patbierkortte.com}
}
```

---
