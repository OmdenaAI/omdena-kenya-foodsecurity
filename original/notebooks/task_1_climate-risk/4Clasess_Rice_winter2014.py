#!/usr/bin/env python
# coding: utf-8

# IPAR crop Yield data 2014 for Rice winter: quantile-based yield clases

# libraries

# In[3]:


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# dataset

# In[4]:


df = pd.read_csv(r'C:\Users\Maily\AppData\Local\Programs\Python\Python38-32\MyData\IPAR2014_yields_ndvi_no_duplicates_Rice_winter.csv')
df.head


# histogram of the Rice winter yield data

# In[22]:


ax = sns.displot(df["Yield"])
ax.set(xlabel='Rice winter yield (T/ha)')


# Describe "Yield"

# In[12]:


df['Yield'].describe()


# Divide the data in four clases using the quantile-based discretization function pandas.qcut for raice winter. 
# pandas.qcut(x, q, labels=None, retbins=False, precision=3, duplicates='raise')

# In[13]:


pd.qcut(df['Yield'], q=[0, .25, .5, .75, 1.])


# value counts in each bin 

# In[14]:


pd.qcut(df['Yield'], q=4, labels=["limited", "marginal", "moderate", "optimal"]).value_counts()


# Label the groups and store the results in "suitability".
# Show header

# In[15]:


df["suitability"] = pd.qcut(df['Yield'], q=[0, .25, .5, .75, 1.], labels=["limited", "marginal", "moderate", "optimal"])
df.head


# Create box plot with Seaborn's default settings for Raice CSC. Label the axes.

# In[25]:


_ = sns.boxplot(x="suitability", y="Yield", data=df)
_ = plt.ylabel('yield (T/ha)')
_ = plt.title('Rice winter')
plt.show()


# In[ ]:





# In[ ]:




