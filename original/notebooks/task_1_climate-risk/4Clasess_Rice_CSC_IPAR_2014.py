#!/usr/bin/env python
# coding: utf-8

# IPAR crop Yield data 2014 for Rice CSC: quantile-based yield clases

# libraries

# In[1]:


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# dataset

# In[2]:


df = pd.read_csv(r'C:\Users\Maily\AppData\Local\Programs\Python\Python38-32\MyData\IPAR2014_yields_ndvi_no_duplicates_ Rice_CSC.csv')
df.head


# histogram of the Rice CSC yield data

# In[8]:


ax = sns.displot(df["Yield"])
ax.set(xlabel='Rice CSC yield (T/ha)')


# Describe "Yield"

# In[9]:


df['Yield'].describe()


# Divide the data in four clases using the quantile-based discretization function pandas.qcut for raice CSC. 
# pandas.qcut(x, q, labels=None, retbins=False, precision=3, duplicates='raise')

# In[10]:


pd.qcut(df['Yield'], q=[0, .25, .5, .75, 1.])


# value counts in each bin 

# In[11]:


pd.qcut(df['Yield'], q=4, labels=["limited", "marginal", "moderate", "optimal"]).value_counts()


# Label the groups and store the results in "suitability".
# Show header

# In[12]:


df["suitability"] = pd.qcut(df['Yield'], q=[0, .25, .5, .75, 1.], labels=["limited", "marginal", "moderate", "optimal"])
df.head


# Create box plot with Seaborn's default settings for Raice CSC. Label the axes.

# In[14]:


_ = sns.boxplot(x="suitability", y="Yield", data=df)
_ = plt.ylabel('yield (T/ha)')
_ = plt.title('Rice CSC')
plt.show()


# In[ ]:




