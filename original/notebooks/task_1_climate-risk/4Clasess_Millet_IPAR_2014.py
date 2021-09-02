#!/usr/bin/env python
# coding: utf-8

# IPAR crop Yield data 2014 for Millet: quantile-based yield clases

# libraries

# In[13]:


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# dataset

# In[14]:


df = pd.read_csv(r'C:\Users\Maily\AppData\Local\Programs\Python\Python38-32\MyData\IPAR2014_yields_ndvi_no_duplicates_Millet.csv')
df.head


# histogram of the Millet yield data

# In[25]:


ax = sns.displot(df["Yield"])
ax.set(xlabel='Milletr yield (T/ha)')


# Describe "Yield"

# In[18]:


df['Yield'].describe()


# Divide the data in four clases using the quantile-based discretization function pandas.qcut for Millet. 
# pandas.qcut(x, q, labels=None, retbins=False, precision=3, duplicates='raise')

# In[19]:


pd.qcut(df['Yield'], q=[0, .25, .5, .75, 1.])


# value counts in each bin 

# In[20]:


pd.qcut(df['Yield'], q=4, labels=["limited", "marginal", "moderate", "optimal"]).value_counts()


# Label the groups and store the results in "suitability".
# Show header

# In[21]:


df["suitability"] = pd.qcut(df['Yield'], q=[0, .25, .5, .75, 1.], labels=["limited", "marginal", "moderate", "optimal"])
df.head


# Create box plot with Seaborn's default settings for Millet. Label the axes.

# In[27]:


_ = sns.boxplot(x="suitability", y="Yield", data=df)
_ = plt.ylabel('yield (T/ha)')
_ = plt.title('Millet')
plt.show()


# In[ ]:




