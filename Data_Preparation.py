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

df.shape
df.columns
df.info()


