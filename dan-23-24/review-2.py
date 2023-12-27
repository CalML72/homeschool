# Import everything --------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
# END-------------------------------------------------------------------------------------


# CSV and VALUES ---------------------------------------------------------------------------
# import csv and set values 
df = pd.read_csv('report-card.csv')
# Set values
date_column = 'Date'
percentages_column = 'Score %'
subject_column = 'Subject'
# END csv and values -----------------------------------------------------------------------


# DATETIME ---------------------------------------------------------------------------------
# going down to 1 month increments 
df[date_column] = pd.to_datetime(df[date_column])
df['month'] = df[date_column].dt.to_period('M')

# Sort DataFrame by 'month' and convert the month to string
df = df.sort_values('month')
df['month'] = df['month'].astype(str)
# END -------------------------------------------------------------------------------------



# PERCENTAGE FORMATTING ------------------------------------------------------------------
# Convert the percentages column to numeric (remove '%' sign if present)
df[percentages_column] = df[percentages_column].replace('%', '', regex=True).astype(float)
# Plugging in completion grades
column_to_fill = 'Score %'
default_value = 100
df[column_to_fill] = df[column_to_fill].fillna(default_value)
# specifying to only see above 72%
df = df[df[percentages_column] > 72]
# END -------------------------------------------------------------------------------------


# AVERAGES -----------------------------------------------------------------------------------
# Setting up the average option
df_grouped = df.groupby(['month', 'Subject'], as_index=False)['Score %'].mean()

# styles and charts
sns.set_style(style='whitegrid')

# create charts
plt.figure(figsize=(10, 8))
sns.pointplot(x='month', y='Score %', data=df_grouped, hue='Subject')
plt.xticks(rotation=45)
# Set the y-axis limit to start at 0%
plt.ylim(0, df_grouped['Score %'].max() + 10)
plt.show()


# ~~~~~~~~~~~~~~~ SUBPLOTS - GRID -for each "Subject" ~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up a grid layout for subplots
subjects = df_grouped['Subject'].unique()
num_subjects = len(subjects)

# Adjust the number of rows and columns based on your preferences
num_rows = int(np.ceil(num_subjects / 2))  # 2 columns per row
num_cols = 2

fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(12, 6 * num_rows))
plt.subplots_adjust(hspace=0.5)  # Adjust vertical spacing between subplots

for i, subject in enumerate(subjects):
    row = i // num_cols
    col = i % num_cols
    ax = axes[row, col]
    
    # Filter data for the current subject
    subject_data = df[df['Subject'] == subject]
    
    # Group by 'month' and calculate the mean
    df_subject_grouped = subject_data.groupby(['month'], as_index=False)['Score %'].mean()
    
    # Convert the 'month' column to string for plotting
    df_subject_grouped['month'] = df_subject_grouped['month'].astype(str)
    
    # Create the barplot for the current subject with adjusted width
    sns.barplot(x='month', y='Score %', data=df_subject_grouped, ax=ax, palette='viridis')
    ax.set_title(f'Average Grades - {subject}')
    ax.set_xlabel('Month')
    ax.set_ylabel('Score %')
    ax.tick_params(axis='x', rotation=45)

# Hide empty subplots if the number of subjects is not a multiple of num_cols*num_rows
for i in range(num_subjects, num_rows * num_cols):
    fig.delaxes(axes.flatten()[i])

plt.show()
# END AVERAGES -----------------------------------------------------------------------------------------
