
# coding: utf-8

# In[4]:


from tabula import read_pdf
from tabula import convert_into


# In[39]:


df=read_pdf("/Users/pavneetkaur/Desktop/pdf123.pdf", pages=1)


# In[38]:


df.iloc[:,1]


# In[5]:


convert_into("/Users/pavneetkaur/Desktop/pdf123.pdf","/Users/pavneetkaur/Desktop/output_population.csv", output_format="csv")

