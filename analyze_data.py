# Import the pandas library as pd
import pandas as pd
import chardet
import fileinput
import csv
import requests
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')


ri = pd.read_csv('ri_statewide_2019_02_25.csv',  engine='python', error_bad_lines=False )

#print(ri.contraband_drugs.head())
#exit()
print(ri.info())

print(ri.head())

# Count the number of missing values in each column
print(ri.isnull().sum())

print(' == shape= ',ri.shape)

# Drop the 'vehicle_model' and 'state' columns
ri.drop(['vehicle_model'], axis='columns', inplace=True)

# Examine the shape of the DataFrame (again)
print(ri.shape)

# Count the number of missing values in each column
print(ri.isnull().sum())

# Drop all rows that are missing 'driver_gender'
ri.dropna(subset=['subject_sex'], inplace=True)
print(ri.shape)
# Count the number of missing values in each column (again)
print(ri.isnull().sum())
print(' ==== print data types ... ')
print(ri.dtypes)
print(' === change data types ... ')
ri['arrest_made'] = ri.arrest_made.astype(bool)
ri['search_conducted'] = ri.search_conducted.astype(bool)
ri['contraband_drugs'] = ri.contraband_drugs.astype(bool)
ri['contraband_found'] = ri.contraband_found.astype(bool)
ri.contraband_drugs.fillna(False,inplace=True)
ri.contraband_found.fillna(False,inplace=True)

print(ri.dtypes)
#=====================================================
print(' === add datetime object ... ')
# Concatenate 'stop_date' and 'stop_time' (separated by a space)
combined = ri.date.str.cat(ri.time, sep=' ')

# Convert 'combined' to datetime format
ri['stop_datetime'] = pd.to_datetime(combined)
print(ri.dtypes)
ri.set_index('stop_datetime',inplace=True)
#=====================================================
# Express the counts as proportions
print(' ==== filter data: viloation types and break down by gender ... ')
# total violatiosn break down
print(ri.reason_for_stop.value_counts(normalize=True))
# Create a DataFrame of female drivers
female = ri[ri.subject_sex == 'female']

# Create a DataFrame of male drivers
male = ri[ri.subject_sex  == 'male']
print(' ==== filter data: violations by female drivers ... ')
# Compute the violations by female drivers (as proportions)
print(female.reason_for_stop.value_counts(normalize=True))
print(' ==== filter data: violations by male drivers ... ')
# Compute the violations by male drivers (as proportions)
print(male.reason_for_stop.value_counts(normalize=True))
#=======================================================
print(' ==== Q: does driver gender affects outcome of stop? ... ')
# Create a DataFrame of female drivers stopped for speeding
female_and_speeding = ri[(ri.subject_sex == 'female') & (ri.reason_for_stop == 'Speeding')]

# Create a DataFrame of male drivers stopped for speeding
male_and_speeding = ri[(ri.subject_sex == 'male') & (ri.reason_for_stop == 'Speeding')]

# Compute the stop outcomes for female drivers (as proportions)
print(female_and_speeding.outcome.value_counts(normalize=True))

# Compute the stop outcomes for male drivers (as proportions)
print(male_and_speeding.outcome.value_counts(normalize=True))
#=======================================================
print(' ==== Q: stats on search conduction ... ')
# Check the data type of 'search_conducted'
print(ri.search_conducted.dtype)

# Calculate the search rate by counting the values
print(ri.search_conducted.value_counts(normalize=True))

print(ri.groupby('subject_sex').search_conducted.mean())

print(ri.groupby(['reason_for_stop','subject_sex']).search_conducted.mean())
#=======================================================
# Count the 'search_type' values
print(ri.reason_for_search.value_counts())

# Check if 'search_type' contains the string 'Protective Frisk'
ri['frisk'] = ri.reason_for_search.str.contains('Protective Frisk', na=False)

# Check the data type of 'frisk'
print(ri.frisk.dtype)

# Take the sum of 'frisk'
print(ri.frisk.sum())
#=======================================================
# Create a DataFrame of stops in which a search was conducted
searched = ri[ri.search_conducted == True]

# Calculate the overall frisk rate by taking the mean of 'frisk'
print(searched.frisk.mean())

# Calculate the frisk rate for each gender
print(searched.groupby('subject_sex').frisk.mean())
#===============================================
print('Calculate the overall arrest rate')
print(ri.arrest_made.mean())

# Calculate the hourly arrest rate
print(ri.groupby(ri.index.hour).arrest_made.mean())

# Save the hourly arrest rate
hourly_arrest_rate = ri.groupby(ri.index.hour).arrest_made.mean()

# Create a line plot of 'hourly_arrest_rate'
hourly_arrest_rate.plot()

# Add the xlabel, ylabel, and title
plt.xlabel('Hour')
plt.ylabel('Arrest Rate')
plt.title('Arrest Rate by Time of Day')

# Display the plot
plt.savefig('Arrest_Rate_by_Time_of_Day.png')
plt.clf()
#========================================================
# Calculate the annual rate of drug-related stops
print('Calculate the annual rate of drug-related stops')

print(ri.contraband_drugs.resample('A').mean())

# Save the annual rate of drug-related stops
annual_drug_rate = ri.contraband_drugs.resample('A').mean()

# Calculate and save the annual search rate
annual_search_rate = ri.search_conducted.resample('A').mean()

# Concatenate 'annual_drug_rate' and 'annual_search_rate'
annual = pd.concat([annual_drug_rate,annual_search_rate], axis='columns')

# Create subplots from 'annual'
annual.plot(subplots=True)

plt.xlabel('Year')
# Display the plot
plt.savefig('annual_drug_rate.png')
plt.clf()
#=============================================================
# Create a frequency table of districts and violations
print(pd.crosstab(ri.zone,ri.reason_for_stop))

# Save the frequency table as 'all_zones'
all_zones = pd.crosstab(ri.zone,ri.reason_for_stop)

# Select rows 'Zone K1' through 'Zone K3'
print(all_zones.loc['K1':'X4'])

# Save the smaller table as 'k_zones'
k_zones = all_zones.loc['K1':'X4']

# Create a bar plot of 'k_zones'
k_zones.plot(kind='bar')
plt.savefig('k_zones.png')
plt.clf()
#=============================================================
# Calculate the mean 'stop_minutes' for each value in 'violation_raw'
print(ri.groupby('outcome').zone.mean())

# Save the resulting Series as 'stop_length'
stop_length = ri.groupby('outcome').zone.mean()

# Sort 'stop_length' by its values and create a horizontal bar plot
stop_length.sort_values().plot(kind='barh')
plt.savefig('zone_dist.png')
plt.clf()
