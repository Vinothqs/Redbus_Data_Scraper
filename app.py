import streamlit as st
import sqlite3
import pandas as pd

# Streamlit page config
st.set_page_config(page_title="RedBus Data Explorer", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>🚌 RedBus Data Explorer</h1>", unsafe_allow_html=True)

# Connect to SQLite database
conn = sqlite3.connect("bus_data.db")
cursor = conn.cursor()

# Fetch unique cities from the database
cursor.execute("SELECT DISTINCT source FROM bus_data")
sources = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT DISTINCT destination FROM bus_data")
destinations = [row[0] for row in cursor.fetchall()]

# Sidebar for filters
st.sidebar.header("🔍 Search Buses")

source = st.sidebar.selectbox("From (Source)", sources)
destination = st.sidebar.selectbox("To (Destination)", destinations)

# Date picker (optional)
journey_date = st.sidebar.date_input("Select Journey Date")

# Sorting options
sort_by = st.sidebar.radio("Sort by", ["Bus Name", "Departure Time", "Price", "Ratings"])

# Fetch buses based on selected source and destination
query = "SELECT id, source, destination, bus_name, departure_time, price, rating FROM bus_data WHERE source=? AND destination=?"
df = pd.read_sql_query(query, conn, params=(source, destination))

# Apply sorting
if sort_by == "Bus Name":
    df = df.sort_values(by="bus_name")
elif sort_by == "Departure Time":
    df = df.sort_values(by="departure_time")
elif sort_by == "Price":
    df = df.sort_values(by="price")
elif sort_by == "Ratings":
    df = df.sort_values(by="rating", ascending=False)

# Close the connection
conn.close()

# Display table
st.markdown(f"## Buses from **{source}** to **{destination}** on {journey_date}")

# Apply table styling
st.dataframe(df.style.set_properties(**{
    'text-align': 'center',
    'border': '1px solid black',
    'background-color': '#f9f9f9'
}))

st.success("🎉 Search complete! Find the best buses for your journey.")