from getData import df
import plotly.graph_objs as go
import pandas as pd
import altair as alt
import numpy as np

def getMonthlyScores():
    # Group by month and year and calculate mean moodscore
    monthly_avg = df.groupby('MonthYear')['moodscore'].mean()
    
    # Create a new dataframe with MonthYear and average_moodscore columns
    monthlymoodscore = pd.DataFrame({'MonthYear': monthly_avg.index, 'average_moodscore': monthly_avg.values})

    # Convert MonthYear to datetime format
    monthlymoodscore['MonthYear'] = pd.to_datetime(monthlymoodscore['MonthYear'], format='%b%y')

    # Sort the dataframe by MonthYear in chronological order
    monthlymoodscore = monthlymoodscore.sort_values('MonthYear')

    # Round the average_moodscore column to 2 decimal places
    monthlymoodscore['average_moodscore'] = monthlymoodscore['average_moodscore'].round(2)

    # Convert MonthYear back to string format
    monthlymoodscore['MonthYear'] = monthlymoodscore['MonthYear'].dt.strftime('%b%y')
    return monthlymoodscore

monthlymoodscore = getMonthlyScores()

def plot_yearly_moodscores(year):
    # Filter the monthly moodscores for the given year
    year_mask = monthlymoodscore['MonthYear'].str.endswith(str(year)[-2:])
    year_moodscores = monthlymoodscore[year_mask]
    yearly_avg_moodscore = year_moodscores['average_moodscore'].mean()
    
    # Create a Plotly bar chart
    fig = go.Figure(data=[go.Bar(
        x=year_moodscores['MonthYear'],
        y=year_moodscores['average_moodscore'],
        text=year_moodscores['average_moodscore'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Average Mood Score: %{y:.2f}',
        marker=dict(
            color=year_moodscores['average_moodscore'],
            colorscale='RdYlGn',
            showscale=True,
            cmax=5,
            cmin=0
        )
    )])
    # Update chart layout for a more professional look
    fig.update_layout(
        title=f"Monthly Mood Scores for {year}",
        xaxis_title="Month",
        yaxis_title="Average Mood Score",
        font=dict(
            family="Arial",
            size=14,
            color="#333333"
        ),
        plot_bgcolor='#FFFFFF',
        xaxis=dict(
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            tickfont=dict(size=12),
            range=[0, 5],
            tickmode='array',
            tickvals=[0, 1, 2, 3, 4, 5],
            ticktext=['bad', 'meh', 'okay', 'Solid', 'good', 'rad']
        ),
        margin=dict(
            l=60,
            r=60,
            t=80,
            b=60
        )
    )
    return fig,yearly_avg_moodscore

def plot_weekday_moodscores(df, year=None):
    # Filter the dataframe for the given year
    if year:
        year_mask = df['date'].dt.year == year
        year_data = df[year_mask]
    else:
        year_data = df
    
    # Group the data by day of the week and calculate the mean mood score
    weekday_moodscores = year_data.groupby('weekday')['moodscore'].mean().reset_index()
    
    # Find the day with the highest mood score
    max_day = weekday_moodscores.loc[weekday_moodscores['moodscore'].idxmax(), 'weekday']
    
    # Set the order of the weekdays for plotting
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_moodscores['weekday'] = pd.Categorical(weekday_moodscores['weekday'], categories=weekdays, ordered=True)
    weekday_moodscores = weekday_moodscores.sort_values('weekday')
    
    # Generate the bar chart using Altair
    chart = alt.Chart(weekday_moodscores).mark_bar(width=40).encode(
        x=alt.X('weekday', title='Day of the Week', sort=weekdays),
        y=alt.Y('moodscore', title='Average Mood Score', scale=alt.Scale(domain=(0, 5))),
        tooltip=['weekday', 'moodscore']
    )

    # Add a different color for the day with the highest mood score
    chart = chart.encode(
        color=alt.condition(
            alt.datum.weekday == max_day,
            alt.value('orange'),
            alt.value('steelblue')
        )
    )

    if year:
        chart = chart.properties(title=f'Average Mood Scores by Day of the Week in {year}')
    else:
        chart = chart.properties(title='Average Mood Scores by Day of the Week lifetime')

    return chart

def plot_moodscore_histograms(df, start_date, finish_date):
    # Convert start_date and finish_date to pd.Timestamp objects
    start_date = pd.Timestamp(start_date)
    finish_date = pd.Timestamp(finish_date)
    
    # Define the mapping of mood scores to colors
    color_map = {
        'bad': '#808080',
        'meh': '#01319d',
        'okay': '#4f0080',
        'Solid': '#00FF00',
        'good': '#008000',
        'almost Rad': '#feba29',
        'rad': '#ff6201'
    }

    # Set up the subplots
    charts = []

    # Loop through each day of the week and create a histogram
    for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
        # Filter the data for the current day of the week and the given date range
        day_mask = df['weekday'] == day
        date_mask = (df['date'] >= start_date) & (df['date'] <= finish_date)
        day_data = df[day_mask & date_mask]

        # Create the histogram using Altair
        chart = alt.Chart(day_data).mark_bar().encode(
            alt.X('moodscore:Q', bin=alt.Bin(maxbins=10), title='Mood Score'),
            alt.Y('count()', title='Frequency'),
            alt.Color('mood:N', scale=alt.Scale(domain=['bad', 'meh', 'okay', 'Solid', 'good', 'almost Rad', 'rad'],
                                                 range=[color_map['bad'], color_map['meh'], color_map['okay'], color_map['Solid'], color_map['good'], color_map['almost Rad'], color_map['rad']])),
            tooltip=['moodscore', 'count()']
        ).properties(title=day, width=100)

        charts.append(chart)

    # Combine the histograms into a single chart
    combined_chart = alt.hconcat(*charts)

    return combined_chart


def plot_good_bad_piechart(df, start_date, finish_date):
    # Convert start_date and finish_date to pd.Timestamp objects
    start_date = pd.Timestamp(start_date)
    finish_date = pd.Timestamp(finish_date)

    good_moods = ['rad', 'almost Rad', 'Solid']
    bad_moods = ['meh', 'bad']
    ok_moods = ['okay']

    date_mask = (df['date'] >= start_date) & (df['date'] <= finish_date)
    date_data = df[date_mask]

    mood_counts = date_data['mood'].value_counts()
    mood_counts = mood_counts.reindex(good_moods + bad_moods + ok_moods, fill_value=0)
    good_count = mood_counts[good_moods].sum()
    bad_count = mood_counts[bad_moods].sum()
    ok_count = mood_counts[ok_moods].sum()

    data = pd.DataFrame({
        'category': ['Positive', 'Negative', 'Ok'],
        'count': [good_count, bad_count, ok_count]
    })

    chart = alt.Chart(data).mark_arc(innerRadius=0).encode(
        alt.Theta('count:Q', stack=True),
        alt.Color('category:N', scale=alt.Scale(scheme='category10'))
    ).properties(
        width=300,
        height=200
    )

    return chart

def best_worst_n_day_streak(df, start_date, end_date, n, mode='best'):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    scores = []
    for i in range(len(df_filtered) - n + 1):
        cur_score = df_filtered.iloc[i:i+n]['moodscore'].sum() / n
        initial_date = df_filtered.iloc[i]['date'].strftime('%m/%d/%y')
        final_date = df_filtered.iloc[i+n-1]['date'].strftime('%m/%d/%y')
        scores.append((round(cur_score, 2), initial_date, final_date))
    
    scores.sort(reverse=True if mode == 'best' else False)
    return scores[:5]

def activity_table(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    activity_dict = {}
    overall_avg_mood = df_filtered['moodscore'].mean()

    for _, row in df_filtered.iterrows():
        activities = row['activities'].split(' | ')
        mood = row['moodscore']

        for activity in activities:
            if activity not in activity_dict:
                activity_dict[activity] = {'count': 0, 'total_mood': 0}
            
            activity_dict[activity]['count'] += 1
            activity_dict[activity]['total_mood'] += mood
    
    activity_table_data = []
    for activity, data in activity_dict.items():
        frequency = data['count']
        avg_mood = data['total_mood'] / frequency
        impact = ((avg_mood - overall_avg_mood) / overall_avg_mood) * 100
        activity_table_data.append((activity, frequency, round(impact, 2)))

    activity_table_data.sort(key=lambda x: x[1], reverse=True)

    return activity_table_data

def plot_yearly_calendar_heatmap(df, year=None):
    # Filter the dataframe for the given year
    if year:
        year_mask = df['date'].dt.year == year
        df = df[year_mask]

    # Group the data by date and calculate the mean mood score
    daily_moodscores = df.groupby('date')['moodscore'].mean().reset_index()

    # Create a new dataframe with a column for the month and day
    dates = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    calendar_data = pd.DataFrame({'date': dates})
    calendar_data['month'] = calendar_data['date'].dt.month
    calendar_data['day'] = calendar_data['date'].dt.day
    
    # Merge the mean mood score with the calendar data
    calendar_data = pd.merge(calendar_data, daily_moodscores, on='date', how='left')
    
    # Replace missing mood scores with 0
    calendar_data['moodscore'] = calendar_data['moodscore'].fillna(0)

    # Create a Pivot table for the monthly average mood scores
    monthly_moodscores = pd.pivot_table(
        calendar_data,
        values='moodscore',
        index='month',
        aggfunc=np.mean
    ).reset_index()

    # Create a Plotly calendar heatmap
    fig = go.Figure(go.Heatmap(
        x=calendar_data['month'],
        y=calendar_data['day'],
        z=calendar_data['moodscore'],
        colorscale='RdYlGn',
        zmin=0,
        zmax=5,
        hovertemplate='<b>%{x|%B}</b><br>Average Mood Score: %{z:.2f}'
    ))

    # Add monthly average mood scores to the heatmap
    fig.add_trace(go.Scatter(
        x=monthly_moodscores['month'],
        y=[31] * 12,
        mode='markers+text',
        marker=dict(color='white', size=0),
        text=monthly_moodscores['moodscore'].round(2),
        textfont=dict(size=12),
        textposition='middle center',
        hoverinfo='none'
    ))

    # Update chart layout for a more professional look
    fig.update_layout(
        title=f"Yearly Mood Scores{' for ' + str(year) if year else ''}",
        font=dict(
            family="Arial",
            size=14,
            color="#333333"
        ),
        plot_bgcolor='#FFFFFF',
        xaxis=dict(
            tickfont=dict(size=12),
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ),
        yaxis=dict(
            tickfont=dict(size=12),
            nticks=31,
            fixedrange=True
        ),
        margin=dict(
            l=60,
            r=60,
            t=80,
            b=60
        )
    )

    return fig

def plot_monthly_calendar_heatmap(df, year=None, month=None):
    # Filter the dataframe for the given year
    if year:
        year_mask = df['date'].dt.year == year
        df = df[year_mask]

    # Filter the dataframe for the given month
    if month:
        month_dict = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12
        }
        month_num = month_dict[month.capitalize()]
        month_mask = (df['date'].dt.month == month_num) & (df['date'].dt.year == year)
        df = df[month_mask]
        df = df.dropna(subset=['date'])

    # Group the data by date and calculate the mean mood score
    daily_moodscores = df.groupby('date')['moodscore'].mean().reset_index()

    # Create a new dataframe with a column for the day of the month
    dates = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    calendar_data = pd.DataFrame({'date': dates})
    calendar_data['day'] = calendar_data['date'].dt.day

    # Merge the mean mood score with the calendar data
    calendar_data = pd.merge(calendar_data, daily_moodscores, on='date', how='left')

    # Replace missing mood scores with 0
    calendar_data['moodscore'] = calendar_data['moodscore'].fillna(0)

    # Create a Plotly calendar heatmap
    fig = go.Figure(go.Heatmap(
        x=calendar_data['date'],
        y=calendar_data['day'],
        z=calendar_data['moodscore'],
        colorscale='RdYlGn',
        zmin=0,
        zmax=5,
        hovertemplate='%{x|%d %B %Y}<br>Average Mood Score: %{z:.2f}'
    ))

    # Update chart layout for a more professional look
    fig.update_layout(
        title=f"Monthly Mood Scores for {month.capitalize()} {year}",
        font=dict(
            family="Arial",
            size=14,
            color="#333333"
        ),
        plot_bgcolor='#FFFFFF',
        xaxis=dict(
            tickfont=dict(size=12),
            dtick='D1',
            tickformat='%d'
        ),
        yaxis=dict(
            tickfont=dict(size=12),
            nticks=31,
            fixedrange=True
        ),
        margin=dict(
            l=60,
            r=60,
            t=80,
            b=60
        )
    )

    return fig

def keyword_percentage(df, start_date, end_date, keyword):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    total_days = len(df_filtered)
    keyword_days = 0

    for _, row in df_filtered.iterrows():
        note = row['note']
        if keyword.lower() in note.lower():
            keyword_days += 1

    percentage = (keyword_days / total_days) * 100
    return round(percentage, 2)