import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

def draw_line_plot():
    # Draw line plot
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(20, 7))
    
    ax.plot(df.index, df_line['value'], color='red', linewidth=1)
    
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    highlighted_dates = ['2016-07', '2017-01', '2017-07', '2018-01', 
                         '2018-07', '2019-01', '2019-07', '2020-01']
    
    x_positions = pd.to_datetime(highlighted_dates)

    valid_dates = x_positions[x_positions.isin(df_line.index)]

    ax.set_xticks(valid_dates)
    ax.set_xticklabels(valid_dates.strftime('%Y-%m'))

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Draw bar plot
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name() 

    avg_page_views = df_bar.groupby([df_bar.index.year, df_bar.index.month])['value'].mean().unstack()
    fig, ax = plt.subplots(figsize=(12, 6))
    avg_page_views.plot(kind='bar', ax=ax)


    ax.set_title('Average Daily Page Views per Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    ax.set_xticklabels(avg_page_views.index, rotation=90)

    month_labels = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December']
    ax.legend(title='Months', labels=month_labels)


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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=ax2, 
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 
                       'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 
                       'Nov', 'Dec'])
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
