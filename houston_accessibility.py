import osmnx as ox # package that works with OSM data
import folium # py library for interactive leaflet maps
import geopandas as gpd # package that extends functionality of DF by adding new data type: vector & raster
import pandas as pd # library for data analysis, primarily dataframs

# 1. Defining location of study 
city = "Houston, Texas, USA"

# Download the road network for Houston
# This is a NetworkX graph object
graph = ox.graph_from_place(city, network_type="drive")

# Convert edges to a GeoDataFrame
gdf_edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

# Create a folium map centered on Houston
center = gdf_edges.unary_union.centroid
m = folium.Map(location=[center.y, center.x], zoom_start=10)

# Plot road lines
for _, row in gdf_edges.iterrows():
    folium.PolyLine(
        locations=[(lat, lon) for lon, lat in row["geometry"].coords],
        color="gray",
        weight=1,
        opacity=0.5,
    ).add_to(m)

# 2. Get medical facilities from OpenStreetMap
tags = {"amenity": ["hospital", "clinic", "doctors", "pharmacy"]}
pois = ox.features_from_place(city, tags)

# Plot medical facilities as red dots
for _, row in pois.iterrows():
    geom = row.geometry
    if geom.geom_type == "Point":
        folium.CircleMarker(
            location=[geom.y, geom.x],
            radius=4,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            popup=row.get("name", "Unnamed Facility")
        ).add_to(m)

# 3. Add census tracts (Houston/Harris County)
# Make sure you have this shapefile extracted:
# accessibility-map/tracts/tl_2025_48_tract.shp
tracts = gpd.read_file("tracts/tl_2025_48_tract.shp")

# Filter for Harris County (Houston area)
houston_tracts = tracts[tracts["COUNTYFP"] == "201"]

# 4. Count medical facilities per tract
pois_gdf = gpd.GeoDataFrame(pois, geometry="geometry", crs="EPSG:4326")
houston_tracts = houston_tracts.to_crs("EPSG:4326")

# Spatial join: assign each facility to a tract
join = gpd.sjoin(pois_gdf, houston_tracts, how="inner", predicate="within")
facility_counts = join.groupby("TRACTCE").size().reset_index(name="facility_count")

# Merge counts back into tracts
houston_tracts = houston_tracts.merge(facility_counts, on="TRACTCE", how="left")
houston_tracts["facility_count"] = houston_tracts["facility_count"].fillna(0)

# 5. Add population data and compute facilities per capita
try:
    population = pd.read_csv("data/harris_population.csv")

    # Build GEOID = state (2 digits) + county (3 digits) + tract (6 digits)
    population["GEOID"] = (
        population["state"].astype(str).str.zfill(2)
        + population["county"].astype(str).str.zfill(3)
        + population["tract"].astype(str).str.zfill(6)
    )

    # Rename Total_Population to population
    population = population.rename(columns={"Total_Population": "population"})

    population["GEOID"] = population["GEOID"].astype(str)
    houston_tracts["GEOID"] = houston_tracts["GEOID"].astype(str)

    # Merge with tract data
    houston_tracts = houston_tracts.merge(
        population[["GEOID", "population"]],
        on="GEOID",
        how="left"
    )

    # verify that population data merged correctly with tracts before generating the map
    print("Merge check — sample data:")
    print(houston_tracts[["GEOID", "TRACTCE", "population", "facility_count"]].head(10))
    print("Number of tracts with missing population:", houston_tracts["population"].isna().sum())


    # Compute facilities per 10,000 residents
    houston_tracts["facilities_per_10k"] = (
        houston_tracts["facility_count"] / houston_tracts["population"]
    ) * 10000
    houston_tracts["facilities_per_10k"] = houston_tracts["facilities_per_10k"].fillna(0)

except FileNotFoundError:
    print("Population file not found. Skipping per-capita calculation.")
    houston_tracts["facilities_per_10k"] = houston_tracts["facility_count"]

# 6. Add median income data (optional)
try:
    income = pd.read_csv("data/harris_median_income.csv")
    income["GEOID"] = income["GEOID"].astype(str)
    houston_tracts["GEOID"] = houston_tracts["GEOID"].astype(str)
    houston_tracts = houston_tracts.merge(
        income[["GEOID", "median_income"]],
        on="GEOID",
        how="left"
    )
    print("Median income data merged successfully.")
except FileNotFoundError:
    print("Median income file not found. Skipping income layer.")

# 7. Create the interactive choropleth map
folium.Choropleth(
    geo_data=houston_tracts,
    data=houston_tracts,
    columns=["TRACTCE", "facilities_per_10k"],
    key_on="feature.properties.TRACTCE",
    fill_color="YlOrRd",
    fill_opacity=0.8,
    line_opacity=0.4,
    legend_name="Healthcare Facilities per 10,000 Residents",
).add_to(m)

# Hover tooltip
folium.GeoJson(
    houston_tracts,
    style_function=lambda x: {"color": "black", "weight": 0.3, "fillOpacity": 0},
    tooltip=folium.GeoJsonTooltip(
        fields=["TRACTCE", "facility_count", "facilities_per_10k"],
        aliases=["Tract ID:", "Facilities:", "Facilities per 10k:"],
        localize=True
    )
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Save and open map
m.save("houston_medical_facilities_with_tracts.html")
print("Map saved as 'houston_medical_facilities_with_tracts.html'")
