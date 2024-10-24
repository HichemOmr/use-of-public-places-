# Green Spaces in Luxembourg

This project is a Streamlit application that visualizes green spaces in Luxembourg using Google Places API data. It allows users to filter places by categories and download relevant data, including user reviews. The application displays locations on an interactive map, providing detailed information about each place. The provided flowchart could be useful to follow the steps. 

![SusDens drawio (2)](https://github.com/user-attachments/assets/9acf240e-b658-490e-a782-a399d5150a4a)


## Overpass API - OpenStreetMap Query Tool
We're going to define a dictionary for finding all green public areas in Luxembourg using Overpass QL. Here’s a structured approach:

## Step-by-Step Approach
**Identify Tags**: Determine the specific tags in OpenStreetMap that correspond to green public areas.
**Create a Dictionary**: Define these tags in a dictionary format.
**Write the Overpass Query**: Use the dictionary to construct an Overpass query.

### Dictionary Definition
Here is a dictionary with common tags used to identify green public areas:

[https://overpass-turbo.eu/] 
```
[out:json];
(
  node["leisure"="park"];
  node["landuse"="forest"];
  node["natural"="wood"];
  node["leisure"="garden"];
  node["leisure"="recreation_ground"];
  node["leisure"="nature_reserve"];
  node["landuse"="meadow"];
  node["landuse"="grass"];
  node["natural"="grassland"];
);
out body;
```
The script will output a JSON structure containing the details of all green public areas in Luxembourg, including their nodes. 

##  Excluding locations outside of LUX borders
There were some green spaces in border areas, e.g. Arlon or Metz. 
Removing unnecessary POIs by determining Luxembourg Country Border Line will improve accuracy of our model and results. 
 
The dataset is availabe on the [Country National Data Portal](https://data.public.lu/en/datasets/luxembourgish-country-border-5k-coordinates/) 

![image](https://github.com/user-attachments/assets/a53e2d0e-9fb8-4d48-81af-688b132b3190)


```python
import requests
import pandas as pd
import time
from shapely.geometry import Point, Polygon
import folium

# Function to search for places
def search_places(api_key, location, radius, place_type, next_page_token=None):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={place_type}&key={api_key}"
    if next_page_token:
        url += f"&pagetoken={next_page_token}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
```
 Define the boundaries of Luxembourg (simplified polygon) 
```python
luxembourg_boundary = Polygon(border_coords)

# Function to check if a point is within Luxembourg
def is_in_luxembourg(lat, lon):
    point = Point(lon, lat)
    return luxembourg_boundary.contains(point)

# Your Google Maps API key
#api_key = 'YOUR_API_KEY'

# Luxembourg coordinates
luxembourg_location = "49.815273,6.129583"

# Search radius in meters
radius = 50000  # 50 km

# DataFrame to store the results
results = []
```
Search for each type of place 
```python
for place_type in place_types:
    next_page_token = None

    while True:
        places = search_places(api_key, luxembourg_location, radius, place_type, next_page_token)

        if places and places['results']:
            for place in places['results']:
                latitude = place['geometry']['location']['lat']
                longitude = place['geometry']['location']['lng']
                in_luxembourg = is_in_luxembourg(latitude, longitude)

                results.append({
                    'name': place['name'],
                    'address': place.get('vicinity', 'N/A'),
                    'latitude': latitude,
                    'longitude': longitude,
                    'type': place_type,
                    'in_luxembourg': in_luxembourg
                })

        next_page_token = places.get('next_page_token')
        if not next_page_token:
            break

        # Pause to avoid exceeding request limits
        time.sleep(2)

# Convert results to DataFrame
df = pd.DataFrame(results)
```
At the end of this phse, we initiate a ready-to-use dataset for the research in our country public green environment. 
It is also worth mentioning that we are able to apply our code to other countries and/ areas just by replacing new coordinates. 

