#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 18:34:43 2024

@author: gepostill
"""


#Note - for privacy all file names are written as FILE_NAME to conceal the file path of data and figures on the laptop used to create the code

################################################
#Importing Packages   
################################################

import pandas as pd
import numpy as np
from tableone import TableOne


###############################################
#Importing Data   
################################################

#Importing the data -- all conditionals all ages 
data = pd.read_csv(FILE_NAME)


#Copying the original dataframe ans selecting the columns included in the prediction 
df = data.copy()

#`Subset to only IBD patients
#df = df[df["Cohort"]=="Case"]

#Remove deaths from 2019 and 2020 - these do not have cause of death
df = df[df["death_yr"]!=2019]
df = df[df["death_yr"]!=2020]


#MISSING DATA  
df = df.replace('.',np.nan)
missing_counts = df.isna().sum()
missing_counts_stratified = df.groupby('Cohort').apply(lambda x: x.isna().sum())


#Remove patients with missing cause of death 
df = df.dropna(subset='cod_underlying_icd10')


##Age 
age_stats = df.groupby('Cohort')['Age_death'].agg(['mean','std'])

def median(x): 
    return np.median(x)
def q25(x): 
    return np.percentile(x, 25)
def q75(x): 
    return np.percentile(x, 75)

age_median = df.groupby('Cohort')['Age_death'].agg([('Median', median), ('q25', q25), ('q75',q75)])


#Sex 
sex_stats = pd.crosstab(df['sex'], df['Cohort'], dropna=False)
sex_stats['case_per'] = sex_stats['Case']/sex_stats['Case'].sum()*100
sex_stats['control_per'] = sex_stats['Control']/sex_stats['Control'].sum()*100


#RIO
#Creating a function to dichotomize the numerical values into '>=40' and '<40'
def dichotomize(value):
    if value >= 40: 
        return 'Rural'
    elif value < 40: 
        return 'Urban'
    else: 
        return 'Not classified'

df['rio2008'] = df['rio2008'].astype(float)
df['RIO_cat'] = df['rio2008'].apply(dichotomize)

rio_stats = pd.crosstab(df['RIO_cat'], df['Cohort'], dropna=False)
rio_stats['case_per'] = rio_stats['Case']/rio_stats['Case'].sum()*100
rio_stats['control_per'] = rio_stats['Control']/rio_stats['Control'].sum()*100


#Material_deprivation 
dep_stats = pd.crosstab(df['Material_deprivation'], df['Cohort'], dropna=False)
dep_stats['case_per'] = dep_stats['Case']/dep_stats['Case'].sum()*100
dep_stats['control_per'] = dep_stats['Control']/dep_stats['Control'].sum()*100

#Income
inc_stats = pd.crosstab(df['incquint'], df['Cohort'], dropna=False)
inc_stats['case_per'] = inc_stats['Case']/inc_stats['Case'].sum()*100
inc_stats['control_per'] = inc_stats['Control']/inc_stats['Control'].sum()*100

#Education 
edu_stats = pd.crosstab(df['Education_Quintile'], df['Cohort'], dropna=False)
edu_stats['case_per'] = edu_stats['Case']/edu_stats['Case'].sum()*100
edu_stats['control_per'] = edu_stats['Control']/edu_stats['Control'].sum()*100

#Number of Chronic Conditions 
degree_stats = pd.crosstab(df['Degree_category'], df['Cohort'], dropna=False)
degree_stats['case_per'] = degree_stats['Case']/degree_stats['Case'].sum()*100
degree_stats['control_per'] = degree_stats['Control']/degree_stats['Control'].sum()*100


#Create TableOne Object 
variables = ['sex','Age_death', 'Material_deprivation', 'incquint', 'Education_Quintile', 'RIO_cat', 'Degree', 'lcd', 'Degree_Cat'] 
categorical = ['sex', 'Material_deprivation', 'incquint', 'Education_Quintile', 'RIO_cat', 'lcd', 'Degree_Cat'] 
df[categorical] = df[categorical].astype(str)


#Create TableOne Object 
table1 = TableOne(df, columns=variables, categorical=categorical, groupby='Cohort', pval=True, smd=True)
table1.to_csv(FILENAME)


