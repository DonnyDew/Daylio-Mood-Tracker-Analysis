import streamlit as st
import pandas as pd
from getData import df
from getFeatures import *

st.set_page_config(layout="wide")

# Title
st.title("Mood Tracker Analysis")

# Date input
start_date = st.date_input("Start Date", value =pd.to_datetime("2020-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("today"))

monthly_scores = getMonthlyScores()
st.subheader("Monthly Mood Scores")
st.dataframe(monthly_scores)

# Plot yearly mood scores
st.subheader("Yearly Mood Scores")
year = st.selectbox("Select Year", options=sorted(df['date'].dt.year.unique(), reverse=True), index=0)
fig,yearly_avg_moodscore = plot_yearly_moodscores(year)
st.plotly_chart(fig)
st.write(f"The avg mood for {year} is {round(yearly_avg_moodscore, 2)}")

# Plot weekday mood scores
st.subheader("Weekday Mood Scores")
weekday_chart = plot_weekday_moodscores(df, year)
st.altair_chart(weekday_chart, use_container_width=True)

# Plot moodscore histograms
st.subheader("Mood Score Histograms")
histograms = plot_moodscore_histograms(df, start_date, end_date)
st.altair_chart(histograms, use_container_width=True)

# Plot good/bad mood pie chart
st.subheader("Good/Bad Mood Pie Chart")
pie_chart = plot_good_bad_piechart(df, start_date, end_date)
st.altair_chart(pie_chart, use_container_width=True)

# Best/Worst n-day streak
st.subheader("Best/Worst N-Day Streak")
n = st.number_input("Number of Days (N)", min_value=1, max_value=365, value=7)
best_streaks = best_worst_n_day_streak(df, start_date, end_date, n, mode='best')
worst_streaks = best_worst_n_day_streak(df, start_date, end_date, n, mode='worst')

st.write("Best Streaks:")
for i, streak in enumerate(best_streaks):
    st.write(f"{i+1}. {streak[2]} - {streak[1]} with average score of {streak[0]}")

st.write("Worst Streaks:")
for i, streak in enumerate(worst_streaks):
    st.write(f"{i+1}. {streak[2]} - {streak[1]} with average score of {streak[0]}")

# Activity table
st.subheader("Activity Table")
activity_data = activity_table(df, start_date, end_date)
activity_df = pd.DataFrame(activity_data, columns=["Activity", "Frequency", "Impact (%)"])
st.write(activity_df)

# Note Search
st.subheader("Note Search")
keyword = st.text_input('Enter a keyword')
result = keyword_percentage(df, start_date, end_date, keyword)
st.write(f'The percentage of days that include the keyword "{keyword}" between {start_date} and {end_date} is {result}%.')


# HeatMap Calendar
st.subheader('Daylio Mood Calendar')
year = st.slider('Select a Year:', 2019, 2023, 2021)
year_plot_hm = plot_yearly_calendar_heatmap(df,year=year)
st.plotly_chart(year_plot_hm, use_container_width=True)
month = st.selectbox('Select a Month:', ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], index=0)
month_plot_hm = plot_monthly_calendar_heatmap(df,year=year,month=month)
st.plotly_chart(month_plot_hm, use_container_width=True)





