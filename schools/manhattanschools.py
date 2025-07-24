import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

df = pd.read_excel("schoolsfinal_all_coordinates_merged.xlsx")

geolocator = Nominatim(user_agent="school_geocoder")

def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        sleep(1)  
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
        return pd.Series([None, None])

df["full_address"] = df["school_id"].astype(str) + ", Manhattan, New York, NY"

missing_mask = df["Latitude"].isnull() | df["Longitude"].isnull()
df.loc[missing_mask, ["Latitude", "Longitude"]] = df.loc[missing_mask, "full_address"].apply(get_coordinates)

df.to_excel("schoolsfinal_all_coordinates_updated.xlsx", index=False)

print(" Done! check files for schoolsfinal_all_coordinates_updated.xlsx")
