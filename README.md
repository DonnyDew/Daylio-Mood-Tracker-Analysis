# Daylio Mood Tracker Analysis
This project analyzes export data from the app Daylio and provides various visualizations and insights about the user's mood and activities. The project is divided into three files: `getData`, `getFeatures`, and `Display`.

## Daylio Setup
This project is set up for how I enter data into my Daylio app. I record one entry every day and choose from the moods: bad, meh, okay, solid, good, almost Rad, and rad. Some of these moods are not in the default settings of Daylio.

## getData
`getData` is a Python script that loads the Daylio data into a pandas DataFrame. The dataset contains information about the user's mood and activities for each day. The script uses the `pandas` library to read the data from a CSV file and preprocess it by converting the date column to a datetime object and setting it as the index. The resulting DataFrame is returned to be used in the analysis. 

## getFeatures
`getFeatures` is a Python script that provides functions to compute various features and insights from the mood tracker dataset. Some of the functions include:

* `getMonthlyScores()`: computes the monthly average mood score for each month for each year in the dataset.
* `plot_yearly_moodscores(year)`: plots a bar chart of the user's mood scores for each month of a given year.
* `plot_weekday_moodscores(df, year)`: plots a bar chart of the user's mood scores for each day of the week for a given year.
* `plot_moodscore_histograms(df, start_date, end_date)`: plots histograms of the user's mood scores for each day of the week given a date range.
* `plot_good_bad_piechart(df, start_date, end_date)`: plots a pie chart of the percentage of days with a good or bad mood score for a given date range.
* `best_worst_n_day_streak(df, start_date, end_date, n, mode)`: computes the best or worst n-day streak of mood scores for a given date range.
* `activity_table(df, start_date, end_date)`: computes a table of the user's most frequent activities and their impact on mood for a given date range.
* `keyword_percentage(df, start_date, end_date, keyword)`: computes the percentage of days that include a given keyword in the notes field for a given date range.
* `plot_yearly_calendar_heatmap(df, year)`: plots a heatmap calendar of the user's mood scores for each day of a given year.
* `plot_monthly_calendar_heatmap(df, year, month)`: plots a heatmap calendar of the user's mood scores for each day of a given month and year.

## Display
`Display` is a Python script that creates a Streamlit web application to visualize the features and insights computed in `getFeatures`. The web application includes various interactive widgets such as date pickers, sliders, and text inputs to allow the user to explore the data and insights. Some of the visualizations in the web application include:

* Monthly mood scores
* Yearly mood scores
* Weekday mood scores
* Mood score histograms
* Good/bad mood pie chart
* Best/worst n-day streak
* Activity table
* Note search
* Heatmap calendar
The web application is built using the streamlit library, which makes it easy to create interactive data apps using Python.

## How to use
To use the project, follow these steps:

1. Install the required libraries by running pip install -r requirements.txt in your command line.
2. Download the mood tracker dataset in CSV format and save it in the same directory as the three Python files.
3. Run app.py using the command streamlit run app.py in your command line.
4. Use the interactive widgets to explore the data and insights.

## Other Tools Used
* ChatGPT