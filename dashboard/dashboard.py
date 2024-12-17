import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

sns.set(style="whitegrid")

def create_hourly_trend_df(df):
    return df.groupby("hr")["cnt_hour"].mean()

def create_seasonal_trend_df(df):
    return df.groupby("season_day")["cnt_hour"].mean()

def create_season_mapping(df):
    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df["season_day"] = df["season_day"].map(season_mapping)
    return df

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "all_data.csv")

try:
    all_df = pd.read_csv(file_path)
    st.success("File 'all_data.csv' berhasil dimuat.")
except FileNotFoundError:
    st.error(f"File 'all_data.csv' tidak ditemukan di {file_path}. Pastikan file berada di direktori yang sama dengan script ini.")
    st.stop()

all_df = create_season_mapping(all_df)

st.sidebar.header("Filter Data")
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=200)
selected_season = st.sidebar.multiselect(
    "Pilih Musim:",
    options=all_df["season_day"].unique(),
    default=all_df["season_day"].unique()
)
with st.sidebar:
    st.write("Navigasi:")
    st.markdown("[Grafik Penyewaan Sepeda Tiap Jam](#grafik-penyewaan-sepeda-tiap-jam-per-hari)")
    st.markdown("[Grafik Penyewaan Berdasarkan Musim](#grafik-penyewaan-sepeda-berdasarkan-musim)")

filtered_df = all_df[
    all_df["season_day"].isin(selected_season)
]

if filtered_df.empty:
    st.error("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

st.title("Submission Data Analyst Dicoding with IDCamp")
st.subheader("by Irsyad Muhamad Firdaus")

st.header("Grafik Penyewaan Sepeda Tiap Jam per Hari")
fig, ax = plt.subplots(figsize=(10, 6))
hourly_trend_df = create_hourly_trend_df(filtered_df)
colors = ['#007ACC' if hour in [17, 18, 8] else '#B0B0B0' for hour in hourly_trend_df.index]
hourly_trend_df.plot(kind="bar", color=colors, ax=ax)

for i, (hour, value) in enumerate(hourly_trend_df.items()):
    if hour in [17, 18, 8]:
        ax.text(i, value + 5, f'{value:.0f}', ha='center', va='bottom', fontsize=10, color='black')

ax.set_title("Rata-Rata Penyewaan Sepeda Tiap Jam", fontsize=16, fontweight="bold")
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Rata-Rata Penyewa", fontsize=12)
ax.tick_params(axis="x", rotation=0)
ax.tick_params(axis="y", rotation=0)
st.pyplot(fig)

if st.button('Penjelasan Grafik Penyewaan Tiap Jam'):
    st.markdown('''Grafik ini menunjukkan rata-rata jumlah penyewaan sepeda per jam sepanjang hari. Pola ini mencerminkan waktu sibuk. :blue[Bar yang berwarna biru] menunjukkan 3 waktu dengan jumlah penyewaan sepeda tertinggi dalam waktu 1 hari.''')

st.header("Grafik Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 5))
seasonly_trend_df = create_seasonal_trend_df(filtered_df)
max_season = seasonly_trend_df.idxmax()
colors = ["#FFC300" if season == max_season else "#B0B0B0" for season in seasonly_trend_df.index]
seasonly_trend_df.plot(kind="bar", color=colors, ax=ax)

for i, (season, value) in enumerate(seasonly_trend_df.items()):
    if season == max_season:
        ax.text(i, value + 5, f'{value:.0f}', ha='center', va='bottom', fontsize=10, color='black')

ax.set_title("Rata-Rata Penyewaan Sepeda per Musim", fontsize=16, fontweight="bold")
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Rata-Rata Penyewa", fontsize=12)
ax.tick_params(axis="x", rotation=0)
ax.tick_params(axis="y", rotation=0)
st.pyplot(fig)

if st.button('Penjelasan Grafik Penyewaan Berdasarkan Musim'):
    st.markdown('''Grafik ini menunjukkan rata-rata jumlah penyewaan sepeda pada setiap musim. Terlihat bahwa :orange[bar yang berwarna orange] memiliki rata-rata penyewaan tertinggi dibandingkan dengan yang lain.''')


