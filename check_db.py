import sqlite3

# Connect to the database
conn = sqlite3.connect("bus_data.db")
cursor = conn.cursor()

# Fetch data from the bus_data table
cursor.execute("SELECT * FROM bus_data")
rows = cursor.fetchall()

# Print the data
if rows:
    for row in rows:
        print(row)
else:
    print("No data found in the database.")

# Close the connection
conn.close()