#Assignment 1 Preparing Data for Analysis

## Getting access to the Asthma Dataset

#Tutorials are based on a de-identified dataset projected from Epic on patients with asthma based upon an IRB from Dr. Christopher Chute.  
#The dataset encompasses 60k patients with over 110M data elements encompassing encounters, medications, labs, procedures, symptoms,and vital measurements.  
#The data only includes categorical fields (hence no narrative notes).  
#To compile relevant Jupyter notebook that access this database tutorials you will need to be granted access to the PMAP database with this data. 

#You will need this direct database access for future assignments.


#Getting Access to the Asthma Dataset

#Import the pandas library as pd
import pandas as pd

#read 'asthma_original.csv' into a dataframe as df
df = pd.read_csv('asthma_original.csv')

df.head()

