import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from babel.numbers import format_currency

sns.set(style='dark')

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

hourly_trend_df = create_hourly_trend_df(all_df)
seasonly_trend_df = create_seasonal_trend_df(all_df)

st.write(
    """
    # Submission Data Analyst Dicoding with IDCamp
    by Irsyad Muhamad Firdaus
    """ 
)

st.subheader("Grafik Penyewaan Sepeda tiap Jam per Hari", anchor="Grafik Per Hari", divider="blue")
st.bar_chart(
    data=hourly_trend_df,
    use_container_width=True,
)
st.caption("Penjelasan Grafik dapat dilihat di sini")
if st.button('Penjelasan Grafik 1'):
    st.markdown('''Grafik tersebut menunjukkan pola rata-rata penyewaan sepeda pada setiap jam dalam sehari. Dari hasil analisis, terlihat bahwa puncak penyewaan terjadi pada :blue[jam 17.00 (sore hari)] dengan rata-rata :blue[461 penyewa per jam], diikuti oleh :green[jam 18.00] dengan rata-rata :green[426 penyewa], dan :violet[jam 08.00 (pagi hari)] dengan rata-rata :violet[359 penyewa.] Pola ini mencerminkan waktu-waktu sibuk, seperti saat pulang kerja di sore hari dan berangkat kerja atau sekolah di pagi hari. Sebaliknya, penyewaan sepeda sangat rendah pada dini hari, terutama antara :red[jam 02.00 hingga 04.00], dengan rata-rata :red[kurang dari 15 penyewa] per jam. Grafik ini membantu mengidentifikasi waktu-waktu dengan permintaan tinggi, yang dapat menjadi panduan untuk pengelolaan armada sepeda secara lebih efisien dan strategi pemasaran pada jam-jam tertentu.''')

st.subheader("Grafik Penyewaan Sepeda dalam Musim yang Berbeda", anchor="Pegaruh Musim", divider="blue")
st.bar_chart(
    data=seasonly_trend_df,
    use_container_width=True,
)
if st.button('Penjelasan Grafik 2'):
    st.markdown('''Grafik ini menunjukkan rata-rata jumlah penyewaan sepeda pada setiap musim. Terlihat bahwa :orange[Musim Gugur (Fall)] memiliki rata-rata penyewaan tertinggi dengan jumlah 236 per jam, diikuti oleh :red[Musim Panas (Summer)] dengan jumlah :red[208 penyewaan] per jam. Sebaliknya, :violet[Musim Semi (Spring)] memiliki rata-rata penyewaan terendah dengan jumlah :violet[111 penyewa]. Pola ini menunjukkan bahwa faktor cuaca dan kenyamanan bersepeda memengaruhi tingkat penyewaan sepeda.''')

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.write("Check [Grafik Rata-Rata per Hari](#Grafik%20Per%20Hari)")
    st.write("Check [Grafik Pengaruh Musim](#Pegaruh%20Musim)")
