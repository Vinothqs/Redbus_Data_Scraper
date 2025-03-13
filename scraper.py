from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
import time

# List of cities and their corresponding states
city_state_mapping = {
    "Hyderabad": "Telangana",
    "Vijayawada": "Andhra Pradesh",
    "Chennai": "Tamil Nadu",
    "Bangalore": "Karnataka",
    "Delhi": "Delhi",
    "Jaipur": "Rajasthan",
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra"
}

# Setup SQLite database
conn = sqlite3.connect("bus_data.db")
cursor = conn.cursor()

# Create table with 'state' column
cursor.execute("""
CREATE TABLE IF NOT EXISTS bus_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    destination TEXT,
    state TEXT,  -- New column for state
    bus_name TEXT,
    departure_time TEXT,
    price TEXT,
    rating TEXT
)
""")
conn.commit()

# Setup Firefox WebDriver
driver = webdriver.Firefox()

# Loop through all city combinations
for source in city_state_mapping.keys():
    for destination in city_state_mapping.keys():
        if source != destination:  # Avoid same-city routes
            url = f"https://www.redbus.in/bus-tickets/{source.lower()}-to-{destination.lower()}"
            driver.get(url)

            # Wait for page to load
            time.sleep(5)

            # Extract Bus Details
            bus_names = driver.find_elements(By.XPATH, "//div[contains(@class, 'travels') and contains(@class, 'f-bold')]")
            departure_times = driver.find_elements(By.XPATH, "//div[contains(@class, 'column-two') and contains(@class, 'p-right-10') and contains(@class, 'w-30')]")
            prices = driver.find_elements(By.XPATH, "//div[contains(@class, 'fare')]//span")
            ratings = driver.find_elements(By.XPATH, "//div[contains(@class, 'rating')]//span")

            # Get state from mapping
            state = city_state_mapping[source]

            # Save data to database
            for i in range(len(bus_names)):
                name = bus_names[i].text.strip() if i < len(bus_names) else "N/A"
                time_ = departure_times[i].text.strip() if i < len(departure_times) else "N/A"
                price = prices[i].text.strip() if i < len(prices) else "N/A"
                rating = ratings[i].text.strip() if i < len(ratings) else "N/A"

                cursor.execute("INSERT INTO bus_data (source, destination, state, bus_name, departure_time, price, rating) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (source, destination, state, name, time_, price, rating))
                conn.commit()

            print(f"✅ Data extracted for {source} ({state}) to {destination}")

# Close database & browser
conn.close()
driver.quit()
print("🎉 Scraping completed for all routes!")