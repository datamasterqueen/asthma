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


# Step 4 Number of exacerbations 

## Instructions

#- create a new integer column in `df_med` called `exacer` for the number of exacerbations
#- assign the field to 1 if the pharmaceutical_class is equal to GLUCOCORTICOIDS
#- create a new dataframe `df_ocs` including the `osler_id` and `exacer` columns from `df_med`
#- and grouping by `osler_id` summing the exacerbations for each patient
#- reset the index for `df_ocs` so `osler_id` is a column and not the index 
#- bring `df_ocs` into `df` by using pd.merge 
#- `left` join `df_ocs` with `df` so that the `df_ocs` columns come after the `df` columns
#- becasuse we did a left join there may be patients without any medications that result in a null for exacer
#- replace null values for exacer with 0
#- create a new field `exacer_lvl` which bins the number of exacerbations into 4 groups (0,1-2,3-4,5+)
#- bins=[-np.inf,0,2,4,np.inf]

df_med['exacer'] = 0
df_med.loc[df_med['pharmaceutical_class']=='GLUCOCORTICOIDS','exacer'] = 1
df_ocs = df_med.loc[:,['osler_id','exacer']]
df_ocs = df_ocs.groupby('osler_id').exacer.sum().sort_values(ascending=False)
df_ocs = df_ocs.to_frame().reset_index()
df = pd.merge(df , df_ocs, on='osler_id', how='left')
df=df.fillna({'exacer':0})
df = df.astype({'exacer':'int64'})
df['exacer_lvl']= pd.cut(df.exacer, [-np.inf,0,2,4,np.inf], \
                        labels=["0","1-2","3-4","5+"])
df.exacer_lvl.value_counts()

#Verify
list(df.columns)==['osler_id', 'date_of_birth', 'gender', 'race', 'ethnicity', 'age',
       'age_cat', 'ocs','ics','saba','exacer', 'exacer_lvl'] #True
df.exacer.max()==46 #True
df.exacer.isnull().sum()==0 #True
df.exacer.sum()==13292 #True
df.exacer_lvl.value_counts()==[53611,5901,696,468] #True


# Step 5. Number of Hospitalizations related to Asthma

## Instructions

#- We want to find all the hospital encounters where the symptoms for those encounters include the following reasons
#- load all encounters with a hospital encounter
#- load all symptoms with the included ICD10 codes
#- join the tables (Use SQL or Pandas for the previous steps)
#- group by patient and count the number of unique encounters
#- create a column on `df` called `hosp_num` with the number of hospitalizations (Null values should zero)
#- create a column on `df` called `is_hosp` as a True/False for hospitalization

#| ICD 10 code | definition |
#|--|--|
#| J45.51 ||
#| J45.52 ||
#| J45.901 ||

query="SELECT * FROM encounters where encounter_type IN ('Hospital Encounter') "
df_enc = pd.read_sql_query(query, engine)
df_enc.head(1)

query="SELECT * FROM symptoms where diagnosis_code_icd10 IN ('J45.51','J45.52','J45.901')"
df_sym = pd.read_sql_query(query, engine)
df_sym.head(1)

df_encsym = pd.merge(df_enc , df_sym, on='encounter_id', how='inner')

srs_hosp = df_encsym.groupby('osler_id_x').encounter_id.nunique()

srs_hosp

df_encsym2 = df_encsym.groupby('osler_id_x').encounter_id.nunique()

df_encsym2 = df_encsym2.to_frame().reset_index()

df_encsym2 = df_encsym2.rename(columns={"osler_id_x":"osler_id","encounter_id":"hosp_num"})

df_encsym2.head(1)

df = pd.merge(df , df_encsym2, on='osler_id', how='left')

df.head(1)

df=df.fillna({'hosp_num':0})

df = df.astype({'hosp_num':'int64'})

mask = df['hosp_num'] > 0

df['is_hosp'] = 0

df.loc[mask, 'is_hosp'] = 1

df.head(1)

#Verify
len(srs_hosp)==976 #True
srs_hosp.max()==15 #True
df.isnull().sum().sum()==0 #True
df.hosp_num.sum()==1421 #True
round(df.is_hosp.mean(),3)==0.016 #True


# Step 6: Height, weight and bmi

#Greenblatt- 
#BMI. Body Mass Index (BMI) was calculated using an average of height and weight measurements, after eliminating values that fell outside 5% of the patient’s median height measurement and 10% of the patient’s median weight measurement. 
#BMI was classified into 5 categories: not overweight or obese (<25.0 kg/m2), overweight (25.0 to <30.0 kg/m2), class 1 obese (30.0 to <35.0 kg/m2), class 2 obese (35.0 to <40.0 kg/m2) and class 3 obese (>40.0 kg/m2). 

## Instructions
#- load vitals_weight into a dataframe `df_weight`
#- load vitals_height into a dataframe `df_height`
#- Calculate for each patient the average height after filtering out the top and bottom 5%
#- Calculate for each patient the average weight after filtering out the top and bottom 10%
#- Create a column in `df` called `height` for the patients height in meters (0.0254 m/inch)
#- Create a column in `df` called `weight` for the patients weight in kilograms
#- Create a column in `df` called `bmi` for the weight divided by the square of the height
#- Create a column in `df` called `bmi_cat` for the categories of BMI
#- Use `bins=[-np.inf,25,30,35,40,np.inf]`

#| BMI Cat | Description |
#|--|--|
#| not overweight or obese | (<25.0 kg/m2)|
#| overweight | (25.0 to <30.0 kg/m2)|
#| class 1 obese | (30.0 to <35.0 kg/m2)| 
#| class 2 obese |(35.0 to <40.0 kg/m2) |
#| class 3 obese | (>40.0 kg/m2)|

#- use this function to calculate the average height and weight

def filtered_avg(series,quant):
    lower_quant=np.quantile(series,quant/100)
    upper_quant=np.quantile(series,1-quant/100)
    return series[(series>lower_quant)&(series<upper_quant)].mean()
  
#Height
query="SELECT * FROM vitals_height"
df_height = pd.read_sql_query(query, engine)

df_height.height = pd.to_numeric(df_height.height)

srs_height = df_height.groupby('osler_id')\
.height.apply(filtered_avg, quant=5)

df.set_index('osler_id', inplace=True)

df['height']= srs_height*0.0254

df.head(1)

#Weight
query="SELECT * FROM vitals_weight"
df_weight = pd.read_sql_query(query, engine)
df_weight.weight = pd.to_numeric(df_weight.weight)
srs_weight = df_weight.groupby('osler_id')\
.weight.apply(filtered_avg, quant=10)
df['weight']= srs_weight
df.head(1)
df.reset_index(inplace=True)

#BMI
df['bmi']=df['weight']/(df['height']**2)
df.bmi.mean()
df['bmi_cat']= pd.cut(df.bmi, [-np.inf,25,30,35,40,np.inf], \
                      labels=["1. not overweight or obese","2. overweight","3. class 1 obese","4. class 2 obese","5. class 3 obese"])
(df.bmi_cat=='2. overweight').sum()

#Verify
round(df.height.max(),2)==2.08 #True
round(df.weight.median(),2)==74.32 #True
round(df.height.median(),2)==1.58 #True
round(df.weight.mean(),2)==73.27 #True
round(df.bmi.mean(),2)==25.54 #True
(df.bmi_cat=='2. overweight').sum()==2638 #True

# Step 7: Co-morbidities 
#- install the hcuppy library using `!pip install hcuppy`
#- Algorithm for elix codes
#- group problem list by osler id
#- send series of icd10 codes to custom function
#- convert to ta list of elixhauser terms
#- add the list of terms to a column in pats
#- get a list of all the terms
#- add columns in pats for each term
#- fill in columns with boolean

!pip install hcuppy

import json
from hcuppy.elixhauser import ElixhauserEngine
ee=ElixhauserEngine()

query = "select * from problemlist"
df_prob=pd.read_sql_query(query, engine)
df_prob=df_prob[df_prob.osler_id.isin(df.osler_id)]

def get_dx_list(dx_series):
    output=[]
    results=ee.get_elixhauser(dx_series.tolist())
    if len(results['cmrbdt_lst'])>0:
        output=results['cmrbdt_lst']
    return output

srs_prob=df_prob.groupby('osler_id')\
.diagnosis_code_icd10.apply(get_dx_list)

df_prob = srs_prob.to_frame().reset_index()
df_prob = df_prob.rename(columns={"diagnosis_code_icd10":"elix"})
df_prob.elix.explode()
set(df_prob.elix.explode())

for elix_name in set(df_prob.elix.explode()):
    df_prob[elix_name]=False
    
df_prob=df_prob.loc[:,'osler_id':'elix']
df_prob.head(1)

df = pd.merge(df , df_prob, on='osler_id', how='left')

for elix_name in set(df.elix.explode()):
    if elix_name=='NaN':
        df[elix_name.str.lower]=False
 
for elix_name in set(df.elix.explode()):
    if str(elix_name)!='nan':
        df["el_{}".format(elix_name.lower())]=False
        
from datetime import datetime
stime=datetime.now()

for i,row in df.iterrows():
    if str(row.elix)!='nan':
        for name in row.elix:
            df.loc[i,"el_{}".format(name.lower())]=True
            
print("Time to complete operation = {} seconds".\
      format((datetime.now()-stime).total_seconds()))

#Verify
df.shape[1]==49 #True
df[df.columns[df.columns.str.contains('el_')]].sum().sum()==130758 #True

# Step 8. add special diagnosis codes for

#- Create boolean fields to state the presence of each of the conditions below
#- use the global problem list to look for these conditions

#| Diagnosis | ICD 10 Code |
#| --- | --- |
#| chronic_bronchitis |J41.0-J41.8 |
#| sinusitis |J32.0 - J32.9 |
#| copd | J44.1-.9| 
#| emphysema | J43-J43.9 |
#| acute_bronchitis |J20 -J20.9 |
#| cystic_fibrosis |E84 - E84.9 |


