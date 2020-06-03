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
