# Traffic Crash Analytics & Safety Intelligence Platform

## Project Overview

Traffic Crash Analytics & Safety Intelligence Platform is a data analytics dashboard built using **Python, Streamlit, MySQL, Pandas, Plotly, and SQLAlchemy**. The platform analyzes large-scale traffic crash datasets and provides interactive visualizations, hotspot detection, injury analysis, weather impact analysis, trend forecasting, and safety insights.

The system helps transportation authorities, city planners, and researchers identify high-risk areas and factors contributing to traffic accidents.

## Objectives

* Analyze traffic crash patterns and trends.
* Identify dangerous roads and hotspot locations.
* Study weather and lighting effects on crashes.
* Measure injury and fatality rates.
* Generate actionable safety insights.
* Visualize crash data through interactive dashboards.

## Technologies Used

### Frontend

* Streamlit
* Plotly

### Backend

* Python

### Database

* MySQL

### Libraries

* Pandas
* SQLAlchemy
* PyMySQL

## Features

### Dashboard Overview

* Total Crashes
* Total Injuries
* Fatal Injuries
* Years Covered

### Crash Analysis

* Most Common Crash Types
* Injury Rate by Crash Type
* Top Contributing Causes

### Weather & Lighting Analysis

* Weather vs Crash Type Analysis
* Night-Time Crash Causes
* Daylight vs Darkness Injury Comparison

### Traffic Safety Analysis

* Dangerous Streets
* Traffic Control Device Analysis
* Day-of-Week Crash Patterns

### Trend Analysis

* Peak Crash Hours
* High-Risk Time Slots
* Year-over-Year Growth Rate

### Geographic Analysis

* Crash Frequency Locations
* Hotspot Zones
* Interactive Visualizations

### Query Explorer

* Execute and explore all analytical SQL queries
* Export results as CSV

## Database Information

### Database Name

```sql
traffic_crash_db
```

### Main Table

```sql
crashtable
```

### Dataset Size

* 660,934 Records
* 39 Columns
* Years Covered: 2020 – 2026

## Advanced SQL Analytics

The project contains 15 advanced analytical SQL queries:

1. Top Dangerous Weather × Crash-Type Combinations
2. Top Streets by Injury Crashes
3. Injury Rate per Crash Type
4. Peak Crash Hour per Month
5. Night-Time Crash Causes
6. Daylight vs Darkness Injury Analysis
7. Traffic Control Device Analysis
8. High-Frequency Crash Locations
9. Streets with Highest Injury Rate
10. Most Common Crash Type per Year
11. Day with Highest Average Crashes
12. High-Risk Time Slot Analysis
13. Top Contributing Causes per Crash Type
14. Year-over-Year Crash Growth Rate
15. Hotspot Zone Analysis

## Installation

### Clone Repository

```bash
git clone https://github.com/noormohamedk/Traffic-Crash-Analystics.git
cd Traffic-Crash-Analystics
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure MySQL

Create database:

```sql
CREATE DATABASE traffic_crash_db;
```

Update MySQL credentials inside:

```text
analysis.py
load_data.py
```

### Import Dataset

```bash
python load_data.py
```

### Run Dashboard

```bash
python -m streamlit run app.py
```

---

## Dashboard Modules

* Overview Dashboard
* Crash Analysis
* Weather Analysis
* Lighting Analysis
* Traffic Safety Analysis
* Trend Analysis
* Geographic Analysis
* Query Explorer
