# Final Assignment

## Clinical researchers are requesting clinical records analyzing the factors associated with exacerbations.  

#- They would like to replicate a recently published paper from U Penn that published their methodology
#-https://asthmarp.biomedcentral.com/articles/10.1186/s40733-019-0048-y

## Specification
#They would like a 'flat' csv file of 

#- all the patients in the CAMP database
#- one patient per row
#- all the measurements per patient in columns

#|field| definition|
#|--|--|
#|gender| patient gender |
#|race | patient race |
#|age | patient age in years |
#|age_cat| patient age binned in decades|
#|ocs | whether the patient had an OCS prescription|
#|ics| whether the patient had an ICS prescription|
#|saba | whether the patient had an SABA prescription|
#|exacer| number of exacerbations |
#|exacer_lvl | binned exacerbations by 0,1-2,2-3,4-5,5+|
#|hosp_num| number of hospital visits due to Asthma exacerbation |
#|is_hosp| whether they were hospitalized |
#|height| patient height |
#|weight| patient weight |
#|bmi| patient body mass index |
#|bmi_cat| bmi in class categories |
#|el_pulmcirc| does the patient have PULMCIRC comorbidity |
#|el_renlfail| does the patient have RENLFAIL comorbidity |
#|el_coag| does the patient have COAG comorbidity |
#|el_arth| does the patient have ARTH comorbidity |
#|el_dm| does the patient have DM comorbidity |
#|el_tumor| does the patient have TUMOR comorbidity |
#|el_drug| does the patient have DRUG comorbidity |
#|el_perivasc| does the patient have PERIVASC comorbidity |
#|el_hypothy| does the patient have HYPOTHY comorbidity |
#|el_neuro| does the patient have NEURO comorbidity |
#|el_aids| does the patient have AIDS comorbidity |
#|el_valve| does the patient have VALVE comorbidity |
#|el_wghtloss| does the patient have WGHTLOSS comorbidity |
#|el_ulcer| does the patient have ULCER comorbidity |
#|el_anemdef| does the patient have ANEMDEF comorbidity |
#|el_dmcx| does the patient have DMCX comorbidity |
#|el_htncx| does the patient have HTNCX comorbidity |
#|el_chf| does the patient have CHF comorbidity |
#|el_lymph| does the patient have LYMPH comorbidity |
#|el_psych| does the patient have PSYCH comorbidity |
#|el_para| does the patient have PARA comorbidity |
#|el_htn| does the patient have HTN comorbidity |
#|el_obese| does the patient have OBESE comorbidity |
#|el_alcohol| does the patient have ALCOHOL comorbidity |
#|el_lytes| does the patient have LYTES comorbidity |
#|el_liver| does the patient have LIVER comorbidity |
#|el_bldloss| does the patient have BLDLOSS comorbidity |
#|el_depress| does the patient have DEPRESS comorbidity |
#|el_mets| does the patient have METS comorbidity |
#|el_chrnlung| does the patient have CHRNLUNG comorbidity |
#|chronic bronchitis| does the patient have a diagnosis for Chronic Bronicitis   |
#|sinusitis| does the patient have a diagnosis for Sinusitis |
#|copd| does the patient have a diagnosis for copd  |
#|emphysema| does the patient have a diagnosis for Emphysema    |
#|acute_bronchitist| does the patient have a diagnosis for Acute Bronchitis  |
#|cystic_fibrosis| does the patient have a diagnosis for Cystic Fibrosis  |
#|duration| duration in days between earliest and latest encounter|

# Import Libraries & connect to DB

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns

import getpass
from SciServer import Authentication

myUserName = Authentication.getKeystoneUserWithToken(Authentication.getToken()).userName
passwd = getpass.getpass('Password for ' + myUserName + ': ')
user = "win\\" + myUserName

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
.format(driver, host_ip, db_port, db, user, passwd, tds_ver))
# Create Engine
engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect=' +
urllib.parse.quote(conn_str))

# Step 1. Create a dataframe for Patients Table

## Instructions
#- create a dataframe `df` of all the records in the `patients` table

query="SELECT * FROM patients"
df = pd.read_sql_query(query, engine)

len(df)==60676


# Step 2. Calculate age and age category

#The data spans 3 years. Ages for the same patient will vary. 
#You consulted with the researchers and they would like you measure it from a arbitrary time from date of birth.  
#Subtract the date of birth from the year 2018 since that is the latest date of the data.

## Instructions

#- create a new column to the df dataframe `age` 
#- subtract the year of the date of birth from the year 2018 to get float
#- create a new column `age_cat` into the following groups
#- <18,18-30,31-40,41-50,51-60,61-70,71-80,81-90,91-100,100+
#- using bins=[-np.inf,18,30,40,50,60,70,80,90,100,np.inf]

df['age']=2018-df.date_of_birth.dt.year
df['age_cat']= pd.cut(df.age, [-np.inf,18,30,40,50,60,70,80,90,100,np.inf], \
                        labels=["<18","18-30","31-40","41-50","51-60","61-70","71-80","81-90","91-100","100+"])
df.age.head()
df.age_cat.value_counts()

#Verify
df.age.head()==[5,3,41,48,16]
round(df.age.mean(),2)==37.07
df.age_cat.value_counts()==[17651,9135,7857,7326,7057,6529,3673,1237,209,2]

# Step 3. Medications check

## Instructions 

#- create a dataframe `df_med` of the meds database
#- create `pts_ocs`,`pts_ics`,`pts_saba` with lists of patient_ids if they take the medication using pharmaceutical_class matching

#|medication| string match|
#|--|--|
#|OCS|GLUCOCORTICOIDS|
#|ICS|r'CORT.+INH'|
#|SABA|r'BETA.+INH.+SHORT'|

#- create new columns for df `ocs`,`ics`,`saba`
#- make the columns True if the patient is taking the respective medication

query="SELECT * FROM meds"
df_med = pd.read_sql_query(query, engine)

meds_ocs = df_med[df_med.loc[:,'pharmaceutical_class']=='GLUCOCORTICOIDS']
meds_ics = df_med[df_med.loc[:,'pharmaceutical_class'].str.contains(r'CORT.+INH', regex=True)]
meds_saba = df_med[df_med.loc[:,'pharmaceutical_class'].str.contains(r'BETA.+INH.+SHORT', regex=True)]

pts_ocs = meds_ocs.osler_id.unique()
pts_ics = meds_ics.osler_id.unique()
pts_saba = meds_saba.osler_id.unique()

df['ocs'] = 0
df['ics'] = 0 
df['saba'] = 0

mask_ocs=df.osler_id.isin(pts_ocs)
mask_ics=df.osler_id.isin(pts_ics)
mask_saba=df.osler_id.isin(pts_saba)

df.loc[mask_ocs,'ocs']=1
df.loc[mask_ics,'ics']=1
df.loc[mask_saba,'saba']=1

#Verify
df[['ocs','ics','saba']].sum()==[7065,16475,26951]




