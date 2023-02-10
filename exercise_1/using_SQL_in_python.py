#!/usr/bin/env python
# coding: utf-8

# # Using SQL in Python

# In[ ]:


#installing packages
get_ipython().system('pip install -q -U pandas')
get_ipython().system('pip install -q ipython-sql')


# In[1]:


#importing packages
import pandas as pd
import sqlite3
import requests
import io


# In[2]:


#importing the dataset from Github repository

url = 'https://raw.githubusercontent.com/manthayconte/python_for_data_analysis/main/exercise_1/dataset/diabetes.csv'
download = requests.get(url).content

df = pd.read_csv(io.StringIO(download.decode('utf-8')))


# In[3]:


#checking the dataset basic data
df.head()


# In[4]:


#the dataset has 768 observations and 9 variables
df.shape


# In[ ]:


#if you want to download the database from GitHub:
#url = 'https://github.com/manthayconte/python_for_data_analysis/tree/main/exercise_1/database/dbprojeto1.db'
#urllib.request.urlretrieve(url, 'dbprojeto1.db')


# In[5]:


#creating a connection to a SQLite database
cnn = sqlite3.connect('/Users/gabrielconte/Documents/GitHub/Python_data_analytics/exercise_1/database/dbprojeto1.db')


# In[6]:


#write the dataFrame to the database as a table
df.to_sql('diabetes', cnn, if_exists = 'replace')


# In[7]:


#loading the SQL extension 
get_ipython().run_line_magic('load_ext', 'sql')


# In[17]:


#defining the database
get_ipython().run_line_magic('sql', 'sqlite:////Users/gabrielconte/Documents/GitHub/Python_data_analytics/exercise_1/database/dbprojeto1.db')


# In[19]:


#checking the observations number
%%sql

SELECT count(*) as contagem

FROM diabetes


# In[34]:


get_ipython().run_cell_magic('sql', '', '\nSELECT * FROM diabetes LIMIT 5')


# In[40]:


#adding a column to categorize the Age 
%%sql

ALTER TABLE diabetes
ADD age_group VARCHAR(20)


# In[42]:


#adding the categorized information in age_group
%%sql
UPDATE diabetes
SET age_group = (CASE
    WHEN Age < 20 THEN 'LESS THEN 20'
    WHEN Age >= 20 AND Age < 30 THEN 'BETWEEN 20 AND 30'
    WHEN Age >= 30 AND Age < 40 THEN 'BETWEEN 30 AND 40'
    WHEN Age >= 40 AND Age <= 50 THEN 'BETWEEN 40 AND 50'
    WHEN Age > 50 THEN 'MORE THEN 50'
  END)


# In[44]:


#checking the new column
%%sql

SELECT * FROM diabetes LIMIT(5)


# In[73]:


#descriptive analysis using categorized age_group
%%sql
SELECT
    CASE WHEN Outcome = 0 THEN 'NO' ELSE 'YES' END as 'diabetes',
    age_group,
    ROUND(AVG(Glucose),0) as 'AVG_glucose',
    MAX(Glucose) as 'MAX_glucose',
    MIN(Glucose) as 'MIN_glucose',
    ROUND(AVG(BloodPressure),0) as 'AVG_bloodPressure',
    MAX(BloodPressure) as 'MAX_bloodPressure',
    MIN(BloodPressure) as 'MIN_bloodPressure',
    ROUND(AVG(BMI),0) as 'AVG_bmi',
    MAX(BMI) as 'MAX_bmi',
    MIN(BMI) as 'MIN_bmi'
FROM diabetes 
GROUP BY age_group, Outcome

