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

# Proses data
all_df = create_season_mapping(all_df)

hourly_trend_df = create_hourly_trend_df(all_df)
seasonly_trend_df = create_seasonal_trend_df(all_df)

st.title("Submission Data Analyst Dicoding with IDCamp")
st.subheader("by Irsyad Muhamad Firdaus")

st.header("Grafik Penyewaan Sepeda Tiap Jam per Hari")
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#007ACC' if hour in [17, 18, 8] else '#B0B0B0' for hour in hourly_trend_df.index]
hourly_trend_df.plot(kind="bar", color=colors, ax=ax)

for i, (hour, value) in enumerate(zip(hourly_trend_df.index, hourly_trend_df)):
    if hour in [17, 18, 8]:
        ax.text(i, value + 5, f'{value:.0f}', ha='center', va='bottom', fontsize=10, color='black')

ax.set_title("Rata-Rata Penyewaan Sepeda Tiap Jam", fontsize=16, fontweight="bold")
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Rata-Rata Penyewa", fontsize=12)
ax.tick_params(axis="x", rotation=0)
ax.tick_params(axis="y", rotation=0)
st.pyplot(fig)

if st.button('Penjelasan Grafik Penyewaan Tiap Jam'):
    st.markdown('''Grafik ini menunjukkan pola rata-rata penyewaan sepeda pada setiap jam dalam sehari. Dari hasil analisis, terlihat bahwa puncak penyewaan terjadi pada :blue[jam 17.00 (sore hari)] dengan rata-rata :blue[461 penyewa per jam], diikuti oleh :green[jam 18.00] dengan rata-rata :green[426 penyewa], dan :violet[jam 08.00 (pagi hari)] dengan rata-rata :violet[359 penyewa.] Pola ini mencerminkan waktu-waktu sibuk, seperti saat pulang kerja di sore hari dan berangkat kerja atau sekolah di pagi hari. Sebaliknya, penyewaan sepeda sangat rendah pada dini hari, terutama antara :red[jam 02.00 hingga 04.00], dengan rata-rata :red[kurang dari 15 penyewa] per jam. Grafik ini membantu mengidentifikasi waktu-waktu dengan permintaan tinggi, yang dapat menjadi panduan untuk pengelolaan armada sepeda secara lebih efisien dan strategi pemasaran pada jam-jam tertentu.''')

st.header("Grafik Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 5))
season_colors = ["#FF5733", "#FFC300", "#FFC300", "#FFC300"]
seasonly_trend_df.plot(kind="bar", color=season_colors, ax=ax)

for i, (season, value) in enumerate(zip(seasonly_trend_df.index, seasonly_trend_df)):
    if season == "Fall":
        ax.text(i, value + 5, f'{value:.0f}', ha='center', va='bottom', fontsize=10, color='black')

ax.set_title("Rata-Rata Penyewaan Sepeda per Musim", fontsize=16, fontweight="bold")
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Rata-Rata Penyewa", fontsize=12)
ax.tick_params(axis="x", rotation=0)
ax.tick_params(axis="y", rotation=0)
st.pyplot(fig)

if st.button('Penjelasan Grafik Penyewaan Berdasarkan Musim'):
    st.markdown('''Grafik ini menunjukkan rata-rata jumlah penyewaan sepeda pada setiap musim. Terlihat bahwa :orange[Musim Gugur (Fall)] memiliki jumlah rata-rata penyewaan tertinggi dengan jumlah 236 per jam, diikuti oleh :red[Musim Panas (Summer)] dengan jumlah :red[208 penyewaan] per jam. Sebaliknya, :violet[Musim Semi (Spring)] memiliki rata-rata penyewaan terendah dengan jumlah :violet[111 penyewa]. Pola ini menunjukkan bahwa faktor cuaca dan kenyamanan bersepeda memengaruhi tingkat penyewaan sepeda.''')

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=200)
    st.write("Navigasi:")
    st.markdown("[Grafik Penyewaan Sepeda Tiap Jam](#grafik-penyewaan-sepeda-tiap-jam-per-hari)")
    st.markdown("[Grafik Penyewaan Berdasarkan Musim](#grafik-penyewaan-sepeda-berdasarkan-musim)")
