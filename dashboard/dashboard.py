import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style="whitegrid")

# === Helper functions ===
def create_hourly_trend_df(df):
    return df.groupby("hr")["cnt_hour"].mean()

def create_seasonal_trend_df(df):
    return df.groupby("season_day")["cnt_hour"].mean()

def create_season_mapping(df):
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df["season_day"] = df["season_day"].map(season_mapping)
    return df

# === Load Data ===
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "all_data.csv")

try:
    all_df = pd.read_csv(file_path)
    st.success("✅ Data loaded successfully.")
except FileNotFoundError:
    st.error(f"❌ File 'all_data.csv' not found at {file_path}. Please make sure it's in the same directory.")
    st.stop()

all_df = create_season_mapping(all_df)

# === Sidebar Filters ===
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    st.markdown("## Filter Options")
    selected_season = st.multiselect(
        "Select Seasons:",
        options=all_df["season_day"].unique(),
        default=all_df["season_day"].unique()
    )

    selected_weather = st.multiselect(
        "Select Weather Conditions:",
        options=all_df["weathersit_hour"].unique(),
        default=all_df["weathersit_hour"].unique()
    )

    st.markdown("### Weather Info:")
    st.caption("1: Clear, Few clouds")
    st.caption("2: Mist, Cloudy")
    st.caption("3: Light Rain or Snow")
    st.caption("4: Heavy Rain or Snowstorm")

    st.markdown("### Navigation")
    st.markdown("[Hourly Rental Trend](#hourly-bike-rental-trend)")
    st.markdown("[Seasonal Rental Trend](#seasonal-bike-rental-trend)")

# === Filtered DataFrame ===
filtered_df = all_df[
    (all_df["season_day"].isin(selected_season)) &
    (all_df["weathersit_hour"].isin(selected_weather))
]

if filtered_df.empty:
    st.error("🚫 No data matches the selected filters.")
    st.stop()

# === Title ===
st.title("🚴 Ride the Trend: Exploring Bike Rentals")
st.subheader("A data analysis project by Irsyad Muhamad Firdaus")
st.caption("Submission for IDCamp x Dicoding: Data Analyst Learning Path")

st.markdown("---")

# === Hourly Rental Chart ===
st.header("⏰ Hourly Bike Rental Trend")
fig, ax = plt.subplots(figsize=(10, 6))
hourly_trend_df = create_hourly_trend_df(filtered_df)
highlight_hours = [8, 17, 18]  # commuting hours

colors = ['#007ACC' if hour in highlight_hours else '#B0B0B0' for hour in hourly_trend_df.index]
hourly_trend_df.plot(kind="bar", color=colors, ax=ax)

for i, (hour, value) in enumerate(hourly_trend_df.items()):
    if hour in highlight_hours:
        ax.text(i, value + 5, f'{value:.0f}', ha='center', va='bottom', fontsize=10)

ax.set_title("Average Bike Rentals per Hour", fontsize=16, fontweight="bold")
ax.set_xlabel("Hour of the Day", fontsize=12)
ax.set_ylabel("Average Rentals", fontsize=12)
ax.tick_params(axis="x", rotation=0)
ax.tick_params(axis="y", rotation=0)
st.pyplot(fig)

with st.expander("📘 Explanation: Hourly Rental Trend"):
    st.markdown("""
    This chart shows the **average number of bike rentals per hour**.  
    The **blue bars** highlight peak rental hours (typically commuting times at **8 AM, 5 PM, and 6 PM**), 
    indicating when people rent bikes the most.
    """)

st.markdown("---")

# === Seasonal Rental Chart ===
st.header("🌤️ Seasonal Bike Rental Trend")
fig, ax = plt.subplots(figsize=(8, 5))
seasonal_trend_df = create_seasonal_trend_df(filtered_df)
max_season = seasonal_trend_df.idxmax()

colors = ["#FFC300" if season == max_season else "#B0B0B0" for season in seasonal_trend_df.index]
seasonal_trend_df.plot(kind="bar", color=colors, ax=ax)

for i, (season, value) in enumerate(seasonal_trend_df.items()):
    if season == max_season:
        ax.text(i, value + 5, f'{value:.0f}', ha='center', va='bottom', fontsize=10)

ax.set_title("Average Bike Rentals per Season", fontsize=16, fontweight="bold")
ax.set_xlabel("Season", fontsize=12)
ax.set_ylabel("Average Rentals", fontsize=12)
ax.tick_params(axis="x", rotation=0)
ax.tick_params(axis="y", rotation=0)
st.pyplot(fig)

with st.expander("📘 Explanation: Seasonal Rental Trend"):
    st.markdown(f"""
    This chart shows the **average number of rentals per season**.  
    The **yellow bar** indicates the season with the **highest rental activity**: **{max_season}**.  
    This may be due to favorable weather or holiday patterns during that time.
    """)
