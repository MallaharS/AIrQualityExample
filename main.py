import requests
import pandas as pd
import matplotlib.pyplot as plt

API_KEY = " YOUR_API_KEY_HERE"
HEADERS = {"X-API-Key": API_KEY}

# 1. Get monitoring stations near Hamilton
url = "https://api.openaq.org/v3/locations"
params = {"coordinates": "43.2557,-79.8711", "radius": 25000, "limit": 10}
response = requests.get(url, params=params, headers=HEADERS)
print("Status:", response.status_code)
data = response.json()


# 2. Pull one station's latest readings, matched to pollutant names
def get_station_data(location):
    name = location.get("name")
    station_id = location.get("id")

    latest = requests.get(
        f"https://api.openaq.org/v3/locations/{station_id}/latest", headers=HEADERS
    ).json()["results"]

    value_by_sensor = {item["sensorsId"]: item["value"] for item in latest}

    readings = {"station_name": name}
    for sensor in location["sensors"]:
        param = sensor["parameter"]["name"]
        sid = sensor["id"]
        if sid in value_by_sensor:
            readings[param] = value_by_sensor[sid]
    return readings


# 3. Build a table: one row per station
def generate_dataframe(locations):
    rows = [get_station_data(loc) for loc in locations]
    return pd.DataFrame(rows)


# 4. Make sure pollutant columns are numeric
def clean_dataframe(df):
    for col in df.columns:
        if col != "station_name":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


# 5. Plot PM2.5 by station
def display_pm25_bar(df):
    plot_df = df.copy()
    plot_df["station_name"] = plot_df["station_name"] + " #" + \
        (plot_df.groupby("station_name").cumcount() + 1).astype(str)

    plot_df = plot_df.dropna(subset=["pm25"]).sort_values("pm25")
    colors = ["tab:red" if v > 15 else "tab:green" for v in plot_df["pm25"]]

    plt.figure(figsize=(11, 6))
    plt.barh(plot_df["station_name"], plot_df["pm25"], color=colors)
    plt.axvline(15, color="gray", linestyle="--", linewidth=1, label="WHO 24h guideline (15)")
    plt.xlabel("PM2.5 (µg/m³)")
    plt.title("PM2.5 Air Quality by Station — Hamilton Area")
    plt.legend()
    plt.tight_layout()
    plt.savefig("pm25_by_station.png", dpi=120)
    plt.show()


# ---- run everything ----
df = generate_dataframe(data["results"])
df = clean_dataframe(df)
print(df)
display_pm25_bar(df)
