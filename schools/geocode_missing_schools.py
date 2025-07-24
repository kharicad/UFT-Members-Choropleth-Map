import pandas as pd
import requests
from time import sleep

# === Step 1: Load your data ===
df = pd.read_excel("schoolsfinal_still_missing_after_all_matching.xlsx")

API_KEY = "AIzaSyDfsl1mjjNVgkHyd1WMVrYqyPxfmCa7lSQ"

# === Step 3: Geocode function ===
def geocode_google(search_name):
    query = f"{search_name}, Manhattan, New York, NY"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": query, "key": API_KEY}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return pd.Series([location["lat"], location["lng"]])
        else:
            return pd.Series([None, None])
    except Exception as e:
        print(f"Error for {query}: {e}")
        return pd.Series([None, None])

# === Step 4: Apply to each row ===
df[["Latitude", "Longitude"]] = df["search_name"].apply(geocode_google)
    # You can increase this delay if you get errors
    # Google has rate limits (~50/sec with some burst allowed)
sleep(1)


df.to_excel("schoolsfinal_geocoded_from_google.xlsx", index=False)
print("✅ Done! File saved as schoolsfinal_geocoded_from_google.xlsx")
