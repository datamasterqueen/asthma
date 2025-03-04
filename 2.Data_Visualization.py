# Step 1. Load Libraries and Create an encrypted authentication token
## Instructions
#- load the pandas library and assign it to an alias of `pd`
#- load the numpy library and assign it the alias of `np`
#- load the library matplotlib.pyplot and assign it the alias of `plt`
#- load the seaborn library and assign it the alias of `sns`
#- use the `%matplotlib inline` command to render graphics in the notebook
#- import the getpass library
#- import the Authentication module from the SciServer library
#- import myUserName from the SciServer getKeystoneUseerWithToken function
#- use getpass to store your password as an encrypted variable `passwd`
#- assign your username to the variable `user` and add an `win\\` prefix

## Solutions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

import getpass
from SciServer import Authentication

myUserName = Authentication.getKeystoneUserWithToken(Authentication.getToken()).userName
passwd = getpass.getpass('Password for ' + myUserName + ': ')
user = "win\\" + myUserName

## Database connection 

#The data sits on a database server that is designed to query large data sets quickly. 
#This script connects to the PMAP database server and allows access to the *CAMP_PMCoe_Projection* 
#which is the de-identified asthma dataset.  

# Step 2. Connect to the PMAP Database

## Instructions
#- import the sqlalchemy library
#- import the urllib.parse library
#- set the host_ip = `ESMPMDBPR4.WIN.AD.JHU.EDU`
#- set the database name = `CAMP_PMCoe_Projection`
#- set the database port to `1433`
#- set the driver to `FreeTDS`
#- set the tds_ver= to `8.0
#- add the username and password from previous step
#- call sqlalchemy to create a database connection variable called `engine`

import sqlalchemy
import urllib.parse
#SQL Driver
driver="FreeTDS"
tds_ver="8.0"
# Database
host_ip="ESMPMDBPR4.WIN.AD.JHU.EDU" # Update this accordingly
db_port="1433"
db="CAMP_PMCoe_Projection" # Update this accordingly
# Create Connection String
conn_str=("DRIVER={};Server={};PORT={};DATABASE={};UID={};PWD={};TDS_VERSION={}"
.format(driver, host_ip, db_port, db, user, passwd, tds_ver)
)
# Create Engine
engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect=' +
urllib.parse.quote(conn_str)
)

# Step 3. Explore weight and height data sets

### Instructions
#- Run SQL query on the `vitals_weight` table.
#- Read the query into a DataFrame named `df_weight`.
#- Display the first 5 rows of the `df_weight`.
#- Generate descriptive statistics of the `weight` column in `df_weight` using the describe() method
#- Note the data type of weight
#- convert the weight column to a float with the pd.to_numeric() method
#- Run the descriptive statistics method on the `weight` column
#- How many null values are there for weight?

#This can take 5-10 seconds as you are querying and loading 100,000s of records into your dataframe

#Solutions
query="SELECT * FROM vitals_weight"
df_weight = pd.read_sql_query(query, engine)
df_weight.head()

# Change data type to float
df_weight.weight.dtypes
df_weight.weight = pd.to_numeric(df_weight.weight,downcast='float')
df_weight.weight.dtypes
# Display descriptive statistics
df_weight.weight.describe()
# Calculate sum of null values for weight
df_weight.weight.isna().sum()

# Step 4. Explatory Data Analysis on weight 

#perform basic exploratory data analysis on weight, look for distrubution and outliers

## Instructions
#- generate a historgram of the weight column in df_weight
#- set the bins parameter to 50
#- set the log parameter to True to set the yscale to logarithmic

# Solutions
df_weight.weight.hist()
df_weight.weight.hist(bins=50)
df_weight.weight.hist(bins=50, log=True)

# Step 5. Perform a data tracer on a patient to look at the values

#A data tracer is a spot check on the data to see if has an internal consistency

## Instructions
#- Find the patient (`osler_id`) having the most  `weight` records; print his/her `osler_id` and the counts
#- Run the describe() method on that one patient's weight to see how their weight varies.

df_weight.groupby('osler_id').weight.count().sort_values().tail()
df_weight.loc[(df_weight['osler_id']=='be5dd7ae-c1f9-424d-b389-07301676474e')].weight.describe()


# Step 6. Visualize the data

