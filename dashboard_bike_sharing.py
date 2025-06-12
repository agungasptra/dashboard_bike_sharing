import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# Load dataset
day_df = pd.read_csv("../data/day.csv")

# Konversi kolom tanggal
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Sidebar - Rentang tanggal
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

with st.sidebar:
    st.title("Bike Sharing Dashboard")
    st.markdown("### Pilih Rentang Waktu:")
    start_date, end_date = st.date_input(
        "Rentang waktu",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data berdasarkan tanggal
filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                     (day_df['dteday'] <= pd.to_datetime(end_date))]

# Header
st.title("📊 Dashboard Bike Sharing Dataset")

# METRIC
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Peminjaman", value=int(filtered_df['cnt'].sum()))
with col2:
    st.metric("Rata-rata Peminjaman", value=round(filtered_df['cnt'].mean(), 2))

# Grafik jumlah peminjaman per hari
st.subheader("Jumlah Peminjaman Sepeda Harian")
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(filtered_df['dteday'], filtered_df['cnt'], marker='o', linestyle='-')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig)

# Distribusi berdasarkan season
st.subheader("Distribusi Peminjaman Berdasarkan Musim (Season)")
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
filtered_df['season'] = filtered_df['season'].map(season_map)
fig, ax = plt.subplots()
sns.boxplot(x='season', y='cnt', data=filtered_df, palette="coolwarm", ax=ax)
st.pyplot(fig)

# Distribusi berdasarkan weekday
st.subheader("Rata-rata Peminjaman Berdasarkan Hari")
weekday_map = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
filtered_df['weekday'] = filtered_df['weekday'].apply(lambda x: weekday_map[x])
weekday_avg = filtered_df.groupby('weekday')['cnt'].mean().reindex(weekday_map)
fig, ax = plt.subplots()
weekday_avg.plot(kind='bar', ax=ax, color="#90CAF9")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

# Hubungan antara suhu dan peminjaman
st.subheader("Hubungan Suhu dengan Jumlah Peminjaman")
fig, ax = plt.subplots()
sns.scatterplot(x='temp', y='cnt', data=filtered_df, ax=ax)
st.pyplot(fig)
