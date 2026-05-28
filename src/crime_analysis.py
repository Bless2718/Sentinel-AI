import pandas as pd

# Load dataset
df = pd.read_excel('data/Train.xlsx')

# Display first 5 rows
print(df.head())

# Show number of rows and columns
print("Shape of dataset:", df.shape)

# Show column names
print("\nColumns:")
print(df.columns)

# Show data types
print("\nData Types:")
print(df.dtypes)
print("\nMissing Values:")
print(df.isnull().sum())
# Remove duplicate rows
df = df.drop_duplicates()

print("\nShape after removing duplicates:")
print(df.shape)
# Convert Date column into datetime format
df['Date'] = pd.to_datetime(df['Date'])

print("\nDate conversion successful")
# Day name (Monday, Tuesday, etc.)
df['Weekday'] = df['Date'].dt.day_name()

# Weekend indicator
df['Is_Weekend'] = df['Weekday'].isin(['Saturday', 'Sunday'])

print(df[['Date', 'Weekday', 'Is_Weekend']].head())
import matplotlib.pyplot as plt

# Count crimes by month
monthly_crime = df['MONTH'].value_counts().sort_index()

# Create chart
monthly_crime.plot(kind='bar')

plt.title('Crime Count by Month')
plt.xlabel('Month')
plt.ylabel('Number of Crimes')
plt.savefig('figures/monthly_crime.png')
plt.show()
hourly_crime = df['HOUR'].value_counts().sort_index()

hourly_crime.plot(kind='bar')

plt.title('Crime Count by Hour')
plt.xlabel('Hour')
plt.ylabel('Number of Crimes')
plt.savefig('figures/hourly_crime.png')
plt.show()
top_crimes = df['TYPE'].value_counts().head(10)

top_crimes.plot(kind='bar')

plt.title('Top 10 Crime Types')
plt.xlabel('Crime Type')
plt.ylabel('Count')
plt.savefig('figures/top_crimes.png')
plt.show()
top_areas = df['NEIGHBOURHOOD'].value_counts().head(10)

top_areas.plot(kind='bar')

plt.title('Top 10 Dangerous Neighborhoods')
plt.xlabel('Neighborhood')
plt.ylabel('Crime Count')
plt.savefig('figures/top_areas.png')
plt.show()
df.to_csv('data/cleaned_crime_data.csv', index=False)

print("Cleaned dataset saved successfully")

# Replace missing neighborhood names
df['NEIGHBOURHOOD'] = df['NEIGHBOURHOOD'].fillna('Unknown')

print(df['NEIGHBOURHOOD'].isnull().sum())

# Fill missing HOUR values
df['HOUR'] = df['HOUR'].fillna(df['HOUR'].median())

# Fill missing MINUTE values
df['MINUTE'] = df['MINUTE'].fillna(df['MINUTE'].median())

print(df[['HOUR', 'MINUTE']].isnull().sum())

df['HOUR'] = df['HOUR'].astype(int)
df['MINUTE'] = df['MINUTE'].astype(int)

print(df.dtypes)

def get_time_period(hour):
    if 5 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 17:
        return 'Afternoon'
    elif 17 <= hour < 21:
        return 'Evening'
    else:
        return 'Night'

df['Time_Period'] = df['HOUR'].apply(get_time_period)

print(df[['HOUR', 'Time_Period']].head())

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

yearly_crime = df['YEAR'].value_counts().sort_index()

yearly_crime.plot(kind='line', marker='o')

plt.title('Crime Trend by Year')
plt.xlabel('Year')
plt.ylabel('Number of Crimes')

plt.savefig('figures/yearly_crime_trend.png')

plt.show()

plt.figure(figsize=(12,6))

hourly_crime = df['HOUR'].value_counts().sort_index()

hourly_crime.plot(kind='bar')

plt.title('Crime Count by Hour')
plt.xlabel('Hour')
plt.ylabel('Number of Crimes')

plt.savefig('figures/hourly_crime.png')

plt.show()

plt.figure(figsize=(12,6))

top_crimes = df['TYPE'].value_counts().head(10)

top_crimes.plot(kind='bar')

plt.title('Top 10 Crime Types')
plt.xlabel('Crime Type')
plt.ylabel('Count')

plt.xticks(rotation=45)

plt.savefig('figures/top_crimes.png')

plt.show()

plt.figure(figsize=(12,6))

dangerous_areas = df['NEIGHBOURHOOD'].value_counts().head(10)

dangerous_areas.plot(kind='bar')

plt.title('Top 10 Dangerous Neighborhoods')
plt.xlabel('Neighborhood')
plt.ylabel('Crime Count')

plt.xticks(rotation=45)

plt.savefig('figures/dangerous_neighborhoods.png')

plt.show()

import seaborn as sns

plt.figure(figsize=(10,6))

numeric_df = df[['HOUR', 'MINUTE', 'YEAR', 'MONTH', 'DAY', 'Latitude', 'Longitude']]

sns.heatmap(numeric_df.corr(), annot=True)

plt.title('Correlation Heatmap')

plt.savefig('figures/correlation_heatmap.png')

plt.show()

# Convert month number to month name
month_names = {
    1:'January', 2:'February', 3:'March', 4:'April',
    5:'May', 6:'June', 7:'July', 8:'August',
    9:'September', 10:'October', 11:'November', 12:'December'
}

df['Month_Name'] = df['MONTH'].map(month_names)
df.to_csv('data/final_cleaned_crime_data.csv', index=False)

print('Final cleaned dataset saved successfully')