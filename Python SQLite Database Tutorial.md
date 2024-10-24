This tutorial will guide you through inserting data into your SQLite database and updating columns using Python.  
Please check **src** and use the script code `Coding-for-Database.ipynb`.

# Database-for-SusDens

This project involves creating and managing a SQLite database for the "Database-for-SusDens" using Python. Below is an overview of the code structure, key processes, and instructions on how to run the code.

## Overview and Structure of the Code

### 1. Environment Setup:
- The notebook begins by importing necessary libraries (`os`, `sqlite3`, `pandas`) and setting up the environment.
- The current working directory is printed to ensure the correct path for file operations.

### 2. Data Loading:
- The Excel file `data/SusDens-Database (Final).xlsx` is loaded into a pandas DataFrame. This file contains place information that will be processed and inserted into the SQLite database.

### 3. SQLite Database Interaction:
- The SQLite database (new_database.db) is defined as a constant (DATABASE_NAME), and you only need to connect to it using this constant.
- The `Place` table is prepared by selecting and renaming relevant columns from the DataFrame.
- Data types are checked and corrected before insertion into the database.
- A helper function `insert_data_from_df` is defined to insert the data into the SQLite table.

### 4. Data Insertion:
- The processed data is inserted into the `Place` table within the SQLite database.

## How to Run the Code

### 1. Setup:
- Ensure that Python is installed on your machine, along with the necessary libraries (`pandas`, `sqlite3`, `openpyxl`).
- Place the `SusDens-Database (Final).xlsx` file in the appropriate directory or update the `excel_file` path variable in the notebook.

### 2. Execution:
- Run the notebook cells sequentially to load data from the Excel file, process it, and insert it into the SQLite database.
- The database file (new_database.db) already exists, and you only need to connect to it. However, if the file does not exist, the code will automatically create the new one. Please ensure that you are working in the correct directory to connect to the existing database

### 3. Customization:
- If you have a different dataset or want to update existing data, modify the `excel_file` path and reload the notebook.
- Adjust the schema or data processing steps as needed for new data.
## Additional Instructions

### For `PopularTime`, `reviews`, and `photos`
- Follow a similar process for handling `PopularTime`, `reviews`, and `photos` data:
  - Prepare the respective tables by selecting and renaming relevant columns from the DataFrames.
  - Check and correct data types as needed before insertion.
  - Define and use appropriate helper functions for inserting data into these tables.
- If you need to update data, replace the path to the new variable and rerun the relevant cells in the notebook. I always have a titile for inserting data. You can look for it by searching 'Inserting data for xx table'

### Note on Table/Column Names
- When updating or modifying the database schema, make sure that the columns of table names in the script correspond with those in the current database schema. Column names may have changed due to schema updates.
- Verify and update table/column names in the script if necessary to match the current schema in the database.

### Adding New Columns
- SQLite does not allow direct modification of table schemas to add new columns.
- To add a new column:
  1. Create a temporary table with the new column.
  2. Copy data from the existing table into the temporary table.
  3. Rename the temporary table to replace the old table.
  4. Ensure that the new column is correctly populated with relevant data.




