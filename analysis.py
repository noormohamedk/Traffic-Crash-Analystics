import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

DB_USER = "root"
DB_PASSWORD = quote_plus("Zayahaya@1806")
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "traffic_crash_db"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def run_query(sql: str):
    return pd.read_sql(sql, engine)

Q1_SQL = """
SELECT
    WEATHER_CONDITION,
    FIRST_CRASH_TYPE,
    COUNT(*) AS TOTAL_CRASHES
FROM crashtable
WHERE WEATHER_CONDITION IS NOT NULL
  AND FIRST_CRASH_TYPE IS NOT NULL
GROUP BY WEATHER_CONDITION, FIRST_CRASH_TYPE
ORDER BY TOTAL_CRASHES DESC
LIMIT 5;
"""

Q2_SQL = """
SELECT
    STREET_NAME,
    COUNT(*) AS INJURY_CRASHES
FROM crashtable
WHERE INJURIES_TOTAL > 0
  AND STREET_NAME IS NOT NULL
GROUP BY STREET_NAME
ORDER BY INJURY_CRASHES DESC
LIMIT 10;
"""

Q3_SQL = """
SELECT
    FIRST_CRASH_TYPE,
    COUNT(*) AS TOTAL_CRASHES,
    SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) AS INJURY_CRASHES,
    ROUND(
        100.0 * SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS INJURY_PCT
FROM crashtable
WHERE FIRST_CRASH_TYPE IS NOT NULL
GROUP BY FIRST_CRASH_TYPE
ORDER BY INJURY_PCT DESC;
"""

Q4_SQL = """
WITH HourlyCount AS (
    SELECT
        CRASH_MONTH,
        CRASH_HOUR,
        COUNT(*) AS CRASH_COUNT
    FROM crashtable
    WHERE CRASH_MONTH IS NOT NULL AND CRASH_HOUR IS NOT NULL
    GROUP BY CRASH_MONTH, CRASH_HOUR
),
Ranked AS (
    SELECT *,
        RANK() OVER (PARTITION BY CRASH_MONTH ORDER BY CRASH_COUNT DESC) AS rnk
    FROM HourlyCount
)
SELECT
    CRASH_MONTH,
    CRASH_HOUR AS PEAK_HOUR,
    CRASH_COUNT
FROM Ranked
WHERE rnk = 1
ORDER BY CRASH_MONTH;
"""

Q5_SQL = """
SELECT
    PRIM_CONTRIBUTORY_CAUSE,
    COUNT(*) AS NIGHT_CRASHES
FROM crashtable
WHERE CRASH_HOUR >= 18
  AND PRIM_CONTRIBUTORY_CAUSE IS NOT NULL
GROUP BY PRIM_CONTRIBUTORY_CAUSE
ORDER BY NIGHT_CRASHES DESC
LIMIT 5;
"""

Q6_SQL = """
SELECT
    LIGHTING_CONDITION,
    COUNT(*) AS TOTAL_CRASHES,
    ROUND(AVG(INJURIES_TOTAL), 4) AS AVG_INJURIES,
    ROUND(AVG(INJURIES_FATAL), 4) AS AVG_FATAL
FROM crashtable
WHERE LIGHTING_CONDITION IN ('DAYLIGHT', 'DARKNESS', 'DARKNESS - LIGHTED ROAD',
                              'DARKNESS - LIGHTED', 'DAWN', 'DUSK')
  AND INJURIES_TOTAL IS NOT NULL
GROUP BY LIGHTING_CONDITION
ORDER BY AVG_INJURIES DESC;
"""

Q7_SQL = """
SELECT
    TRAFFIC_CONTROL_DEVICE,
    COUNT(*) AS TOTAL_CRASHES,
    ROUND(AVG(INJURIES_TOTAL), 4) AS AVG_INJURIES_PER_CRASH
FROM crashtable
WHERE TRAFFIC_CONTROL_DEVICE IS NOT NULL
  AND INJURIES_TOTAL IS NOT NULL
GROUP BY TRAFFIC_CONTROL_DEVICE
ORDER BY AVG_INJURIES_PER_CRASH DESC
LIMIT 10;
"""

Q8_SQL = """
SELECT
    ROUND(LATITUDE, 4)  AS LAT,
    ROUND(LONGITUDE, 4) AS LON,
    COUNT(*) AS CRASH_FREQUENCY
FROM crashtable
WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL
GROUP BY ROUND(LATITUDE, 4), ROUND(LONGITUDE, 4)
ORDER BY CRASH_FREQUENCY DESC
LIMIT 5;
"""

