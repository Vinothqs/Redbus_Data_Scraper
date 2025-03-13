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

# Fetch unique cities and states from the database
cursor.execute("SELECT DISTINCT source FROM bus_data")
sources = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT DISTINCT destination FROM bus_data")
destinations = [row[0] for row in cursor.fetchall()]

# **Manually define states (for now, since your DB doesn't have a state column)**
state_mapping = {
    "Hyderabad": "Telangana",
    "Vijayawada": "Andhra Pradesh",
    "Chennai": "Tamil Nadu",
    "Bangalore": "Karnataka",
    "Delhi": "Delhi",
    "Jaipur": "Rajasthan",
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra"
}
states = list(set(state_mapping.values()))

# Sidebar Filters
st.sidebar.header("🔍 Search Buses")

# **State Dropdown**
selected_state = st.sidebar.selectbox("Select State", ["All"] + states)

# **Source & Destination Dropdowns**
source = st.sidebar.selectbox("From (Source)", sources)
destination = st.sidebar.selectbox("To (Destination)", destinations)

# **Price Range Slider**
min_price, max_price = st.sidebar.slider("Price Range (₹)", min_value=0, max_value=5000, value=(500, 3000))

# **Star Rating Filter**
min_rating = st.sidebar.slider("Minimum Star Rating", min_value=0.0, max_value=5.0, value=3.0, step=0.1)

# Sorting Options
sort_by = st.sidebar.radio("Sort by", ["Bus Name", "Departure Time", "Price", "Ratings"])

# **Query the database based on filters**
query = "SELECT id, source, destination, bus_name, departure_time, price, rating FROM bus_data WHERE source=? AND destination=?"
df = pd.read_sql_query(query, conn, params=(source, destination))

# **Filter by State**
if selected_state != "All":
    df = df[df["source"].map(state_mapping) == selected_state]

# **Filter by Price Range**
df["price"] = df["price"].astype(str).str.replace("₹", "").str.replace(",", "").astype(float)  # Convert price to float
df = df[(df["price"] >= min_price) & (df["price"] <= max_price)]

# **Filter by Star Rating**
df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)  # Convert ratings to float
df = df[df["rating"] >= min_rating]

# **Apply Sorting**
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

# Display Table
st.markdown(f"## Buses from **{source}** to **{destination}**")
st.dataframe(df.style.set_properties(**{'text-align': 'center', 'border': '1px solid black', 'background-color': '#f9f9f9'}))

st.success("🎉 Search complete! Find the best buses for your journey.")