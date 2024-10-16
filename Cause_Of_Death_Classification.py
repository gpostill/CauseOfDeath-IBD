#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 08:13:21 2023

@author: gepostill
"""

#Note - for privacy all file names are written as FILE_NAME to conceal the file path of data and figures on the laptop used to create the code


#Cause of Death 

import pandas as pd 
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from tableone import TableOne


#DEFINING FUNCTION 

    
#Cleaned Data 
df = pd.read_csv(FILE_NAME)


table_year = pd.crosstab(df['death_yr'], df['Cohort'])
#check how many with rows in the 2019 and 2020 will be removed

#Dropping records from 2019-2020
df = df[df['death_yr']!=2019]
df = df[df['death_yr']!=2020]

#ICD 10 Category
table_LCD = pd.crosstab(df['lcd'], df['Cohort'])
table_LCD_percent = pd.crosstab(df['lcd'], df['Cohort'], normalize='columns', margins=True, margins_name='Total') #Returns percentages

#Counting the number of records with missing COD: 
missing_icd = df['cod_underlying_icd10'].isna().sum()
print(f"Missing ICD: {missing_icd}")
#there are 673 patients with missing COD with DOD before 2019 

missing_lcd = df['lcd'].isna().sum()
print(f"Missing LCD: {missing_lcd}")

df = df.dropna(subset=['cod_underlying_icd10'])


#IBD-Specific causes of death 
IBD_COD = df[df['cod_underlying_icd10'].str.startswith('K5')]
IBD_COD_count = IBD_COD.groupby(['Cohort','Premature','cod_underlying_icd10']).size().reset_index(name='count')
IBD_COD_count = IBD_COD_count.pivot_table(index='cod_underlying_icd10',columns=['Cohort','Premature'], values='count', fill_value=0)


 
#COD into icd 10 categories 
df['ICD10_category'] = df['cod_underlying_icd10']

neoplasm = ['D120','D126','D136','D150','D151','D180','D219','D27','D320','D329','D331','D332','D333','D350','D352','D361','D369','D370','D372','D376','D377','D379','D381','D414','D429',
            'D430','D431','D432','D443','D45','D464','D469','D471','D472','D473','D474','D477','D479','D481','D489']

blood = ['D509','D560','D589','D591','D593','D595','D619','D643','D648','D649','D65','D684','D685','D686','D689','D690','D693','D694','D696','D70','D71','D735','D751','D752','D758',
         'D759','D761','D762','D763','D801','D839','D849','D860','D868','D869','D891','D899']
  
new_name = []
for cause in df['ICD10_category']: 
    if cause[0] == 'A': 
        cause = 'Infectious and parasitic diseases'
    elif cause[0] == 'B':
        cause = 'Infectious and parasitic diseases'
    elif cause[0] == 'C': 
        cause = 'Neoplasms'
    elif cause in neoplasm: 
        cause = 'Neoplasms'
    elif cause in blood: 
        cause = 'Diseases of the blood'
    elif cause[0] == 'E': 
        cause = 'Endocrine, nutritional, and metabolic diseases'
    elif cause[0] == 'F': 
        cause = 'Mental and behavioural disorders'
    elif cause[0] == 'G': 
        cause = 'Diseases of the nervous system'
    elif cause[0] == 'H': 
        cause ='Other causes'       # 'Diseases of the eye, adenexa, ear, and mastoid process'
    elif cause[0] == 'I': 
        cause = 'Diseases of the circulatory system'
    elif cause[0] == 'J': 
        cause =  'Diseases of the respiratory system'
    elif cause[0] == 'K':
        cause = 'Diseases of the digestive system'
    elif cause[0] == 'L': 
        cause = 'Diseases of the skin'
    elif cause[0] == 'M': 
        cause = 'Diseases of the musculoskeletal system'
    elif cause[0] == 'N': 
        cause = 'Diseases of the genitourinary system'
    elif cause[0] == 'O': 
        cause = 'Other causes'      #'Pregnancy, childbirth, and perinatal period'
    elif cause[0] == 'P': 
        cause = 'Other causes'      #'Pregnancy, childbirth, and perinatal period'
    elif cause[0] == 'Q': 
        cause = 'Other causes'      #'Congenital anomalies'
    elif cause[0] == 'R': 
        cause = 'Other causes'
    elif cause[0] == 'S': 
        cause = 'Injuies and other external causes'
    elif cause[0] == 'T': 
        cause = 'Injuies and other external causes'
    elif cause[0] == 'U': 
        cause = 'Other causes'
    elif cause[0] == 'V': 
        cause = 'Injuies and other external causes'
    elif cause[0] == 'W': 
        cause = 'Injuies and other external causes'
    elif cause[0] == 'X': 
        cause = 'Injuies and other external causes'
    elif cause[0] == 'Y': 
        cause = 'Injuies and other external causes'
    else:  
        cause = 'Other causes' 
    new_name.append(cause)
        

df['ICD10_category'] = new_name


#Categorize the digestive causes of death 
df['K_digestive_causes'] = np.nan

#Identify the unique causes in the dataset
filtered_values = df[df['cod_underlying_icd10'].str.startswith('K')]['cod_underlying_icd10']
unique_values = filtered_values.unique()

#Group categories 
#note: I have manually created these categoreis 
oral_cav = ['K047', 'K102', 'K112']
esophagus_stomach = ['K20', 'K210', 'K219', 'K220', 'K221', 'K222', 'K223', 'K224','K227', 'K229', 'K254', 'K255',
                     'K259', 'K264', 'K265', 'K266', 'K269', 'K274', 'K275', 'K279', 'K284', 'K289', 'K291', 
                     'K295', 'K297', 'K311', 'K316', 'K318', 'K319', 'K3190']
appendix = ['K350','K353','K358','K37']
hernia = ['K403','K409','K413','K419','K420','K429','K430','K432','K433','K435','K436','K439','K440','K449','K450','K460','K469']
noninfectious_collitis = ['K501','K509','K519','K520','K528','K529']
other_intestine = ['K550','K5500','K5509','K551','K552','K559','K560','K561','K562','K563','K564',
                   'K565','K566','K567','K573','K578','K579','K589','K590','K593','K598','K610','K611',
                   'K613','K623','K625','K627','K628','K630','K631','K6310','K6319', 'K632','K635', 'K639', 'K649']
peritoneum = ['K650','K658','K659','K660','K661','K668','K669']
liver = ['K700','K701', 'K703', 'K704', 'K709', 'K7200', 'K7209', 'K721', 'K729', 'K7290', 'K7299', 'K743', 
         'K745', 'K746', 'K750', 'K754','K758', 'K759', 'K760', 'K766', 'K767', 'K768', 'K769']
gallbladder = ['K800', 'K801', 'K802', 'K805', 'K810', 'K811', 'K819', 'K822','K828', 'K829', 'K830', 'K831',
               'K851', 'K852', 'K859', 'K861', 'K862', 'K863', 'K868', 'K869']
other_digestive = ["K902", "K904", "K909", "K918", "K920", "K922", "K928", "K929"]


new_cause = []
for cause in df['cod_underlying_icd10']: 
    if cause in oral_cav: 
        cause = 'Diseass of oral cavity, salivary glands and jaws'
    elif cause in esophagus_stomach: 
        cause = 'Diseases of oesophagus, stomach, and duodenum'
    elif cause in appendix: 
        cause = 'Diseases of appendix'
    elif cause in hernia: 
        cause = 'Hernia'
    elif cause in noninfectious_collitis: 
        cause = 'Noninfective enteritis and colitis'
    elif cause in other_intestine: 
        cause = 'Other diseases of intestines'
    elif cause in peritoneum: 
        cause = 'Diseases of peritoneum'
    elif cause in liver: 
        cause = 'Diseases of liver'
    elif cause in gallbladder: 
        cause = 'Disorders of gallbladder, biliary tract, and pancreas'
    elif cause in other_digestive: 
        cause = 'Other diseases of the digestive system'
    else:  
        cause = np.nan
    new_cause.append(cause)
        

df['K_digestive_causes'] = new_cause

#Export Cause of Death 
df.to_csv(FILE_NAME)



##############################

#ICD 10 Category
table_ICD10_category = pd.crosstab(df['ICD10_category'], df['Cohort'])
table_ICD10_category_percent = pd.crosstab(df['ICD10_category'], df['Cohort'], normalize='columns', margins=True, margins_name='Total') #Returns percentages

#Mapping the ICD-10 causes of death to the lcd column values
df_lcd = df[['lcd','ICD10_category']]
df_lcd['count'] = 1
df_lcd = df_lcd.pivot_table(index='lcd',columns='ICD10_category', values='count', aggfunc='sum')

#Replacing small cell values
for small in [1,2,3,4,5]: 
    df_lcd = df_lcd.replace(small, '1-5')


#Exporting to CSV
df_lcd.to_csv(FILE_NAME)


########################################
###### Cause of death descriptive ######
########################################

#Creating a function to dichotomize the numerical values into '>=40' and '<40'
def dichotomize(value):
    if value >= 40: 
        return 'Rural'
    elif value < 40: 
        return 'Urban'
    else: 
        return 'Missing'

df['rio2008'] = df['rio2008'].astype(float)
df['RIO_cat'] = df['rio2008'].apply(dichotomize)

##Create a Table 1 of Cause of Death Data
variables = ['sex','Age_death','Premature', 'RIO_cat', 'Material_deprivation','Education_Quintile','incquint_updated'] 
categorical = ['sex', 'Premature', 'RIO_cat', 'Material_deprivation','Education_Quintile','incquint_updated'] 

#Create TableOne Object 
table1 = TableOne(df, columns=variables, categorical=categorical, groupby='Cohort', pval=True, smd=True, missing=True)
table1.to_csv(FILE_NAME)


def replace_1_5(value):
    try: 
        if 1 <= float(value) <= 5: 
            return '1-5'
        else: 
            return value
    except: 
        return value #Returning value if cannot be converted to foat


####### ICD10 ########

##Create a Table 1 of Cause of Death Data - One-hot encoding the ICD columns
df_encoded = pd.get_dummies(df['ICD10_category'], prefix='', prefix_sep='').add_prefix('ICD_')
df_encoded.replace({1: 'Yes', 0: 'No'}, inplace=True)

#Add in some of the columns
df_encoded['ICD'] = df['ICD10_category']
df_encoded['Cohort'] = df['Cohort']
df_encoded['Premature'] = df['Premature']

#Create TableOne Object 
table1_ICD = TableOne(df_encoded, columns=list(df_encoded.columns), categorical=list(df_encoded.columns), groupby='Cohort', pval=True, smd=True)
table1_ICD = table1_ICD.tableone.applymap(replace_1_5)
table1_ICD.to_csv(FILE_NAME)

#Create TableOne Object - PREMATURE
df_encoded_prem = df_encoded[df_encoded['Premature']==1]
table1_ICD_PREM = TableOne(df_encoded_prem, columns=list(df_encoded_prem.columns), categorical=list(df_encoded_prem.columns), groupby='Cohort', pval=True, smd=True)
table1_ICD_PREM.to_csv(FILE_NAME)

#Create TableOne Object - NON-PREMATURE
df_encoded_Nprem = df_encoded[df_encoded['Premature']==0]
table1_ICD_NPREM = TableOne(df_encoded_Nprem, columns=list(df_encoded_Nprem.columns), categorical=list(df_encoded_Nprem.columns), groupby='Cohort', pval=True, smd=True)
table1_ICD_NPREM.to_csv(FILE_NAME)


####### LCD ########

##Create a Table 1 of Cause of Death Data - One-hot encoding the ICD columns
df_encoded = pd.get_dummies(df['lcd'], prefix='', prefix_sep='')
df_encoded.replace({1: 'Yes', 0: 'No'}, inplace=True)

#Add in some of the columns
df_encoded['ICD'] = df['lcd']
df_encoded['Cohort'] = df['Cohort']
df_encoded['Premature'] = df['Premature']

#Create TableOne Object 
table1_LCD = TableOne(df_encoded, columns=list(df_encoded.columns), categorical=list(df_encoded.columns), groupby='Cohort', pval=True, smd=True)
table1_LCD.to_csv(FILE_NAME)

#Create TableOne Object - PREMATURE
df_encoded_prem = df_encoded[df_encoded['Premature']==1]
table1_LCD_PREM = TableOne(df_encoded_prem, columns=list(df_encoded_prem.columns), categorical=list(df_encoded_prem.columns), groupby='Cohort', pval=True, smd=True)
table1_LCD_PREM.to_csv(FILE_NAME)

#Create TableOne Object - NON-PREMATURE
df_encoded_Nprem = df_encoded[df_encoded['Premature']==0]
table1_LCD_NPREM = TableOne(df_encoded_Nprem, columns=list(df_encoded_Nprem.columns), categorical=list(df_encoded_Nprem.columns), groupby='Cohort', pval=True, smd=True)
table1_LCD_NPREM = table1_LCD_NPREM.applymap(lambda x:'1-5' if isinstance(x, (int, float)) and 1 <= x <=5 else x)
table1_LCD_NPREM.to_csv(FILE_NAME)



exit()


##################################

#K diseases by cohort 
table_K = pd.crosstab(df['K_digestive_causes'], df['Cohort'])
table_K_percent = pd.crosstab(df['K_digestive_causes'], df['Cohort'], normalize='columns', margins=True, margins_name='Total') #Returns percentages


#ICD 10 Category - by Premature
table_ICD10_prem = df.groupby(['Cohort','Premature','ICD10_category']).size().reset_index(name='count')
table_ICD10_prem = table_ICD10_prem.pivot_table(index='ICD10_category',columns=['Cohort','Premature'], values='count', fill_value=0)


#LCD Category - by Premature
LCD_prem = df.groupby(['Cohort','Premature','lcd']).size().reset_index(name='count')
LCD_prem = LCD_prem.pivot_table(index='lcd',columns=['Cohort','Premature'], values='count', fill_value=0)
LCD_prem.to_csv(FILE_NAME)


##### #Cross-tabulate COD - IBD

df_IBD = df[df['Cohort']=="Case"] #selecting people with IBD from dataframe
total_IBD = len(df_IBD) #total number of people with IBD 

#Cross-tabilating and exporting the results
IBD_crosstab = pd.crosstab(df_IBD['lcd'], df_IBD['ICD10_category'], dropna=False) #cross-tab COD

#Creating a version to export 
IBD_num_export = IBD_crosstab.copy()
IBD_num_export.replace(to_replace=range(1,6), value="1-5", inplace=True)
IBD_num_export.to_csv(FILE_NAME/) #export statement

#Creating a list of the LCD codes for the y label 
index_list = IBD_num_export.index.tolist()
index_list = [string.replace("_"," ") for string in index_list]

#Extracting the coluns names for later 
ICD_names = IBD_crosstab.columns

#Plotting a heatmap of the numbers - 
plt.figure(figsize=(6,18))
sns.heatmap(IBD_crosstab, annot=False, cmap="Blues")
plt.xlabel('ICD-10 Categories', fontsize=12, fontweight='bold')
plt.ylabel('LCD Categories', fontsize=12, fontweight='bold')
plt.yticks(ticks=range(len(index_list)), labels=index_list)
#plt.title('Heatmap of Crosstabulated Data for IBD Patients ')
plt.tight_layout()
plt.savefig(FILE_NAME)
plt.show()

#Plotting a heatmap of the numbers - annotated
plt.figure(figsize=(6,18))
sns.heatmap(IBD_crosstab, annot=False, cmap="Blues")

#Manually annotating 
for i in range(len(IBD_crosstab)):
    for j in range(len(IBD_crosstab.columns)):
        value = IBD_crosstab.iloc[i,j]
        if value > 5: 
            plt.text(j + 0.5, i + 0.5, str(value), ha='center', va='center', fontsize=8)
        elif value == 0: 
            plt.text(j + 0.5, i + 0.5, "", ha='center', va='center', fontsize=8)
        else: 
            plt.text(j + 0.5, i + 0.5, "1-5", ha='center', va='center', fontsize=8)

plt.xlabel('ICD-10 Categories', fontsize=12, fontweight='bold')
plt.ylabel('LCD Categories', fontsize=12, fontweight='bold')
plt.yticks(ticks=range(len(index_list)), labels=index_list)
#plt.title('Heatmap of Crosstabulated Data for IBD Patients ')
plt.tight_layout()
plt.savefig(FILE_NAME)
plt.show()


#Using percents
IBD_crosstab_percent = IBD_crosstab.copy() #copy so that I have both numerical and percent 
for name in ICD_names: 
    IBD_crosstab_percent[name] = IBD_crosstab_percent[name]/total_IBD*100

#Find the max percentage 
IBD_crosstab_percent.max(axis=1).max(axis=0)
#The greatest percentage for IBD deaths is: 64.93244096476828

#exporting the percent file
IBD_crosstab_percent.to_csv(FILE_NAME)

#Create a rounded version for the heatmap
IBD_crosstab_percent_rounded = IBD_crosstab_percent.round(1)

#exporting the percent file
IBD_crosstab_percent.to_csv(FILE_NAME)


#Plotting a heatmap of the percents - 
plt.figure(figsize=(6,18))
sns.heatmap(IBD_crosstab_percent, annot=False, cmap="Blues", vmin=0, vmax=10)
plt.xlabel('ICD-10 Categories', fontsize=12, fontweight='bold')
plt.ylabel('LCD Categories', fontsize=12, fontweight='bold')
plt.yticks(ticks=range(len(index_list)), labels=index_list)
#plt.title('Heatmap of Crosstabulated Data for IBD Patients ')
plt.tight_layout()
plt.savefig(FILE_NAME)
plt.show()

#Plotting a heatmap of the numbers - annotated
plt.figure(figsize=(6,18))
sns.heatmap(IBD_crosstab_percent, annot=False, cmap="Blues", vmin=0, vmax=10)

#Manually annotating 
for i in range(len(IBD_crosstab_percent_rounded)):
    for j in range(len(IBD_crosstab_percent_rounded.columns)):
        value = IBD_crosstab_percent_rounded.iloc[i,j]
        if value >= 0.1: 
            plt.text(j + 0.5, i + 0.5, str(value)+"%", ha='center', va='center', fontsize=7)
        else: 
            plt.text(j + 0.5, i + 0.5, "", ha='center', va='center', fontsize=7)

plt.xlabel('ICD-10 Categories', fontsize=12, fontweight='bold')
plt.ylabel('LCD Categories', fontsize=12, fontweight='bold')
plt.yticks(ticks=range(len(index_list)), labels=index_list)
#plt.title('Heatmap of Crosstabulated Data for IBD Patients ')
plt.tight_layout()
plt.savefig(FILE_NAME)
plt.show()



##### #Cross-tabulate COD - matched controls

df_control = df[df['Cohort']=="Control"] #selecting people with IBD from dataframe
total_control = len(df_control) #total number of people with IBD 

#Cross-tabulating and exporting the results
control_crosstab = pd.crosstab(df_control['lcd'], df_control['ICD10_category'], dropna=False) #cross-tab COD

#Creating a version to export 
control_num_export = control_crosstab.copy()
control_num_export.replace(to_replace=range(1,6), value="1-5", inplace=True)
control_num_export.to_csv('/linux_home/gepostill/Files/u/gepostill/EXPORT/control_crosstab_num_export.csv') #export statement

#Extracting the coluns names for later 
control_names = control_crosstab.columns

#Creating a list of the LCD codes for the y label 
index_list = control_num_export.index.tolist()
index_list = [string.replace("_"," ") for string in index_list]

#Plotting a heatmap of the numbers 
plt.figure(figsize=(6,18))
sns.heatmap(control_crosstab, annot=False, cmap="Blues")
plt.xlabel('ICD-10 Categories', fontsize=12, fontweight='bold')
plt.ylabel('LCD Categories', fontsize=12, fontweight='bold')
plt.yticks(ticks=range(len(index_list)), labels=index_list)
#plt.xticks(rotation=80)
#plt.title('Heatmap of Crosstabulated Data for Control Patients ')
plt.tight_layout()
plt.savefig(FILE_NAME)
plt.show()

#Plotting a heatmap of the numbers - annotated
plt.figure(figsize=(6,18))
sns.heatmap(control_crosstab, annot=False, cmap="Blues")

#Manually annotating 
for i in range(len(control_crosstab)):
    for j in range(len(control_crosstab.columns)):
        value = control_crosstab.iloc[i,j]
        if value > 5: 
            plt.text(j + 0.5, i + 0.5, str(value), ha='center', va='center', fontsize=8)
        elif value == 0: 
            plt.text(j + 0.5, i + 0.5, "", ha='center', va='center', fontsize=8)
        else: 
            plt.text(j + 0.5, i + 0.5, "1-5", ha='center', va='center', fontsize=8)

plt.xlabel('ICD-10 Categories', fontsize=12, fontweight='bold')
plt.ylabel('LCD Categories', fontsize=12, fontweight='bold')
plt.yticks(ticks=range(len(index_list)), labels=index_list)
#plt.title('Heatmap of Crosstabulated Data for IBD Patients ')
plt.tight_layout()
plt.savefig(FILE_NAME)
plt.show()


#Using percents
control_crosstab_percent = IBD_crosstab.copy() #copy so that I have both numerical and percent 
for name in ICD_names: 
    control_crosstab_percent[name] = control_crosstab_percent[name]/total_control*100

#Find the max percentage 
control_crosstab_percent.max(axis=1).max(axis=0)
#The greatest percentage for IBD deaths is: 64.93244096476828

#exporting the percent file
control_crosstab_percent.to_csv(FILE_NAME)


#Create a rounded version for the heatmap
control_crosstab_percent_rounded = control_crosstab_percent.round(1)

#Plotting a heatmap of the percents - 
plt.figure(figsize=(6,18))
sns.heatmap(control_crosstab_percent, annot=False, cmap="Blues", vmin=0, vmax=70)
plt.xlabel('ICD-10 Categories', fontsize=12, fontweight='bold')
plt.ylabel('LCD Categories', fontsize=12, fontweight='bold')
plt.yticks(ticks=range(len(index_list)), labels=index_list)
#plt.title('Heatmap of Crosstabulated Data for IBD Patients ')
plt.tight_layout()
plt.savefig(FILE_NAME)
plt.show()

#Plotting a heatmap of the numbers - annotated
plt.figure(figsize=(6,18))
sns.heatmap(control_crosstab_percent, annot=False, cmap="Blues", vmin=0, vmax=70)

#Manually annotating 
for i in range(len(control_crosstab_percent_rounded)):
    for j in range(len(control_crosstab_percent_rounded.columns)):
        value = control_crosstab_percent_rounded.iloc[i,j]
        if value >= 0.1: 
            plt.text(j + 0.5, i + 0.5, str(value)+"%", ha='center', va='center', fontsize=7)
        else: 
            plt.text(j + 0.5, i + 0.5, "", ha='center', va='center', fontsize=7)

plt.xlabel('ICD-10 Categories', fontsize=12, fontweight='bold')
plt.ylabel('LCD Categories', fontsize=12, fontweight='bold')
plt.yticks(ticks=range(len(index_list)), labels=index_list)
#plt.title('Heatmap of Crosstabulated Data for IBD Patients ')
plt.tight_layout()
plt.savefig(FILE_NAME)
plt.show()







