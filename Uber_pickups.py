import streamlit as st
import pandas as pd
import numpy as np

st.title("Uber pickups in NYC")

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(columns=lambda column: str(column).lower(), inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Done! Data cached.")

st.caption(
    "First 10,000 records from the September 2014 "
    "NYC Uber pickups tutorial dataset."
)

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

st.subheader("Number of pickups by hour")

hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour,
    bins=24,
    range=(0, 24),
)[0]

hourly_pickups = pd.DataFrame(
    {"Pickups": hist_values},
    index=pd.Index(range(24), name="Hour"),
)

st.bar_chart(hourly_pickups)

hour_to_filter = st.slider(
    "Hour",
    min_value=0,
    max_value=23,
    value=17,
)

filtered_data = data[
    data[DATE_COLUMN].dt.hour == hour_to_filter
]

st.subheader(f"Map of pickups at {hour_to_filter:02d}:00")
st.write(f"{len(filtered_data):,} pickups during this hour.")
st.map(filtered_data)