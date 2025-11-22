# Houston Accessibility Map
**A geospatial analysis project exploring how equitably healthcare facilities are distributed across Houston.**

This project builds an interactive map that displays the accessibility of healthcare facilities across Houston census tracts. By combining OpenStreetMap (OSM) facility data with U.S. Census socioeconomic data, the project evaluates spatial equity and helps identify neighborhoods that may face disproportionate barriers to care.

## Healthcare Facility Data

OpenStreetMap via osmnx

Filtered for points tagged as:

amenity=hospital

amenity=clinic

amenity=doctor

healthcare=*

Hiccup: OSM tags are inconsistent. Clinics don't always share uniform labeling, and doctor’s offices sometimes lack healthcare tags. I had to expand the search tag set and validate manually.

## Socioeconomic Data

US Census Bureau, ACS 5-Year Estimates

Intended variables:

Median household income

Population

Insurance coverage rates

Vehicle availability

Hiccup: Income data wasn’t immediately accessible through the API due to a misunderstanding of table codes. Needed additional lookup time, and some variables had to be modified.

## Census Tract Boundaries

TIGER/Line shapefiles or osmnx.geometries_from_place()

## What the Map Shows

Each census tract is represented as a polygon. When you hover over a tract, the map displays:
Tract ID

Distance to the nearest healthcare facility

Number of facilities within a selected radius

Any additional demographic overlays (if used)

Color shading indicates accessibility — e.g., darker shades represent longer distances from facilities.

## Built With
Python

GeoPandas

OSMnx

Shapely

Folium

Pandas

