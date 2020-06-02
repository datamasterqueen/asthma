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

