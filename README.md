# CS 3270 Python Software Develpment 
## Module 11: Phase 11 Submit - Final Project Assignment
This project is a secure web application that lets a logged-in user upload an Australian weather CSV dataset and view interactive weather analytics by theme and city. The dashboard generates charts and a short summary using Python (pandas + matplotlib).

### Main Features
- User authentication (login/register/logout). All main pages require authentication.
- CSV upload + validation (required columns checked; shows missing columns if invalid).
- Dataset import into SQLite database (this becomes the data source for the dashboard).
- Interactive dashboard with 3 themes:
  - Temperature Trends
  - Rainfall Patterns
  - Extreme Indicators
- City selection updates the dashboard results (charts + summary).
- Generated charts are saved in `static/img/` and cleaned up on logout (keeps `australia.jpg`).

### System Architecture (High Level)
- **Presentation Layer:** HTML templates in `/templates` with styling in `/static/css`
- **Application Layer:** `app.py` handles routing, authentication, and page flow
- **Business Logic / Analytics Layer:** `functions.py` handles:
  - dataset validation
  - CSV import into DB
  - DB query -> pandas DataFrame (filter by city)
  - chart generation + summary text per theme
- **Data Layer:** SQLite database using SQLAlchemy (`User` table stores weather records)

### Dashboard Flow (How the UI Works)
1. User logs in.
2. If no dataset is loaded, user uploads a CSV file.
3. The CSV is validated and cleaned, then inserted into the database.
4. On the dashboard:
   - The user selects a theme using 3 buttons.
   - The user selects a city from the dropdown.
   - The dashboard automatically updates charts and summary on the same page (results load inside the dashboard view).

### CSV Upload + Processing
- The uploaded CSV is saved to the server.
- The dataset is validated against required columns.
- Data is cleaned/standardized (numeric conversion + RainToday converted to boolean).
- Clean rows are inserted into SQLite (previous dataset rows are replaced).

### Testing
A basic pytest file (`test_final_project.py`) was added to validate key functionality:
- Dataset validation detects missing columns.
- Trend functions return the expected output format: `(summary_string, [chart_paths])`.

### Iteration Notes / Challenges
- SQLAlchemy context issues were fixed by keeping DB operations inside the Flask request context and passing dependencies correctly.
- Matplotlib plotting in Flask required a non-interactive backend (`Agg`) to avoid GUI/thread errors.
- Dashboard layout was refined to improve chart sizing, two-column chart layout, and styled dropdowns/buttons.

### Modifications
- `templates` folder was updated with the created code for the app, adding the following files:
    - `index.html`
    - `login.html`
    - `register.html`
    - `upload.html`
    - `dashboard.html`
    - `dashboard_results.html`
- `app.py` file was modified to follow the requirements of the assignment, redirect to the html pages and store the logic of the database connection and app. 
- `functions.py` file was created as an assistant file to store all the functions that were called by `app.py`, some of them also manage logic, others create the charts and summary for the files.
- `test_final_project.py` file was created for testing. Allowing to test crucial functions of the app such as missing values handling, datasets with missing columns, and the trends correctly return the expected tuple of the summary and the charts list.
- `static` folder was modified in order to add the needed functionalities of a proper website, including the following folders:
    - `css`: adding `style.css` and `style2.css` for styling.
    - `img`: adding the needed images for data analytics when processed that going to be deleted after user logs out.
    - `js`: adding `script.js` for logic.

### How to Run the Application
1. Install all dependencies: `pip install -r requirements.txt`
2. Run the application: `python app.py`
3. Open web browser and navigate to `http://127.0.0.1:5001/`

## Module 10: Phase 10 Submit - Predictive Modeling Scikit-Learn
In this phase, the project was focused on Machine Learning applications. We were asked to implement a Machine Learning model on the Dataset that is being used. I added `module_10_weather_forecasting.ipynb` a python notebook where I implemented the Machine Learning model. 

### Modifications
- `requirements.txt` was modified adding seaborn and scikit-learn.
- `module_06_07.py` file was modified to switch the `RainToday` column from string values ("Yes", "No") to Boolean. More columns were added to the required columns and ended having the following:
    - Location, MinTemp, MaxTemp, Temp9am, Temp3pm, Rainfall, Humidity9am, Humidity3pm, Pressure9am, Cloud9am and RainToday.

### Objective
- Build a classification model that predicts **RainToday (True/False)**.
- Demonstrate core predictive modeling steps: feature selection, training/testing, evaluation, and interpretation.

### Model Used
- **RandomForestClassifier (scikit-learn)**
  - Trained on the training split and evaluated on the test split.
  - Random Forest was chosen because it handles non-linear relationships without heavy feature engineering.

### Features and Target
- **Target (y):** `RainToday`
- **Features (X):** weather variables known by ~9am.
- To reduce leakage and keep the task realistic, the following columns were **dropped** from X:
  - `RainToday` (target column)
  - `Temp3pm`, `Humidity3pm` (future-in-the-day measurements)
  - `Rainfall` (often directly determines RainToday; causes leakage)

> Note: `Location` is categorical, so it was converted into numeric features using **one-hot encoding** (dummy variables) before training.

### Evaluation Metrics
To evaluate model performance, I used:
- **classification_report** (precision, recall, F1-score)
- **confusion_matrix** (to visualize correct/incorrect predictions)


## Module 9: Phase 9 Submit - 3-tier Web Application
In this phase, the project was transitioned into a fully functional 3-tier web application. The goal was to demonstrate application tiering by separating the database, application logic, and user interface while allowing users to interact with and visualize the Australian weather dataset.

### The 3-Tier Architecture
- **Data Tier (Database):** Utilizes an SQLite database (`db.sqlite3`) managed through **SQLAlchemy ORM**. It stores over 95,000 cleaned weather records for rapid querying.
- **Logic Tier (Application):** Controlled by **Flask** and Python. It handles incoming requests, queries the database, processes clean data using Pandas from previous modules, and serves dynamic content.
- **Presentation Tier (User Interface):** Built with custom **HTML**, modern **CSS** with styling, and rendered dynamically via **Jinja** templates.

### Key Features Implemented
- **Bulk Data Import Guard:** Added logic to check if the database already has records, ensuring the server starts instantly instead of reloading 95k rows on every debug restart.
- **Interactive Search:** A dynamic search bar on the home page processes `POST` requests to query specific cities and return tailored weather records.
- **Integrated Visualizations:** A dedicated dashboard page that routes and displays the Matplotlib analytical charts generated in previous phases.
- **Error Handling:** Graceful fallbacks for empty search queries and "Method Not Allowed" route safeguards.
- **Modified `main.py` file :** Modified the plot function to save the files into `static/img` folder.

### How to Run the Application
1. Install all dependencies: `pip install -r requirements.txt`
2. Run the application: `python app.py`
3. Open web browser and navigate to `http://127.0.0.1:5001/`

## Module 8 - Phase 8 (PySpark Migration / Cluster Deployment)
In this phase, the project was migrated from pandas-based processing to **PySpark** to demonstrate running the analysis on a Spark (cluster-style) environment. The goal was to keep the computations distributed in Spark and only bring small results to the driver when necessary (for plotting).

### Environment
- Ran using a PySpark session (local Spark / virtual cluster setup).
- Verified Spark execution with `df.printSchema()` and `df.show()`.

### Key Changes Made for PySpark
- **Data loading:** `pd.read_csv(...)` was replaced with `spark.read.csv(..., header=True, inferSchema=True)`.
- **Data processing:** pandas-style operations were rewritten using Spark transformations:
  - Column creation using `withColumn(...)`
  - Filtering using `filter(...)`
  - Aggregations using `groupBy(...).agg(...)`
- **Cluster considerations:** avoided converting the full Spark DataFrame to Python/pandas (no full `.toPandas()` or large `.collect()`).
- **Plotting approach:** Spark does the heavy aggregation first, then only small outputs are converted to pandas for matplotlib.

### Features Implemented (Spark Versions)
- `spark_derived(df)`: adds derived columns (temp_range, humidity_change, is_rainy)
- `spark_filter_hot_days(df, threshold)`: filters hot days using Spark
- `spark_total_rainfall(df)`: computes total rainfall using Spark aggregation
- `spark_top_locations_by_avg_max_temp(df, top_n)`: top locations by avg max temperature
- `spark_make_plots(df)`: generates 3 charts and saves PNGs to a `plots/` folder

### Charts Created
1. **Bar chart:** Top 10 locations by average MaxTemp (shows hottest regions by average)
2. **Histogram:** Rainfall distribution (shows how rainfall values are distributed)
3. **Scatter plot:** MaxTemp vs Humidity3pm (shows relationship between temperature and humidity)


## Module 7 - Phase 7
In this phase, asyncronous programming was used to improve running time and allow the program to run parallely using AsyncIO in data analysis tools.

### Main Additions
- `module_06.py` was renamed with `modules_06_07.py` since the program was modified to run AsyncIO functions created in the file.
- The following functions were modified with asyncIO and added:
    - `filter_hot_days(df, threshold=35)`
    - `total_rainfall(df)`
    - `top_locations_by_avg_max_temp(df, top_n=10)`
    - `make_plots(df, out_dir="plots")`
- `main.py` had some modifications in order to allow asyncIO functions to run, including the await in all functions called, created with batch. 

## Module 6 - Phase 6
In this phase, several tools and patterns of python were introduced and explained, including data analysis and visualization tools like pandas, matplotlib or seaborn, which were used to create a data analysis and some visualizations of the dataset used in this project.

### Main Additions
- `module_06.py` was created for storing functions of data analysis, including the following:
    - `prepare_weather_df`: 
        - Clean data and ensures the data is setup correctly.
    - `add_derived`
        - Adds extra colums that will help with the analysis.
    - `filter_hot_days`
        - Filters the hottest days in all the dataser.
    - `total_rainfall`
        - Provides the total rainfall of the dataset.
    - `top_locations_by_avg_max_temp`
        - Returns a list with the top locations by averages of each city
    - `make_plots`
        - Makes 3 charts (bar, histogram, scatter) and saves them as PNG files.
        Returns a list of the saved file paths.
        
## Module 5 - Phase 5
In this Phase, multiple testing frameworks for testing were introduced, pytest is used in this phase to test for `Window_trends` generator.

### Main Additions
- `pytest` was installed using pip.
- `module_04_test.py` is created to test `Window_trends` generator using the following functions:
    - `test_window_trends()`: Used to test the correct generation of windows
    - `test_higher_window_than_DFsize()`: Used to test the case when the window number is higher than the DF size.

## Module 4 - Phase 4
In this phase, iteration tools were introduced to support more efficient and structured processing of the weather dataset. Module 4 adds custom iterators, a generator for chunking data, and a basic logging configuration to support debugging and monitoring.

### Main Additions
- ` iterate_and_print_df(df) `
Iterates through a DataFrame and prints each row as a Weather_record object (from Module 3). This demonstrates iterating through tabular data and converting raw rows into meaningful objects.
- `AU_dataFrame_Iter` (Iterator Class)
Implements the iterator protocol `(__iter__, __next__)` to iterate row-by-row through a DataFrame using `.iloc.` This provides a controlled way to traverse data without using for index, row in `df.iterrows()` directly.
- `Window_trends` (Sliding Window Iterator)
Iterates through the DataFrame using a sliding window of size `window_size`. Each iteration returns a window (subset DataFrame), which can be used for trend analysis, rolling averages, or detecting patterns across consecutive records.
- `weather_chunks(df, chunk_size)` (Generator)
A generator function that yields chunks of the DataFrame without creating a full list of chunked frames in memory. This supports scalable processing and is useful when working with large datasets.

- `load_logging_config()`
Configures Python’s logging system using `logging.basicConfig().` This enables consistent logging output across modules and supports debugging without relying only on `print()` statements.

## Module 3 - Phase 3
In this phase OOP was introduced and two new classes were added.

### First Task
New Classes Weather_record & City were added in module_03.py file with it's own Representation.

- Weather_record: Represents a single meteorological observation from the dataset, encapsulating daily metrics like temperature, rainfall, and thermal sensation status.
- City: Representation of a specific location, used to for weather data and track humidity for that city.

### Second Task
The module was imported into the main file and 4 new objects were created from those classes:
- max_temp_record
- min_temp_record
- city_max_temperature
- city_min_temperature

### Third Task
The Objects were correctly printed as expected.

## Module 2 - Phase 2
This Phase references Modularization, this phase is meant to give experience interacting with the Python ecosystem in a standard way.

### First Task
Write code to give descriptive statistics such as mean, median, mode, range etc.

### Second Task
Modularize the code. Build and publish a package using the procedures described in Chapter 2 of the textbook to TestPyPI.

### Third Task 
Install and use the package in the code as the installation would be in any official Python library.

## Module 1 - Phase 1

This module is the introduction of Python Software Develpment. 

### First Task

Create the environment for the Pythonista Culture, installing and implementing [Github Copilot](https://github.com/features/copilot) to implelemnt LLM tools to assist with our code.


### Second Task
Test the project and the IDE by creating a simple function 'def print_hi' and call that function in the `if __name__ == '__main__':` conditional statement.

### Third Task
Download a Dataset, add it to our project folder, open it and also allow writting into the dataset if needed. The dataset was downloaded from [Kaggle - Australian Weather](https://www.kaggle.com/datasets/arunavakrchakraborty/australia-weather-data).

One functions was created for open the CSV file and convert it into DataFrame using the pandas library.
## Installations
```python
pip install pandas
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install australian_weather
pip install pytest 
```
## Imports

```python
import pandas as pd
```

## Author
Created for David Ariza, Computational Data Science, UVU.
Course: CS-3270.

Cmd+Shift+V to preview Markdown in VS Code.
