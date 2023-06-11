import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'])

df = df.set_index('date')

# Clean data
# filtering out days when the value were in the top 2.5% of the dataset or bottom 2.5% of the dataset
df = df[(df['value'] <= df['value'].quantile(0.975))
        & (df['value'] >= df['value'].quantile(0.025))]


def draw_line_plot():
  # Draw line plot
  fig, ax = plt.subplots()

  ax.plot(df.index, df['value'], color='red')

  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')
  ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

  fig.set_size_inches(20, 6)
  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  # show average daily page views for each month grouped by year
  df_bar = df.copy()
  df_bar['year'] = df_bar.index.year
  df_bar['month'] = df_bar.index.month_name()
  df_bar = df_bar.groupby(['year', 'month'])['value'].mean()
  df_bar = df_bar.reset_index()

  # Order by months
  months = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ]

  df_bar['month'] = pd.Categorical(df_bar['month'],
                                   categories=months,
                                   ordered=True)

  # Draw bar plot
  fig, ax = plt.subplots(figsize=(12, 6))

  sns.barplot(x='year', y='value', hue='month', data=df_bar)

  plt.xlabel('Years')
  plt.ylabel('Average Page Views')
  plt.legend(title='Months', loc=2)

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]

  # Draw box plots (using Seaborn)
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

  sns.boxplot(data=df_box, ax=ax1, x='year', y='value')
  ax1.set_title('Year-wise Box Plot (Trend)')
  ax1.set_xlabel('Year')
  ax1.set_ylabel('Page Views')

  months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
    'Nov', 'Dec'
  ]
  sns.boxplot(data=df_box, ax=ax2, x='month', y='value', order=months)
  ax2.set_title('Month-wise Box Plot (Seasonality)')
  ax2.set_xlabel('Month')
  ax2.set_ylabel('Page Views')

  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
