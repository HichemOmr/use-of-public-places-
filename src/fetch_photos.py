import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import requests
import base64
import os
import zipfile
from io import BytesIO
import concurrent.futures
import time
from ast import literal_eval
from requests.exceptions import RequestException

# Load the data (example of loading remaining rows)
file_path = 'S:/Echange/Places Data Collection/Nahid/SusDens-Database (Final).xlsx'
data = pd.read_excel(file_path, skiprows=range(1, 1851), nrows=100)

# Google Places API key
API_KEY = 'AIzaSyCNHQyYOQtDKiySFR_O4hy_a1dTHewX8Gw'

# Function to categorize types
def categorize_types(types):
    if 'campground' in types:
        return 'Campground'
    elif 'zoo' in types:
        return 'Zoo'
    elif 'florist' in types:
        return 'Florist'
    elif 'tourist_attraction' in types:
        return 'Tourist Attraction'
    elif 'natural_feature' in types:
        return 'Natural Feature'
    else:
        return 'Park'

# Safely evaluate types column
data['category'] = data['types'].apply(lambda x: categorize_types(literal_eval(x)))

# Streamlit app setup
st.title('Green Spaces in Luxembourg')

# Sidebar for selecting types
type_options = ['All'] + list(data['category'].unique())
selected_types = st.sidebar.multiselect(
    'Select Types',
    options=type_options,
    default=['Park']
)

# Filter data based on selected types
filtered_data = data if 'All' in selected_types else data[data['category'].isin(selected_types)]

# Update place list based on selected types
place_names = ['All'] + list(filtered_data['name'].unique())
selected_place = st.sidebar.selectbox('Select Place', place_names)

# Filter data for the selected place
selected_place_data = filtered_data if selected_place == 'All' else filtered_data[filtered_data['name'] == selected_place]

# Create map
map_center = [49.6116, 6.1319]
lux_map = folium.Map(location=map_center, zoom_start=12)
marker_cluster = MarkerCluster().add_to(lux_map)

# Add markers to the map
for idx, row in selected_place_data.iterrows():
    location = [row['geometry.location.lat'], row['geometry.location.lng']]
    category = row['category']
    types = literal_eval(row['types'])
    folium.Marker(
        location=location,
        popup=f"{row['name']}: {category}, {', '.join(types)}",
        icon=folium.Icon(color='green' if category == 'Park' else
                         'blue' if category == 'Campground' else
                         'red' if category == 'Natural Feature' else
                         'purple' if category == 'Zoo' else
                         'pink' if category == 'Florist' else
                         'orange' if category == 'Amusement Park' else
                         'cadetblue' if category == 'Tourist Attraction' else 'gray')
    ).add_to(marker_cluster)

# Save and display the map
map_path = 'filtered_luxembourg_green_spaces_map.html'
lux_map.save(map_path)
st.components.v1.html(open(map_path, 'r', encoding='utf-8').read(), height=600)

# Option to download filtered data as CSV
st.sidebar.header('Export Filtered Data')
if st.sidebar.button('Export data as CSV'):
    filtered_data.to_csv('filtered_data.csv', index=False)
    st.sidebar.write('Download the filtered dataset:', 'filtered_data.csv')

# Generate download link for the CSV file
def generate_download_link(dataframe, filename='filtered_data.csv'):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'
    return href

st.sidebar.markdown(generate_download_link(filtered_data), unsafe_allow_html=True)

# Function to fetch a single photo with retry logic
def fetch_photo(photo_reference):
    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"
    max_retries = 5
    backoff_factor = 1
    for attempt in range(max_retries):
        try:
            response = requests.get(photo_url)
            response.raise_for_status()
            return response.content
        except RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
            else:
                raise e

# Function to fetch photos
def fetch_photos(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}"
    response = requests.get(url)
    place_details = response.json()
    return place_details.get('result', {}).get('photos', [])

# Function to create a zip file in-memory with subfolders for each place
def create_zip_with_subfolders(data):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for place_name in data['name'].unique():
            place_id = data[data['name'] == place_name]['place_id'].values[0]
            photos = fetch_photos(place_id)
            if photos:
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    photo_contents = list(executor.map(fetch_photo, [photo['photo_reference'] for photo in photos]))
                for i, photo_content in enumerate(photo_contents):
                    zip_file.writestr(f'{place_name}/{place_name}_photo_{i}.jpg', photo_content)
    zip_buffer.seek(0)
    return zip_buffer

# Display option to download photos
if st.sidebar.button('Download All Photos'):
    zip_buffer = create_zip_with_subfolders(filtered_data)
    b64 = base64.b64encode(zip_buffer.read()).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="all_places_photos.zip">Click here to download the photos</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
