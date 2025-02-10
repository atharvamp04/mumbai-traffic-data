import requests
import os
import pandas as pd
from datetime import datetime

# Load API Key from GitHub Secrets
API_KEY = os.getenv("GMAPS_API_KEY")

# Define route stops (Modify as per your requirement)
ROUTE = [
    "Chhatrapati Shivaji Terminus, Mumbai",
    "Dadar, Mumbai",
    "Bandra, Mumbai",
    "Andheri, Mumbai",
    "Goregaon, Mumbai",
    "Borivali, Mumbai"
]

# Function to get travel time
def get_traffic_data(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&departure_time=now&traffic_model=best_guess&key={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        try:
            element = data["rows"][0]["elements"][0]
            travel_time = element["duration_in_traffic"]["text"]  # Travel time with traffic
            no_traffic_time = element["duration"]["text"]  # Travel time without traffic
            return travel_time, no_traffic_time
        except KeyError:
            return "N/A", "N/A"
    return "N/A", "N/A"

# Collect data for each stop
traffic_data = []
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for i in range(len(ROUTE) - 1):
    origin, destination = ROUTE[i], ROUTE[i + 1]
    travel_time, no_traffic_time = get_traffic_data(origin, destination)
    
    traffic_data.append({
        "Timestamp": timestamp,
        "From": origin,
        "To": destination,
        "Travel Time (With Traffic)": travel_time,
        "Travel Time (Without Traffic)": no_traffic_time
    })

# Convert to DataFrame and save as CSV
df = pd.DataFrame(traffic_data)
csv_filename = "mumbai_traffic_data.csv"

# Append to existing CSV if available
try:
    old_df = pd.read_csv(csv_filename)
    df = pd.concat([old_df, df], ignore_index=True)
except FileNotFoundError:
    pass

df.to_csv(csv_filename, index=False)
print(f"✅ Data saved to {csv_filename}")
