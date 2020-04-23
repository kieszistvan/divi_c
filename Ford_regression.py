import pandas as pd
import numpy as np
import sys
import os
import csv
from sklearn.linear_model import LinearRegression
import seaborn
import plotly
import matplotlib.pyplot as plt
import math
from datetime import datetime as dt

# Function to dynamically get the layoutsize of the subplots
def plot_size_finder(N):
    subplot_size = math.floor(math.sqrt(N))
    subplot_size = math.sqrt(N) if subplot_size**2==N else subplot_size+1
    return subplot_size

ford_data = pd.read_excel('test_V2.xlsx', header=0)
ford_data['Date'] = pd.to_datetime(ford_data['Date']).apply(lambda x: dt.strftime(x, "%b-%d"))
Quarters = ford_data.Q.unique()
# Define subplot size based on quarters in the data
layout_size = int(plot_size_finder(len(Quarters)))

# Reshape dataframe to have all prices besides each other - quarter becoming column name
ford_by_quarter = pd.DataFrame()
for q in Quarters:
    ford_by_quarter = pd.concat([ford_by_quarter, ford_data.loc[(ford_data.Q == q), 'Price'].reset_index(drop=True)], axis=1)
ford_by_quarter.columns=Quarters

# Define max and min values for all dates available - to be used for sizing the plot labels
max_price = ford_by_quarter.max().max()
min_price = ford_by_quarter.min().min()

# Create new column to support the bar chart whereby we indicate the time of dividend in the plot
# Set to historical max in order to be able show it as one bar across the plot
ford_data['Div_Date_indicator'] = ford_data['Amount'].apply(lambda x: 0 if pd.isna(x) else max_price)
# ford_by_quarter.plot(subplots=True, layout=(2,2))
# Define style and colorpalette of the plots
plt.style.use('seaborn-darkgrid')
palette = plt.get_cmap('Set1')
plt.figure(figsize=(10,10))
num = 0  # counter for the plots
for column in ford_by_quarter:
    num += 1
    # Find the right spot on the plot
    plt.subplot(layout_size, layout_size, num)
    # Plot the lineplot and the barplot
    plt.plot(ford_data.loc[(ford_data.Q == column), 'Date'], ford_by_quarter[column], marker='', color=palette(num), linewidth=1.9, alpha=0.9, label=column)
    plt.bar(ford_data.loc[(ford_data.Q == column), 'Date'],ford_data.loc[(ford_data.Q == column), 'Div_Date_indicator'], color=palette(num), alpha=0.9, label=False, width=0.3)
    # Set Limits
    plt.ylim(min_price, max_price)
    plt.tick_params(axis='x', which='major', labelsize=8, labelrotation=45)  # Change rotation and size for readibility

    # Remove Y axis ticks if subplot it not on the left side
    y_label_parameter = list(range(1, layout_size ** 2, layout_size))
    if num not in y_label_parameter:
        plt.tick_params(labelleft=False)
    # Add  subplot title
    plt.title(column, loc='left', fontsize=11, fontweight=0, color=palette(num))
# Add general title of the object
plt.suptitle("Ford Share price around dividend dates", fontsize=13, fontweight=0, color='black',
             style='italic')
plt.subplots_adjust(wspace=0.1, hspace=0.5) # Adjust distance between subplots
plt.show()

print('End of Plotting')