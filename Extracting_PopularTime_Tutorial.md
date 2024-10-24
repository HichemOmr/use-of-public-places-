# Extracting PopularTime
## Overview

This project involves extracting popular times data for various places using the Google Places API and processing this data into a structured format. The data is retrieved using the `populartimes` Python package and saved into Excel files for each place.
There are 2 parts:
- Demo Part: where you can use a goople place id to try, it will retrive the data for the desired place
- Main Part: this is the script that helps you to get populartime for all places using an excel input


## Code Structure

The project consists of the following files:

1. **`popular_times.ippynb`**: Handles data retrieval from the Google Places API, processes the data, and saves it into Excel files. You can find it in src
2. **`SusDens-Database (Final).xlsx`**: Contains place IDs for which the popular times data needs to be retrieved.
3. **Output Files**: 
   - **`places_with_data.xlsx`**: Lists places for which popular times data was successfully retrieved.
   - **`places_without_data.xlsx`**: Lists places for which no popular times data was found.
   - **`errors.xlsx`**: Lists errors encountered during data retrieval.

## Prerequisites

1. **Python 3.6+**: Ensure Python is installed on your system. Download it from [python.org](https://www.python.org/downloads/).
2. **Google Places API Key**: Obtain an API key from Google Places API. 
3. **Required Python Packages**: Install the required packages using `pip`.
## Running the Script

1. **Set Up**:
   - Ensure you have the necessary packages installed: `populartimes`, `pandas`, and `openpyxl`.
   - Obtain and set your API key in the script.

2. **Execute**:
   - Run the script in a Python environment.
   - Ensure you are pointing out to the correct file path of the SusDens-Database (Final).xlsx file in the script. If you need to use a different Excel file to update the data, replace the input_file variable with the path to your new file

3. **Check Results**:
   - The results will be saved in the `out/popular_times` directory.
   - Review the generated Excel files for data and error logs.

By following these instructions, you should be able to retrieve and process popular times data efficiently while handling any potential issues.
## Script Workflow

### 1. Load Place IDs

- **Description**: Reads place IDs from the file `SusDens-Database (Final).xlsx`.
- **Purpose**: Extracts the list of place IDs for which the popular times data will be retrieved.
- **Details**: The file should be an Excel spreadsheet containing a column with place IDs.

### 2. Create Output Directory

- **Description**: Creates a directory named `popular_times` (or any name you specify) to store the results.
- **Purpose**: Ensures that there is a designated folder where all the processed data files will be saved.
- **Details**: The directory is created if it does not already exist.

### 3. Retrieve and Process Data

- **Description**: For each place ID, retrieves popular times data from the Google API.
- **Purpose**: Fetches and formats the popular times data for each place.
- **Details**:
  - Retrieves data using the Google API and the provided place IDs.
  - Formats the data into a DataFrame.
  - Saves the formatted data into an Excel file named after the place.

### 4. Error Handling

- **Description**: Logs places with missing data or errors into separate Excel files.
- **Purpose**: Keeps track of places that either have no popular times data or encountered errors during data retrieval.
- **Details**: 
  - `places_with_data.xlsx` records places for which data was successfully retrieved.
  - `places_without_data.xlsx` lists places with no available popular times data.
  - `errors.xlsx` contains details about any errors encountered.

### 5. Rate Limiting

- **Description**: Includes a 1-second delay between API requests to respect rate limits.
- **Purpose**: Ensures compliance with API usage policies and prevents hitting rate limits.
- **Details**: A `time.sleep(1)` command is used to pause execution between requests.


