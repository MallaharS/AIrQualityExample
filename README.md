# Air Quality Analyzer — Hamilton Area

A Python tool that pulls live air-quality data from the [OpenAQ API](https://openaq.org), processes it with Pandas, and visualizes PM2.5 levels across monitoring stations in the Hamilton, Ontario area.

## What it does

- **Fetches** monitoring stations within 25 km of Hamilton from the OpenAQ v3 REST API (authenticated with an API key)
- **Joins** two different API responses — matching each station's sensors to their latest readings — to map raw sensor IDs to named pollutants (PM2.5, NO₂, O₃, etc.)
- **Cleans** the data into a structured Pandas DataFrame, handling stations that measure different sets of pollutants
- **Visualizes** PM2.5 concentration by station as a ranked bar chart, color-coded against the WHO 24-hour air-quality guideline (15 µg/m³)

## Why PM2.5

PM2.5 (fine particulate matter) is the pollutant every station in the dataset measures, and it's the primary metric health agencies use for air-quality standards — making it the most meaningful and consistent basis for comparison.

## Tech stack

Python, Requests (REST API), Pandas, Matplotlib

## Setup & run

```bash
pip install requests pandas matplotlib

# Add your free OpenAQ API key (from https://openaq.org) to the API_KEY variable, then:
python main.py
```

## Sample output

The script prints a table of all stations and their pollutant readings, then displays and saves a bar chart (`pm25_by_station.png`) ranking stations by PM2.5, with stations exceeding the WHO guideline shown in red.

## A note on the data

OpenAQ returns each station's *most recent* reading, and some stations report more frequently than others — so the readings are not all from the same moment in time. This is a snapshot comparison of each station's latest available value, not a synchronized measurement. A natural next step would be to pull a fixed historical time window per station for a true like-for-like comparison.
