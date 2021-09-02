#!/usr/bin/env python
# coding: utf-8

# IPAR crop Yield data 2014 for Maiz: quantile-based yield clases

# libraries

# In[1]:


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# dataset

# In[2]:


my = pd.read_csv(r'C:\Users\Maily\AppData\Local\Programs\Python\Python38-32\MyData\IPAR2014_yields_ndvi_no_duplicates_Maize.csv')


# histogram of the maiz yield data

# In[15]:


ax = sns.displot(my["Yield"])
ax.set(xlabel='Maize yield (T/ha)')


# Describe "Yield"

# In[16]:


my['Yield'].describe()


# Divide the data in four clases using the quantile-based discretization function pandas.qcut for maize. 
# pandas.qcut(x, q, labels=None, retbins=False, precision=3, duplicates='raise')

# In[17]:


pd.qcut(my['Yield'], q=[0, .25, .5, .75, 1.])


# value counts in each bin 

# In[18]:


pd.qcut(my['Yield'], q=4, labels=["limited", "marginal", "moderate", "optimal"]).value_counts()


# Label the groups and store the results in "suitability".
# Show header

# In[19]:


my["suitability"] = pd.qcut(my['Yield'], q=[0, .25, .5, .75, 1.], labels=["limited", "marginal", "moderate", "optimal"])
my.head


# Create box plot with Seaborn's default settings for maize. Label the axes.

# In[22]:


_ = sns.boxplot(x="suitability", y="Yield", data=my)
_ = plt.ylabel('yield (T/ha)')
_ = plt.title('Maize')
plt.show()


# In[ ]:




