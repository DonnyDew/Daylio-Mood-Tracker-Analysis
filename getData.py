import pandas as pd

# Define the mood score mappings
mood_score_map = {'rad': 5, 'almost Rad': 4.5, 'good': 4, 'Solid': 3, 'okay': 2, 'meh': 1, 'bad': 0}

# Read the CSV file into a pandas dataframe
df = pd.read_csv('daylio_export_2023_12_01.csv')

# Convert the full_date column to a datetime format
df['full_date'] = pd.to_datetime(df['full_date'], format='%Y-%m-%d')
# Extract the date and weekday from the full_date column
df['date'] = df['full_date'].dt.strftime('%Y-%m-%d')
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['weekday'] = df['full_date'].dt.strftime('%A')

# Map the mood values to their corresponding mood scores
df['moodscore'] = df['mood'].map(mood_score_map)
df['MonthYear'] = df['full_date'].dt.strftime('%b%y')
# Select only the relevant columns
df = df[['full_date','date', 'weekday', 'mood', 'activities', 'note', 'moodscore','MonthYear']]



