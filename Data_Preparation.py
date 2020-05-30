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

#Import the pandas library as pd
import pandas as pd

#read 'asthma_original.csv' into a dataframe as df
df = pd.read_csv('asthma_original.csv')

df.head()

## 2. Exploring the data

#The `.shape` and `.columns` attributes let you see the shape of the DataFrame and obtain a list of its columns. 
#The `.info()` method provides important information about a DataFrame, such as the number of rows, number of columns, 
#number of non-missing values in each column, and the data type stored in each column. 

### Instructions

#- Print the shape of df and its columns. Note: `.shape` and `.columns` are attributes, not methods, so you don't need to follow these with parentheses ().
#- Print the `.info()` of the df

#Print the shape of df
print(df.shape)
#Print the columns of df
print(df.columns)
#Print the info of df
print(df.info())

## 2. Dropping columns

#If a DataFrame contains columns that are not useful to your analysis, such columns should be dropped from the DataFrame, 
#to make it easier for you to focus on the remaining columns.

### Instructions

#- Examine the DataFrame's `.shape` to find out the number of rows and columns.
#- Drop 'Unnamed: 0' and 'race' and columns by passing the column names to the `.drop()` method as a list of strings.
#- Examine the `.shape` again to verify that there are now two fewer columns.


#Examine the shape of the DataFrame
print(df.shape)

#drop the columns
df.drop(['Unnamed: 0','race'], axis='columns', inplace=True)

#Examine the shape of the DataFrame (again)
print(df.shape)


## 3. Dropping rows

#When you know that a specific column will be critical to your analysis, and only a small fraction of rows are missing 
#a value in that column, it often makes sense to remove those rows from the dataset.

#During this course, the weight and height column will be critical to many of your analyses. 
#Because only a small fraction of rows are missing, we'll drop those rows from the dataset.

## 3. Dropping rows

#When you know that a specific column will be critical to your analysis, and only a small fraction of rows are missing a value
#in that column, it often makes sense to remove those rows from the dataset.

#During this course, the weight and height column will be critical to many of your analyses. 
#Because only a small fraction of rows are missing, we'll drop those rows from the dataset.

### Instructions

#- Count the number of missing values in each column.
#- Drop all rows that are missing weight or hieght by passing the column name to the subset parameter of `.dropna()`.
#- Count the number of missing values in each column again, to verify that none of the remaining rows are missing weight or height.
#- Examine the DataFrame's `.shape` to see how many rows and columns remain.

#count the number of missing values in each column 
print(df.isnull().sum())

# Drop all rows that are missing weight or height
df.dropna(subset=['weight','height'], inplace=True)

df.shape

## 4. Checking data types

#Explore the DataFrame to determine which column's data type should be changed.

### Instructions

#- Check the current data type of `df`.
#- Convert hosp_num to an integer
