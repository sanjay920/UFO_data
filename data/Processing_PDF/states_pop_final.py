
# coding: utf-8

# In[30]:


import PyPDF2 as p
from tabula import convert_into
from tabula import read_pdf


# In[31]:


pop_1870_1950= read_pdf("/Users/pavneetkaur/Desktop/states_population.pdf", pages=4)


# In[19]:


pop_1960_2010= read_pdf("/Users/pavneetkaur/Desktop/states_population.pdf", pages=5)


# In[32]:


convert_into("/Users/pavneetkaur/Desktop/states_population.pdf","/Users/pavneetkaur/Desktop/output_1870_2010.csv",output_format="csv",pages="4-5")

