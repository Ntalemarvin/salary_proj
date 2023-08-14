# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 12:54:50 2023

@author: MARVIN
"""
import pandas as pd
    
df = pd.read_csv('glassdoor_jobs.csv')

# Data Cleaning Todo-list
# salary parsing
# company name text only
# state field
# age of a company
# parsing of job description

# salary parsing

# creating cloumns hourly & employer provided
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0) 
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

# filtering -1s in salary estimate
df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

# company name text only
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-3],axis=1) #:-3 everthing until last 3 characters

# state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])

df['Same_Estate'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis =1)

# age of a company
df['age'] = df['Founded'].apply(lambda x: x if x <1 else 2023 - x)

# parsing of job description

# Python 
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

# R studio
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studo' or 'r-studio' in x.lower() else 0)

# spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)

# aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

# excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

df_out = df.drop(['Unnamed: 0'],axis = 1)
df_out.to_csv('salary_cleaned.csv',index = False)

