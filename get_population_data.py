# get_population_data.py
import requests
import pandas as pd

url = "https://api.census.gov/data/2022/acs/acs5"
params = {
    "get": "B01003_001E,NAME",
    "for": "tract:*",
    "in": "county:201 state:48"  # Harris County, TX
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data[1:], columns=data[0])
df.rename(columns={"B01003_001E": "Total_Population"}, inplace=True)
df["Total_Population"] = df["Total_Population"].astype(int)

# Save to CSV for later use
df.to_csv("data/harris_population.csv", index=False)
print("✅ Population data saved to data/harris_population.csv")