Q9_SQL = """
WITH StreetStats AS (
    SELECT
        STREET_NAME,
        COUNT(*) AS TOTAL_CRASHES,
        SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) AS INJURY_CRASHES
    FROM crashtable
    WHERE STREET_NAME IS NOT NULL
    GROUP BY STREET_NAME
    HAVING TOTAL_CRASHES > 100
)
SELECT
    STREET_NAME,
    TOTAL_CRASHES,
    INJURY_CRASHES,
    ROUND(100.0 * INJURY_CRASHES / TOTAL_CRASHES, 2) AS INJURY_RATE_PCT
FROM StreetStats
ORDER BY INJURY_RATE_PCT DESC
LIMIT 5;
"""

Q10_SQL = """
WITH YearlyCrashType AS (
    SELECT
        YEAR,
        FIRST_CRASH_TYPE,
        COUNT(*) AS CRASH_COUNT
    FROM crashtable
    WHERE YEAR IS NOT NULL AND FIRST_CRASH_TYPE IS NOT NULL
    GROUP BY YEAR, FIRST_CRASH_TYPE
),
Ranked AS (
    SELECT *,
        RANK() OVER (PARTITION BY YEAR ORDER BY CRASH_COUNT DESC) AS rnk
    FROM YearlyCrashType
)
SELECT YEAR, FIRST_CRASH_TYPE AS TOP_CRASH_TYPE, CRASH_COUNT
FROM Ranked
WHERE rnk = 1
ORDER BY YEAR;
"""

Q11_SQL = """
WITH DayHourCount AS (
    SELECT
        CRASH_DAY_OF_WEEK,
        CRASH_HOUR,
        COUNT(*) AS CRASHES
    FROM crashtable
    WHERE CRASH_DAY_OF_WEEK IS NOT NULL AND CRASH_HOUR IS NOT NULL
    GROUP BY CRASH_DAY_OF_WEEK, CRASH_HOUR
)
SELECT
    CRASH_DAY_OF_WEEK,
    CASE CRASH_DAY_OF_WEEK
        WHEN 1 THEN 'Sunday'    WHEN 2 THEN 'Monday'
        WHEN 3 THEN 'Tuesday'   WHEN 4 THEN 'Wednesday'
        WHEN 5 THEN 'Thursday'  WHEN 6 THEN 'Friday'
        WHEN 7 THEN 'Saturday'
    END AS DAY_NAME,
    ROUND(AVG(CRASHES), 2) AS AVG_CRASHES_PER_HOUR
FROM DayHourCount
GROUP BY CRASH_DAY_OF_WEEK
ORDER BY AVG_CRASHES_PER_HOUR DESC;
"""

Q12_SQL = """
WITH TimeSlot AS (
    SELECT
        CASE
            WHEN CRASH_HOUR BETWEEN 6 AND 11  THEN 'Morning (6–11)'
            WHEN CRASH_HOUR BETWEEN 12 AND 17 THEN 'Afternoon (12–17)'
            WHEN CRASH_HOUR BETWEEN 18 AND 21 THEN 'Evening (18–21)'
            ELSE 'Night (22–5)'
        END AS TIME_SLOT,
        INJURIES_TOTAL
    FROM crashtable
    WHERE CRASH_HOUR IS NOT NULL AND INJURIES_TOTAL IS NOT NULL
)
SELECT
    TIME_SLOT,
    COUNT(*) AS TOTAL_CRASHES,
    SUM(CASE WHEN INJURIES_TOTAL > 0 THEN 1 ELSE 0 END) AS INJURY_CRASHES,
    ROUND(AVG(INJURIES_TOTAL), 4) AS AVG_INJURIES
FROM TimeSlot
GROUP BY TIME_SLOT
ORDER BY INJURY_CRASHES DESC;
"""

Q13_SQL = """
WITH CauseCounts AS (
    SELECT
        FIRST_CRASH_TYPE,
        PRIM_CONTRIBUTORY_CAUSE,
        COUNT(*) AS CAUSE_COUNT
    FROM crashtable
    WHERE FIRST_CRASH_TYPE IS NOT NULL
      AND PRIM_CONTRIBUTORY_CAUSE IS NOT NULL
    GROUP BY FIRST_CRASH_TYPE, PRIM_CONTRIBUTORY_CAUSE
),
Ranked AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY FIRST_CRASH_TYPE ORDER BY CAUSE_COUNT DESC) AS rn
    FROM CauseCounts
)
SELECT
    FIRST_CRASH_TYPE,
    rn AS CAUSE_RANK,
    PRIM_CONTRIBUTORY_CAUSE,
    CAUSE_COUNT
FROM Ranked
WHERE rn <= 3
ORDER BY FIRST_CRASH_TYPE, rn;
"""

