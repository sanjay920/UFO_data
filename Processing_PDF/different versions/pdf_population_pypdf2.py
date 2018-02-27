
# coding: utf-8

# In[103]:


import PyPDF2 as p
from tabula import convert_into
from tabula import read_pdf
import csv


# In[104]:


reader= p.PdfFileReader(open("/Users/pavneetkaur/Desktop/pdf123.pdf","rb"))


# In[130]:


def get_population(page_num):
    page_num = 1
    df=read_pdf("/Users/pavneetkaur/Desktop/pdf123.pdf", pages=page_num)
    total_pop = list(df.iloc[:,1])
    year = list(df.iloc[:,0])
    pop = list(df.iloc[:,1])
    num_idx = year.index('NUMBER')
    percent_idx = year.index('PERCENT')
    for idx in zip(year[num_idx+1:percent_idx], pop[num_idx+1:percent_idx]):
        #print idx
        year = str(idx[0].split('...')[0]).strip()
        if len(year) == 4:
            print year,idx[1]
    return (year, idx[1])
#print (year[num_idx+1:percent_idx], pop[num_idx+1:percent_idx])
#return total_pop


# In[133]:


for pageNum in range(0, reader.numPages):
            get_page=reader.getPage(pageNum)
            abc=get_page.extractText().split("Table ")[:2]
            #print len(abc), abc
            state_name = ""
            if len(abc) ==2:
                state_name = abc[1].split('.')[1].split('-')[0]
            writer = open('/Users/pavneetkaur/Desktop/newsample.csv', 'a')
            #writer.write(str(state_name))
            total_pop = get_population(pageNum)
            
            
            #print state_name, total_pop
            
            writer.close()


# convert_into("/Users/pavneetkaur/Desktop/pdf123.pdf","/Users/pavneetkaur/Desktop/bypypdf2_solution.csv", output_format="csv")

# In[93]:




