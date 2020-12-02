#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


def read_exl(filename):
    temp = pd.read_excel(filename)
    temp.head()
    return temp
read_exl("g1.xls")


# In[3]:


def return_key_word(_table):
    node_index = _table["kernel name:"][5:]
    to_node1 = _table["Unnamed: 1"][5:]
    to_node2 = _table["Unnamed: 2"][5:]
    to_node3 = _table["Unnamed: 3"][5:]
    to_node4 = _table["Unnamed: 4"][5:]
    return node_index, to_node1, to_node2, to_node3, to_node4


# In[4]:


res_table = read_exl("g1.xls")
_from0, _to01, _to02, _to03, to_04 = return_key_word(res_table)


# In[5]:


def _judge(_from, _to1, _to2, _to3, _to4):
    for i in range(len(_from)):
        if _to1[i + 5] != 0 and _from[i + 5] > _to1[i + 5] :
            return True
        if _to2[i + 5] != 0 and _from[i + 5] > _to2[i + 5] :
            return True
        if _to3[i + 5] != 0 and _from[i + 5] > _to3[i + 5] :
            return True
        if _to4[i + 5] != 0 and _from[i + 5] > _to4[i + 5] :
            return True
    return False


# In[6]:


import os
path = "./"
for file in os.listdir(path): 
    if file.split(".")[1] != "xls" and file.split(".")[1] != "xlsx":
        continue
    temp = read_exl(file)
    a,b,c,d,e = return_key_word(temp)
    print(_judge(a,b,c,d,e))


# In[ ]:




