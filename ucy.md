# UCY

UCY is how those without shadows play hide and seek with the sun.

How? It's so easy!

Just follow these four simple rules:

Rules:
- Days cycle endlessly in octal sequence 0-7 without interruption
- Weeks contain exactly eight days (0-7); weeks are numbered 00-55 in octal in long years (short years hide week 00)
- Years always end on Week 45 Day 7 (decimal; week 55 in octal) on or about the day of the equinox
- Zero stays within four sunrises of spring out of fear of the number 4

***

## Why

For 2000+ years we've patched around the fact that 365÷7 is fractional. The optimal solution was always available but never chosen because we prioritized tradition over truth.

***

## Past Calendar Systems

### Lunar Months

Moon waxes and wanes in ~29.5 days. Count months by moon cycles.

Problem: 12 lunar months = 354 days. Drifts 11 days per year from solar seasons.

Beautiful. Observable. Incomplete.

***

### 7-Day Weeks

Julius Caesar's calendar: 365.25 days, 7-day weeks.

Seven days named after celestial bodies: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn.

Problem: 365 ÷ 7 = 52.14 weeks (fractional). Years never contain complete weeks.

Orderly. Traditional. Doesn't divide evenly.

***

### Gregorian Calendar

Pope Gregory XIII (1582): Fix Easter calculations without changing structure.

Must keep:
- 7-day weeks (biblical)
- 12 months (Roman)
- March 20 equinox (church)

Solution: Leap years ÷4, except centuries, except ÷400.

Result: Feb 29 breaks rhythm. Dates drift through weekdays. Months vary (28-31 days).

Functions. Approximate. Patched.

***

## UCY

What if we started over? Recognize the solution that was always there.

Design Principles:
- Abandons the lunar month entirely
- Year begins on equinox (not "equinox falls on March 20")
- 8-day weeks (only length where both 360÷8=45 and 368÷8=46)
- 360 or 368 day years
- 45 or 46 complete weeks
- Pure octal notation
- No leap rules (astronomy decides)

Remembered. Humane. Reframed.

***

## Technical

A calendar with complete weeks.

### Datum

Year zero begins at the spring equinox after Julius Caesar's death (March 21, 44 BCE). This moment anchors all UCY time calculations.

### Year Length Determination

Each year is either 360 days (short) or 368 days (long). The system uses astronomy to decide, not lookup tables or formulas. A pure mathematical rule based on equinox phase determines year length in constant time, without needing to calculate previous years.

Key constraints:
- No two consecutive short years
- Years average ≈365.24 days; common rhythm 368-368-360 averages 365.33 days
- Distribution: ~65% long years, ~35% short years (because 365.24 is closer to 368 than 360)

### Year Structure

Short years: 360 days = 45 weeks (weeks 1-45)
Long years: 368 days = 46 weeks (weeks 0-45)

Date Format: `year_week_day.fraction` (all octal)  
Example: `4024_31_6.1751`

Hierarchy: Days (0-7) → Weeks (0-45 or 1-45) → Years. No months.

### Negative Years

Dates before the datum (44 BCE) produce negative year numbers. The minus sign is replaced with "0" in the string format.

Examples:
- Ugarit Eclipse (1222 BCE): 02234_53_3 UCY
- Distant past (9000 BCE): 021376_43_3 UCY

Zero marks the past. Calculation remains continuous across the boundary.

### Week Zero Hiding

Short years hide week 0 to maintain year-end alignment. All years end on Week 45 Day 7. Like hide and seek, week 0 plays when the year is long, hides when the year is short.

### Equinox Snapping

Year starts are aligned to 8-day boundaries referenced to the datum and stay within approximately four days of the spring equinox. In this reference implementation, the year type (360 vs 368) is determined directly from measured equinoxes via a threshold rule, which keeps the alignment close to the equinox without explicitly computing a snapped boundary.

### Implementation Details

This reference implementation sets `FAST_MODE=False` to prioritize astronomical accuracy for validation purposes. The code measures actual spring equinoxes using NASA JPL ephemerides via the Skyfield library, ensuring precision across deep time.

### Optional Fast Mode (Experimental)

The code includes an optional `FAST_MODE` optimization that uses a constant approximation for years 1800-2200 AD, falling back to measured equinoxes outside this range. This maintains accuracy while improving performance for contemporary dates without affecting the calendar's fundamental properties. Consider FAST_MODE experimental.

### Production Optimization

For production applications, the entire calendar logic can be replaced with a pre-computed lookup table, expressing 10,000+ years of calendar data in <1 kilobyte of storage and making the Skyfield dependency optional.

### Why Eight