Q14_SQL = """
WITH YearlyTotal AS (
    SELECT
        YEAR,
        COUNT(*) AS TOTAL_CRASHES
    FROM crashtable
    WHERE YEAR IS NOT NULL
    GROUP BY YEAR
),
WithLag AS (
    SELECT
        YEAR,
        TOTAL_CRASHES,
        LAG(TOTAL_CRASHES) OVER (ORDER BY YEAR) AS PREV_YEAR_CRASHES
    FROM YearlyTotal
)
SELECT
    YEAR,
    TOTAL_CRASHES,
    PREV_YEAR_CRASHES,
    ROUND(
        100.0 * (TOTAL_CRASHES - PREV_YEAR_CRASHES) / PREV_YEAR_CRASHES, 2
    ) AS YOY_GROWTH_PCT
FROM WithLag
ORDER BY YEAR;
"""

Q15_SQL = """
SELECT
    ROUND(LATITUDE, 2)  AS ZONE_LAT,
    ROUND(LONGITUDE, 2) AS ZONE_LON,
    COUNT(*) AS CRASH_COUNT
FROM crashtable
WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL
GROUP BY ROUND(LATITUDE, 2), ROUND(LONGITUDE, 2)
ORDER BY CRASH_COUNT DESC
LIMIT 10;
"""

QUERIES = {
    1:  ("Top 5 Dangerous Weather × Crash-Type Combos",        Q1_SQL,
         "Clear weather + Parked Motor Vehicle collisions top the list — high-volume routine conditions drive the most crashes."),
    2:  ("Top 10 Streets by Injury Crashes",                   Q2_SQL,
         "A handful of arterial corridors consistently accumulate injury crashes; targeted enforcement here would maximise safety ROI."),
    3:  ("Injury Rate (%) per Crash Type",                     Q3_SQL,
         "Pedestrian and pedalcyclist crash types convert at the highest injury rates, highlighting the need for protective infrastructure."),
    4:  ("Peak Crash Hour per Month",                          Q4_SQL,
         "Evening rush hours (16–18) dominate year-round; winter months show an additional morning-rush spike."),
    5:  ("Top 5 Night-Time Primary Causes (Hour ≥ 18)",        Q5_SQL,
         "Failure to reduce speed and improper lane usage are the leading night-time causes — both are addressable with illumination and signage."),
    6:  ("Avg Injuries: Daylight vs Darkness Conditions",      Q6_SQL,
         "Darkness conditions yield higher average injuries per crash, underscoring the value of better street lighting."),
    7:  ("Traffic Control Device vs Avg Injuries per Crash",   Q7_SQL,
         "Locations with no controls or malfunctioning devices have the worst injury rates — maintenance backlogs cost lives."),
    8:  ("Top 5 Crash-Frequency Locations (Lat/Lon)",          Q8_SQL,
         "Pinpoint hotspots allow authorities to deploy infrastructure improvements where they will have the greatest impact."),
    9:  ("Top 5 Streets by Injury Rate (>100 crashes)",        Q9_SQL,
         "High injury-rate streets with sufficient volume are prime candidates for geometric redesign or speed-limit reduction."),
    10: ("Most Common Crash Type per Year",                    Q10_SQL,
         "Parked Motor Vehicle crashes have grown steadily, reflecting urban density; rear-end crashes track commuter volume."),
    11: ("Day of Week with Highest Avg Crashes per Hour",      Q11_SQL,
         "Fridays record the highest average crashes per hour, pointing to end-of-week fatigue and increased travel demand."),
    12: ("High-Risk Time Slots (Injury Crashes by Bucket)",    Q12_SQL,
         "The Afternoon slot produces the most injury crashes in absolute terms, while Evening shows the highest average injury rate."),
    13: ("Top 3 Contributing Causes per Crash Type",           Q13_SQL,
         "Driver inattention and failure to yield are universal top causes across nearly every crash type — education campaigns should target both."),
    14: ("Year-over-Year Crash Growth Rate",                   Q14_SQL,
         "Post-pandemic rebound years (2021–2022) show sharp growth; 2023–2024 trends indicate whether interventions are working."),
    15: ("Top 10 Hotspot Zones (Lat/Lon rounded to 2dp)",     Q15_SQL,
         "Zone-level clustering identifies neighbourhood-scale danger areas suitable for coordinated enforcement and infrastructure investment."),
}


def fetch_query(query_num: int) -> pd.DataFrame:
    """Return the DataFrame for the given query number (1–15)."""
    _, sql, _ = QUERIES[query_num]
    return run_query(sql)


def fetch_all() -> dict:
    """Return all 15 query DataFrames keyed by query number."""
    return {n: fetch_query(n) for n in QUERIES}


if __name__ == "__main__":
    for n, (label, _, insight) in QUERIES.items():
        df = fetch_query(n)
        print(f"\nQ{n}: {label}")
        print(df.head(3).to_string(index=False))