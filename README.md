Houston Accessibility Map
A geospatial analysis project exploring how equitably healthcare facilities are distributed across Houston.
This project builds an interactive map that displays the accessibility of healthcare facilities across Houston census tracts. By combining OpenStreetMap (OSM) facility data with U.S. Census socioeconomic data, the project evaluates spatial equity and helps identify neighborhoods that may face disproportionate barriers to care.
1. Healthcare Facility Data (Primary)
OpenStreetMap via osmnx


Filtered for points tagged as:


amenity=hospital


amenity=clinic


amenity=doctor


healthcare=*


Hiccup: OSM tags are inconsistent. Clinics don't always share uniform labeling, and doctor’s offices sometimes lack healthcare tags. I had to expand the search tag set and validate manually.

2. Socioeconomic Data (Optional / If included)
US Census Bureau, ACS 5-Year Estimates


Intended variables:


Median household income


Population


Insurance coverage rates


Vehicle availability


Hiccup: Income data wasn’t immediately accessible through the API due to a misunderstanding of table codes. Needed additional lookup time, and some variables had to be modified.

3. Census Tract Boundaries
TIGER/Line shapefiles or osmnx.geometries_from_place()



What the Map Shows
Each census tract is represented as a polygon. When you hover over a tract, the map displays:
Tract ID


Distance to the nearest healthcare facility


Number of facilities within a selected radius


Any additional demographic overlays (if used)


Color shading indicates accessibility — e.g., darker shades represent longer distances from facilities.

Methodology
Download all Houston tract geometries


Pull all healthcare-related points from OSM


Convert coordinates and geometries into GeoPandas objects


Compute:


Nearest facility distance per tract


Facility counts within buffer radii


Join the data to census tract shapefiles


Build an interactive folium map


Display tract identifiers


Technologies Used
Python


GeoPandas


OSMnx


Shapely


Folium


Pandas



Future Improvements
Add analysis of travel times using road networks (Graph-based routing)


Incorporate public transit accessibility


Expand to other types of care (mental health, urgent care, specialists)


Normalize facility density by population or age distribution


License
Open source