Core requirements:
- Both short and long year must divide into complete weeks
- Average year length ≈365 days (Earth's tropical year)
- Week length practical for human use

Starting with 360 days as short year (many factors, divides cleanly), seven week lengths work mathematically: 6, 8, 9, 10, 12, 15, and 18 days. Each creates a different long year that brackets the tropical year.

Why eight wins:
- Practical: While the 7-day week is dominant today, its preference stems largely from historical and religious tradition, not from proof of being the single most optimal structure for human rhythms. An 8-day cycle, or nundinum, was common in Etruscan and Roman culture, demonstrating its practicality.
- Balanced: Pattern 368-368-360 averages (368+368+360)÷3 = 365.33 days
- Notation: Base-8 (octal) already exists and maps to binary
- Drift: Minimal equinox drift, maximum stability

Other options fail: Six creates excessive granularity (60 weeks per year). Nine and larger create drift and lack established notation systems. Ten loses the pattern-matching elegance of octal.

Eight is the solution: mathematically sound, humanly practical, computationally natural.

***

## The Generational Discovery

Within-Run Stability: 97% of years follow 368-368-360
Typical Run Length: 27 years (9 complete cycles of 368-368-360)
Run Distribution: Most runs span 27-30 years across analyzed periods
Validation: See test_generational_stability test

The 27-Year Rhythm:
- 27 years = 9 cycles of 368-368-360
- 27 years ≈ 1 human generation (childhood to adulthood)
- Pattern emerges naturally from mathematics
- Not designed for this alignment

Human Experience:
- Child learns: "368-368-360"
- Pattern holds: Until age 27 (entire youth)
- Sees disruption: Once in generation
- Teaches children: Same simple pattern

Comparison:
- Gregorian: Check every year (80 times in 80-year lifetime)
- UCY: Check every generation (3 times in 80-year lifetime)
- Cognitive load: 27× less

Why It Matters:
When you listen to nature's mathematics instead of imposing rules, you get harmony with human timescales as a gift, not as a goal. The calendar breathes with both cosmic and human rhythms simultaneously.

This wasn't engineered. It emerged. That's the difference between controlling time and playing hide and seek with it.

***

## Comparison

Legacy approach (Gregorian):
- Prioritizes historical inertia over mathematical truth
- Patches accumulated errors with complex rules
- Accepts fractional weeks as "good enough"

Modern solution (UCY):
- Mathematical elegance from first principles
- Cognitive simplicity through natural patterns
- Generational stability by design

The difference:
- Gregorian: Constant vigilance required (check leap rules annually)
- UCY: Generational awareness (pattern stable for ~27 years)

For actual humans living actual lives:
- Gregorian: Pattern changes every 4 years
- UCY: Pattern changes every 27 years

That's 27× reduction in cognitive load.
That's not iteration. That's revolution.

***

## Q & A

**Q: When does the breaking point arrive?**

A: The friction accumulates. Every smartphone requiring leap second corrections. International commerce stumbling over calendar edge cases. Programmers cursing February 29th. The cost of maintaining broken systems compounds daily. Breaking points don't announce themselves—they reveal themselves in retrospect. The question isn't when but how quickly we recognize the transition has already begun.

**Q: Where do revolutions begin?**

A: The margins. A Mars colony implements eight-day work cycles because mathematics demands it. Digital communities adopt octal time for their virtual worlds. Educational institutions teach multiple calendar systems and students recognize which one makes sense. Technical communities implement UCY internally, using it where precision matters. Each adoption proves viability. Each success creates momentum.

**Q: How does computation drive change?**

A: Programmers already think in hexadecimal. Binary is second nature to millions. AI systems, asked to optimize timekeeping, independently arrive at eight-day weeks. They explain with perfect logic why our calendar is inefficient. And this time, we listen to mathematics instead of defending tradition. Machine-internal time representation shifts to UCY while displaying Gregorian for legacy compatibility. The transition happens in the infrastructure before it reaches the interface.

**Q: How does education enable transformation?**

A: Every child who learns calendars are choices, not laws of nature, becomes an agent of change. A generation fluent in both Gregorian and UCY, comfortable switching between them, asks: why do we prefer the broken one? Education doesn't force change. It makes change inevitable. Understanding UCY transforms how you see time itself.

**Q: Why does longer lifespan demand better systems?**

A: A human living 200+ years experiences the Gregorian calendar's quirks hundreds of times. Memorizing leap year rules becomes torture. Explaining why February sometimes has 29 days becomes absurd when repeated across centuries. Long life demands rational calendars. As human lifespan extends, system efficiency becomes survival necessity, not aesthetic preference.

**Q: How do better systems replace established ones?**

A: Arabic numerals replaced Roman numerals. The metric system won most of the world. QWERTY persists but touchscreens use optimized layouts. Better solutions gain adoption when advantages outweigh switching costs. UCY exists now, proven and documented across 10,000 years of validation. Implementation pathways are clear. The technical foundation is solid. Adoption accelerates where precision matters and tradition weighs less.

**Q: What does UCY stand for?**

A: You See Why?

**Q: How do you stand in the light yet cast no shadow?**

A: Be the sun.
