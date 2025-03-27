import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json

# Section 1: Data Import and Cleaning
ambulance_calls_df = pd.read_csv("911-ambulance-calls-2024-Jan-Sep.csv")

# Task 1.2: Clean Data
ambulance_calls_df = ambulance_calls_df.rename(columns={
    "CLOSNG_TS": "closing_ts",
    "ARRIVD_TS": "arrived_ts"
})
ambulance_calls_df["closing_ts"] = pd.to_datetime(ambulance_calls_df["closing_ts"], format='%m/%d/%Y %I:%M:%S %p')
ambulance_calls_df["arrived_ts"] = pd.to_datetime(ambulance_calls_df["arrived_ts"], format='%m/%d/%Y %I:%M:%S %p')

ambulance_calls_df["incident_ts"] = pd.to_datetime(
    ambulance_calls_df["INCIDENT_DATE"] + " " + ambulance_calls_df["INCIDENT_TIME"],
    format='%Y-%m-%d %H:%M:%S'
)
ambulance_calls_df = ambulance_calls_df.drop(columns=["INCIDENT_DATE", "INCIDENT_TIME"])
ambulance_calls_df.columns = ambulance_calls_df.columns.str.lower()

# Task 1.3: Compute Time Intervals
ambulance_calls_df["duration_secs"] = (ambulance_calls_df["closing_ts"] - ambulance_calls_df["incident_ts"]).dt.total_seconds()
ambulance_calls_df["arrived_in_secs"] = (ambulance_calls_df["arrived_ts"] - ambulance_calls_df["incident_ts"]).dt.total_seconds()

# Section 2: Exploratory Analysis
# Task 2.1: Summary Statistics
print(ambulance_calls_df[["duration_secs", "arrived_in_secs"]].describe(percentiles=[.25, .5, .75, .9, .95]).T)

# ECDF Plot
plt.figure(figsize=(12, 4))
sns.ecdfplot(data=ambulance_calls_df, x="duration_secs", label="Duration")
sns.ecdfplot(data=ambulance_calls_df, x="arrived_in_secs", label="Arrival Time")
plt.xlim(0, 20000)
plt.xlabel("Time in Seconds")
plt.legend()
plt.show()

# Task 2.3: KDE Plots
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
sns.kdeplot(data=ambulance_calls_df, x="duration_secs", hue="boro_nm", common_norm=False, clip=(-1, 20000), ax=ax[0])
sns.kdeplot(data=ambulance_calls_df, x="arrived_in_secs", hue="boro_nm", common_norm=False, clip=(-1, 10000), ax=ax[1])
plt.show()

# Section 3: Choropleth Map
nyc_boros = gpd.read_file("borough-boundaries.geojson")

# Ensure borough names match between datasets
nyc_boros['boro_name'] = nyc_boros['boro_name'].replace({'The Bronx': 'Bronx'})

filtered = ambulance_calls_df[
    (ambulance_calls_df["arrived_in_secs"] > 0) &
    (ambulance_calls_df["boro_nm"].notna()) &
    (ambulance_calls_df["arrived_ts"].notna())
]
calls_by_boro = filtered.groupby("boro_nm").agg(
    num_calls=("incident_ts", "size"),
    median_arrived_in_secs=("arrived_in_secs", "median"),
    median_duration_secs=("duration_secs", "median")
).reset_index()

choropleth_gdf = nyc_boros.merge(calls_by_boro, left_on="boro_name", right_on="boro_nm")

choropleth_fig = px.choropleth_mapbox(
    choropleth_gdf,
    geojson=json.loads(choropleth_gdf.to_json()),
    locations="boro_name",
    color="median_arrived_in_secs",
    featureidkey="properties.boro_name",
    hover_data=["num_calls", "median_duration_secs"],
    labels={
        "boro_name": "Borough",
        "median_arrived_in_secs": "Median Arrival Time (seconds)",
        "median_duration_secs": "Median Duration (seconds)"
    },
    mapbox_style="carto-darkmatter",
    center={"lat": 40.75, "lon": -74.0},
    zoom=9,
    height=750,
    width=750
)
choropleth_fig.show()

# Section 4: Scatter Map
new_years_df = ambulance_calls_df[
    (ambulance_calls_df["incident_ts"].dt.date == pd.to_datetime("2024-01-01").date()) &
    (ambulance_calls_df["latitude"].notna()) &
    (ambulance_calls_df["longitude"].notna())
]

scatter_fig = px.scatter_mapbox(
    new_years_df,
    lat="latitude",
    lon="longitude",
    color="arrived_in_secs",
    size="arrived_in_secs",
    opacity=0.7,
    title="Ambulance Calls on New Year's Day 2024",
    zoom=10,
    height=750,
    width=750
)

scatter_fig.update_layout(mapbox_layers=[{
    "type": "line",
    "color": "white",
    "opacity": 0.5,
    "source": json.loads(nyc_boros.geometry.to_json()),
    "line": {"width": 1}
}])
scatter_fig.update_layout(mapbox_style="carto-darkmatter")
scatter_fig.show()