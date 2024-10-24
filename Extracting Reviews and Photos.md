### 1. Importing Necessary Libraries
```python
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
```
This section imports all necessary libraries, including Streamlit for building the web app, Pandas for data manipulation, Folium for map visualization, and several utilities for handling HTTP requests, file operations, and more.

### 2. Loading Data
```python
file_path = 'S:/Echange/Places Data Collection/Nahid/SusDens-Database (Final).xlsx'
data = pd.read_excel(file_path)
```
Loads the dataset containing information about various places in Luxembourg from an Excel file.

### 3. Google Places API Key 
### 3.1. Generate Google Maps API Key
#### 3.1.1. Create a Google Cloud account and navigate to the Google Cloud Console.
#### 3.1.2. Create a new project and enable the Google Places API.
#### 3.1.3. Generate a new API key for the project and restrict it to the necessary services and domains.
```python
API_KEY = 'your_api_key_here'
```
Defines the Google Places API key used to fetch additional information, such as reviews for the places. 

### 4. Categorizing Place Types
```python
def categorize_types(types):
```
Defines a function to categorize places based on their types (e.g., Park, Zoo). This is used to filter and color-code the map markers.

### 5. Streamlit App Setup
```python
st.title('Green Spaces in Luxembourg')
# Sidebar setup and filters
```
Sets up the Streamlit application, including the title and sidebar filters for selecting place types and names.

### 6. Map Creation and Visualization
```python
map_center = [49.6116, 6.1319]
lux_map = folium.Map(location=map_center, zoom_start=12)
# Adding markers
```
Creates an interactive map centered on Luxembourg, adds markers for each place based on the selected filters, and displays the map in the Streamlit app.

### 7. Data Export Feature
```python
def generate_download_link(dataframe, filename='filtered_data.csv'):
   
```
Provides functionality for users to download the filtered data as a CSV file.

### 8.1. Fetching Reviews 
 Function to fetch reviews
```python
def fetch_reviews(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}"
    response = requests.get(url)
    place_details = response.json()
    return place_details.get('result', {}).get('reviews', [])
```
 Function to create a zip file in-memory with subfolders for each place's reviews
```python
def create_zip_with_subfolders(data):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for place_name in data['name'].unique():
            place_id = data[data['name'] == place_name]['place_id'].values[0]
            reviews = fetch_reviews(place_id)
            if reviews:
                for i, review in enumerate(reviews):
                    review_content = format_review_content(review)
                    zip_file.writestr(f'{place_name}/{place_name}_review_{i + 1}.txt', review_content)
    zip_buffer.seek(0)
    return zip_buffer
```
Function to format review content
```python
def format_review_content(review):
    author_name = review.get('author_name', 'Anonymous')
    rating = review.get('rating', 'N/A')
    text = review.get('text', 'No review text')
    timestamp = review.get('time', None)
    review_date = pd.to_datetime(timestamp, unit='s').strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'Unknown date'

    review_content = f"Author: {author_name}\n"
    review_content += f"Rating: {rating}\n"
    review_content += f"Date: {review_date}\n"
    review_content += f"Review:\n{text}\n"

    return review_content
```
Display option to download reviews 
```python
if st.sidebar.button('Download All Reviews'):
    zip_buffer = create_zip_with_subfolders(filtered_data)
    b64 = base64.b64encode(zip_buffer.read()).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="all_places_reviews.zip">Click here to download the reviews</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

```
### 8.2. Fetching Photos
```python
def fetch_photos(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}"
    response = requests.get(url)
    place_details = response.json()

    photos = place_details.get('result', {}).get('photos', [])
    return photos

# Function to create a zip file in-memory with subfolders for each place
def create_zip_with_subfolders(data):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for place_name in data['name'].unique():
            place_id = data[data['name'] == place_name]['place_id'].values[0]
            photos = fetch_photos(place_id)
            if photos:
                # Use ThreadPoolExecutor to download photos in parallel
                with concurrent.futures.ThreadPoolExecutor() as executor:
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

```

Contains functions to fetch reviews for each place using the Google Places API and to package them into a zip file for download.

