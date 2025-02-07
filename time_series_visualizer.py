import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', 
                 parse_dates=['date'], 
                 index_col='date')

# Clean data by filtering out days in top/bottom 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], 'r', linewidth=1)
    
    # Set title and labels
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    return fig

def draw_bar_plot():
    # Copy and prepare data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')
    
    # Calculate monthly averages
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Reorder months
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    df_bar = df_bar.reindex(columns=months)
    
    # Create bar plot
    fig = df_bar.plot(kind='bar', figsize=(10, 5)).figure
    plt.legend(title='Months')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    
    # Year-wise Box Plot
    years = sorted(df_box['year'].unique())
    year_data = [df_box[df_box['year'] == year]['value'] for year in years]
    bp1 = ax1.boxplot(year_data, labels=years, whis=[0, 100], meanline=True, showmeans=False)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    
    # Month-wise Box Plot
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_data = [df_box[df_box['month'] == month]['value'] for month in month_order]
    bp2 = ax2.boxplot(month_data, labels=month_order, whis=[0, 100], meanline=True, showmeans=False)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    
    return fig
