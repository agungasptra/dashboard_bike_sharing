import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# Load dataset
day_df = pd.read_csv("day.csv")

# Cleaning data
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'hum': 'humidity',
    'cnt': 'total_rentals',
    'atemp': 'feels_like_temp',
    'temp': 'temperature',
    'windspeed': 'wind_speed',
    'weathersit': 'weather_condition',
}, inplace=True)
day_df.drop(columns=['instant'], inplace=True)
day_df.drop_duplicates(inplace=True)

# Sidebar - Rentang tanggal
min_date = day_df['date'].min()
max_date = day_df['date'].max()

with st.sidebar:
    st.title("Bike Sharing Dashboard")
    st.markdown("### Select Date Range:")
    date_range = st.date_input(
        "Date Range",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Validasi input tanggal
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.warning("⚠️ Please select two dates to set the date range.")
    st.stop()

# Filter data berdasarkan tanggal
filtered_df = day_df[(day_df['date'] >= pd.to_datetime(start_date)) & 
                     (day_df['date'] <= pd.to_datetime(end_date))]

# Header
st.title("📊 Bike Sharing Dataset Dashboard")

# METRIC
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Rentals", value=int(filtered_df['total_rentals'].sum()))
with col2:
    st.metric("Average Rentals", value=round(filtered_df['total_rentals'].mean(), 2))

# Grafik jumlah peminjaman per hari
st.subheader("Daily Bike Rentals")
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(filtered_df['date'], filtered_df['total_rentals'], marker='o', linestyle='-')
ax.set_xlabel("Date")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

# Distribusi berdasarkan season
st.subheader("Rentals Distribution by Season")
season_map = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
filtered_df['season'] = filtered_df['season'].map(season_map)
fig, ax = plt.subplots()
sns.boxplot(x='season', y='total_rentals', data=filtered_df, palette="coolwarm", ax=ax)
st.pyplot(fig)

# Distribusi berdasarkan weekday
st.subheader("Average Rentals by Weekday")
weekday_map = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
filtered_df['weekday'] = filtered_df['weekday'].apply(lambda x: weekday_map[x])
weekday_avg = filtered_df.groupby('weekday')['total_rentals'].mean().reindex(weekday_map)
fig, ax = plt.subplots()
weekday_avg.plot(kind='bar', ax=ax, color="#90CAF9")
ax.set_ylabel("Average Rentals")
st.pyplot(fig)

# Hubungan antara suhu dan peminjaman
st.subheader("Temperature vs Total Rentals")
fig, ax = plt.subplots()
sns.scatterplot(x='temperature', y='total_rentals', data=filtered_df, ax=ax)
st.pyplot(fig)
