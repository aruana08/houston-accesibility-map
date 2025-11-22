# fetch_median_income.py
import requests
import pandas as pd

# Census API URL for median income by tract in Harris County, TX (state=48, county=201)
url = "https://api.census.gov/data/2023/acs/acs5"
params = {
    "get": "B19013_001E,NAME",
    "for": "tract:*",
    "in": "state:48 county:201"
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data[1:], columns=data[0])
df = df.rename(columns={
    "B19013_001E": "median_income",
    "state": "state",
    "county": "county",
    "tract": "tract"
})

df["median_income"] = pd.to_numeric(df["median_income"], errors="coerce")
df["GEOID"] = df["state"] + df["county"] + df["tract"]

print(df.head())
print(f"✅ Downloaded {len(df)} tracts with median income data")

# Save file
df.to_csv("data/harris_median_income.csv", index=False)
print("💾 Saved as data/harris_median_income.csv")
