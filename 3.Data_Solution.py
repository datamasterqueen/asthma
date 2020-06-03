# Assignment 3

## eCGM  Appropriate Medications for Asthma

#Ref. https://cmit.cms.gov/CMIT_public/ViewMeasure?MeasureId=5780

#CMS Measure Inventory Tool:  Use of Appropriate Medications for Asthma (eCQM)

#Percentage of patients 5-64 years of age who were identified as having
#persistent asthma and were appropriately ordered medication during the
#measurement period

#| Property | Definition |
#|--|--|
#|Numerator| Patients who were ordered at least one prescription for a preferred therapy during the measurement period|
#|Denominator| Patients 5-64 years of age with persistent asthma and a visit during the measurement period|
#|Denom Exclustions| Patients with a diagnosis of emphysema, COPD, obstructive chronic bronchitis, cystic fibrosis or acute respiratory failure that overlaps the measurement period|

#Rationale

#Asthma is one of the most prevalent chronic diseases, becoming increasingly
#more commonplace over the past twenty years. Approximately 24.6 million
#Americans have asthma, and it is responsible for over 3,000 deaths in the U.S.
#annually (American Lung Association 2010). In 2006, 13.3 million clinical visits
#(hospital, outpatient, emergency department, and physician offices) were
#attributed to asthma (Centers for Disease Control and Prevention 2009). The
#incidence rate, and subsequently the number of asthma-related health visits, is
#expected to increase by an additional 100 million globally by 2025 (World
#Health Organization 2007).

#Asthma accounts for over 20 billion spent on health care in the United States.
#Direct costs, including prescriptions, make up 15.6 billion of that total. Indirect
#costs, such as lost productivity, add an additional 5.1 billion (Centers for
#Disease Control and Prevention 2009). Inpatient hospitalization accounts for over 50 percent of overall asthma-related costs (Bahadori et al. 2009). In
#addition to the direct financial burden, asthma is also a leading cause of
#absenteeism and productivity, accounting for an estimated 14.2 million missed
#workdays for adults and over 14 million missed school days for children
#(Akinbami et al. 2009). Studies have shown that the indirect costs of asthma
#are becoming a growing financial burden on patients, and resulting in
#significant additional costs (Bahadori et al. 2009).

#Appropriate medication management could potentially prevent a significant
#proportion of asthma-related costs (hospitalizations, emergency room visits
#and missed work and school days) (Akinbami et al. 2009). The Asthma
#Regional Council supported this inference, stating that proper management
#could potentially save at least 25 percent of total asthma costs, or 5 billion,
#nationally by reducing health care costs (American Lung Association 2009).
#Another initiative, the Children's Health Fund's Childhood Asthma Initiative, examined patients enrolled in an asthma 
#intervention program. Results illustrated that treatment that aligned with clinical guidelines reduced the severity of symptoms 
#experienced, as well as asthma-related events (eg, hospitalizations, emergency room visits, etc.) (Columbia University 2010). 
#Additionally, subsequent savings attributed to improved clinical outcomes totaled to nearly 4.2 million or 4,525 per patient. 
#This translated to a significant reduction in federally subsidized and private insurance-based costs for this population (Columbia University 2010).

# Step 1. Load Libraries and Create an encrypted authentication token
## Instructions
#- load the pandas library and assign it to an alias of `pd`
#- load the numpy library and assign it the alias of `np`
#- import the getpass library
#- import the Authentication module from the SciServer library
#- import myUserName from the SciServer getKeystoneUseerWithToken function
#- use getpass to store your password as an encrypted variable `passwd`
#- assign your username to the variable `user` and add an `win\\` prefix

## Solutions

import pandas as pd
import numpy as np
import getpass
from SciServer import Authentication

myUserName = Authentication.getKeystoneUserWithToken(Authentication.getToken()).userName
passwd = getpass.getpass('Password for ' + myUserName + ': ')
user = "win\\" + myUserName

# Step 2. Connect to the PMAP Database

## Instructions
- import the sqlalchemy library
- import the urllib.parse library
- set the host_ip = `ESMPMDBPR4.WIN.AD.JHU.EDU`
- set the database name = `CAMP_PMCoe_Projection`
- set the database port to `1433`
- set the driver to `FreeTDS`
- set the tds_ver= to `8.0
- add the username and password from previous step
- call sqlalchemy to create a database connection variable called `engine`