## Instructions
#- For that patient
#- draw a scatter plot of all his/her weight over time, use the weight_date column
#- draw a scatter plot of the above patient's weight using the plt object
#- use `plt.xticks(rotation = 45)` to rotate the dates for a better fit
#- remember to render the graph to use a `plt.show()`

#Solutions
df_toppatlist = df_weight.loc[(df_weight['osler_id']=='be5dd7ae-c1f9-424d-b389-07301676474e')]
fig, ax=plt.subplots()
ax.scatter(df_toppatlist['weight_date'], df_toppatlist['weight'])
ax.set_xlabel("Date")
ax.set_ylabel("Weight")
plt.xticks(rotation = 45)
plt.show()

# Step 7: Load the height vitals data

## Instructions
#- Run SQL query on the `vitals_height` table.
#- Read the query into a DataFrame named `df_height`.
#- Convert the height column to a float
#- Display the first 5 rows of the Data.
#- How many null values are there for height?
#- Create a histogram of heights with log set to true and bins set to 40
#- If the average person is ~ 2 meters, what do you think the units are?

## Solutions
query="SELECT * FROM vitals_height"
df_height = pd.read_sql_query(query, engine)
# Covert height data type to float
df_height.height = pd.to_numeric(df_height.height,downcast='float')
df_height.head()

df_height.info()
# Count number of null values
df_height.height.isna().sum()
# Create a histogram
df_height.height.hist(bins=40, log=True)
df_height.height.mean()
#The units are in inches.

# Step 8. Calculate BMI

## Instructions

#- Print the shape of df_weight and df_height using 
#- String format technique "Shape for df_weight is {} and df_height is {}".format()
#- Merge `df_weight` and `df_height` into a new dataframe `df_wh`
#- Use an inner join using the `how` parameter set to `inner`
#- and the `on` parameter set to the `encounter_id` field
#- print the shape of the merged dataframe `df_wh`. 
#- How is BMI calculated? BMI is calculated the same way for both adults and children. 
#- The calculation is based on the formulas here: [Calculate BMI](https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html#Interpreted). 
#(https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html).
#- Create a new column `height_m` with the height converted to meters
#- Calculate patient's BMI at the time of each encounter, and create a new column `bmi` in `df_wh` to store the values. Remember to be consistent with measurement Units. Use either kilograms and meters (or centimeters) or pounds and inches.
#- Generate descriptive statistics of `bmi`. 

## Solutions
print("Shape for df_weight is {} and df_height is {}".format(df_weight.shape, df_height.shape))
df_wh = pd.merge(df_weight, df_height, on='encounter_id', how='inner')
df_wh.shape

df_wh['height_m']=df_wh['height']/39.37
df_wh['bmi']=df_wh['weight']/(df_wh['height_m']**2)
df_wh['bmi'].describe()

# Step 9: BMI data exploratory analysis

## Instructions

#- Create a histogram of `bmi` on the df_wh dataframe
#- Use the log set to True 
#- How many patients have a BMI greater than 100
#- Filter out bmi measurements greater than 100 
#- Recreate the histogram 

## Solutions
df_wh.bmi.hist(log=True)
df_wh[df_wh.bmi >100].osler_id_x.count()
df_wh[df_wh.bmi <100].bmi.hist(log=True)


# Step 10. Create bmi categories

## Instructions

#- create a new category on `df_wh` called `bmi_cat`
#- with the categories in the below table
#- create a horizontal bar chart with the number of measurements in each category

#| name | bmi value range |
#| --- | -- |
#|1. not overweight or obese| <= 25|
#|2. overweight|25 < x <= 30|
#|3. class 1 obese|30 < x <= 35|
#|4. class 2 obese|35 < x <= 40|
#|5. class 3 obese|40 < x|

## Solutions
# Create Categories
df_wh['bmi_cat']= pd.cut(df_wh.bmi, [-np.inf,25,30,35,40,np.inf],  \
                         labels=["1. not overweight or obese","2. overweight",
                                 "3. class 1 obese","4. class 2 obese","5. class 3 obese"])
df_wh.bmi_cat.value_counts()
# Create Bar Chart
df_wh.groupby('bmi_cat').bmi.count().plot(kind='barh')
plt.xlabel('Number of Measurements')
plt.ylabel('BMI Categories')

