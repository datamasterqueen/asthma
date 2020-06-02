#Assignment 1 Preparing Data for Analysis

## Getting access to the Asthma Dataset

#The project is based on a de-identified dataset projected from Epic on patients with asthma based upon an IRB from Dr. Christopher Chute.  
#The dataset encompasses 60k patients with over 110M data elements encompassing encounters, medications, labs, procedures, symptoms,and vital measurements.  
#The data only includes categorical fields (hence no narrative notes).  
#To compile relevant Jupyter notebook that access this database tutorials you will need to be granted access to the PMAP database with this data. 

## 1. Examine the dataset

#In the beginning this course, you'll be analyzing a small flat table derived from the Asthma dataset. 
#The Asthma dataset contains ~60,000 patients seen as either outpatient or inpatient encounters seen between 2016-2018
#and having a diagnosis of Asthma recorded on the problem list or as an encounter diagnosis.  
#The dates of their visits have been obfuscated as part of the de-identification process.

#Before beginning your analysis, it's important that you familiarize yourself with the dataset. In this exercise, 
#you'll read the dataset into pandas, examine the data, and then count the number of missing values.

### Instructions
#- Import pandas using the alias pd.
#- Read the file asthma.csv into a DataFrame named df.
#- Display the first 5 rows of the Data.

#Solutions
# Import the pandas library as pd
import pandas as pd
# read 'asthma_original.csv' into a dataframe as df
df = pd.read_csv('asthma_original.csv')
df.head()

## 2. Exploring the data

#The `.shape` and `.columns` attributes let you see the shape of the DataFrame and obtain a list of its columns. 
#The `.info()` method provides important information about a DataFrame, such as the number of rows, number of columns, 
#number of non-missing values in each column, and the data type stored in each column. 

### Instructions
#- Print the shape of df and its columns. Note: `.shape` and `.columns` are attributes, not methods, so you don't need to follow these with parentheses ().
#- Print the `.info()` of the df

#Solutions
# Print the shape of df
df.shape
# Print the columns of df
df.columns
# Print the info of df
df.info()

## 2. Dropping columns

#If a DataFrame contains columns that are not useful to your analysis, such columns should be dropped from the DataFrame, 
#to make it easier for you to focus on the remaining columns.

### Instructions
#- Examine the DataFrame's `.shape` to find out the number of rows and columns.
#- Drop 'Unnamed: 0' and 'race' and columns by passing the column names to the `.drop()` method as a list of strings.
#- Examine the `.shape` again to verify that there are now two fewer columns.

#Solutions
# Examine the shape of the DataFrame
df.shape
# drop the columns
df.drop(['Unnamed: 0','race'], axis='columns', inplace=True)
# Examine the shape of the DataFrame (again)
df.shape


## 3. Dropping rows

#When you know that a specific column will be critical to your analysis, and only a small fraction of rows are missing 
#a value in that column, it often makes sense to remove those rows from the dataset.

#During this course, the weight and height column will be critical to many of your analyses. 
#Because only a small fraction of rows are missing, we'll drop those rows from the dataset.

### Instructions
#- Count the number of missing values in each column.
#- Drop all rows that are missing weight or hieght by passing the column name to the subset parameter of `.dropna()`.
#- Count the number of missing values in each column again, to verify that none of the remaining rows are missing weight or height.
#- Examine the DataFrame's `.shape` to see how many rows and columns remain.

#Solutions
# count the number of missing values in each column 
df.isnull().sum()
# Drop all rows that are missing weight or height
df.dropna(subset=['weight','height'], inplace=True)
df.shape

## 4. Checking data types

#Explore the DataFrame to determine which column's data type should be changed.

### Instructions
#- Check the current data type of `df`.
#- Convert hosp_num to an integer

#Solutions
#check the data type of 'df'
df.dtypes
# change the office_visits and num_hospitalizations columns data type to int
df.office_visits = df['office_visits'].astype(int)

## 5. Save the DataFrame to a csv file

#Now that you have cleaned your dataframe lets save it back into a cleaned excel file.
#Congratulations, you have explored the data and cleaned it.  Now let's go to the next assignment to perform some analysis.

### Instructions
#- set the index of the dataframe to the first column (index)
#- rename the index  to PatientID
#- save the `df` data frame into a file named `asthma_cleaned.csv`

df.dtypes
df.set_index('index', inplace = True)
df.index.names = ['PatientID']
df.to_csv('asthma_cleaned.csv')
df.head()

## 6. Calculating the hospitalization rate

### Instructions
#- Check the data type of `is_hosp` to confirm that it's a Boolean Series.
#- Calculate the hospitalization rate by counting the Series values and expressing them as proportions.
#- Calculate the hospitalization rate by taking the mean of the Series. (It should match the proportion of True values calculated above.)

#Solutions
# Check the data type of 'hospitalized'
df.is_hosp.dtypes
# Calculate the search rate by counting the values
(df.is_hosp==1).sum()/df.is_hosp.count()
# Calculate the search rate by taking the mean
df.is_hosp.mean()

## 7. Filtering by multiple conditions
#You'll create two DataFrames of patients who were hospitalized: one containing females and the other containing males.

### Instructions
#- Create a DataFrame, female_and_hospitalized, that only includes female who were hospitalized.
#- Create a DataFrame, male_and_hospitalized, that only includes male who were hospitalized.

#Solutions
female_and_hospitalized = df.loc[(df['gender'] == 'Female') & (df['is_hosp'] == 1)]
female_and_hospitalized.head()

male_and_hospitalized = df.loc[(df['gender'] == 'Male') & (df['is_hosp'] == 1)]
male_and_hospitalized.head()

## 8. Comparing hospitaliztion rates by gender

#You'll compare the rates at which female and male patients are hospitalized. 
#Remember that the hospitalization rate for all patients is about 2.96%.

#First, you'll filter the DataFrame by gender and calculate the hospitalization rate for each gender separately. 
#Then, you'll perform the same calculation for both genders at once using a .groupby()

### Instructions
#- Filter the DataFrame to only include female patients, and then calculate the hospitalization rate by taking the mean of `is_hosp`.
#- Filter the DataFrame to only include male patients, and then repeat the calculation.
#- Group by gender to calculate the hospitalization rate for both groups simultaneously. (It should match the previous results.)

#Solutions
# Calculate the hospitalization rate for female
df.loc[(df['gender'] == 'Female')].is_hosp.mean()
# Calculate the hospitalization rate for male
df.loc[(df['gender'] == 'Male')].is_hosp.mean()
# Calculate the search rate for both groups simultaneously
df.groupby('gender').is_hosp.agg('mean')

## 9. Adding a second factor to the analysis

#ICS(inhaled corticosteriods), OCS(oral corticosteriods) and SABA(short-acting beta2 agonists)
#are medications that are usually prescribed for patients who experience Asthma exacerbation.

#The hospitalization rate for females is much higher than for males, it's possible that the difference is mostly due to a second factor.
# You might hypothesize that the hospitalization rates varies by certain medication being prescribed or not. 
# You can test this hypothesis by examining the hospitalization rate for each combination of gender and violation.

### Instructions
#- Use a `groupby()` to calculate the hospitalization for each combination of gender and medication. 
# Is the hospitialization rate always higher for females than males?

#Solutions
# Calculate hospitalization by ocs and gender
df.groupby(['ocs', 'gender']).is_hosp.mean()
# Calculate hospitalization by ics and gender
df.groupby(['ics', 'gender']).is_hosp.mean()
# Calculate hospitalization by saba and gender
df.groupby(['saba', 'gender']).is_hosp.mean()



