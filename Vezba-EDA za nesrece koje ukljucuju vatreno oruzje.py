#!/usr/bin/env python
# coding: utf-8

# # *Analiza nesreća prouzrokovanih vatrenim oružjem*

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from plotly.offline  import download_plotlyjs,init_notebook_mode,plot, iplot
import cufflinks as cf
init_notebook_mode(connected = True)
cf.go_offline()
import datetime as dt
import seaborn as sns
import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.figure_factory as ff
import plotly.io as pio


# In[25]:


df = pd.read_csv('C:\\Users\\kosta\\gun_violence.csv')
df.sample(5)


# In[64]:


df.describe()


# #### Izbacivanje kolona koje mi za ovu analizu nisu potrebne:

# In[31]:


df.drop(columns=['incident_url', 'source_url','incident_url_fields_missing','sources','state_house_district','state_senate_district'],inplace= True)


# In[32]:


# menjanje kolone u odgovarajuci date format kako bi bila upotrebljiva
df['date'] = pd.to_datetime(df['date'])


# In[33]:


df['godina'] = df['date'].dt.year
df['godina']


# In[34]:


# pronalazenje procenta vrednosti koje nedostaju po kolonama

missing = df.isna().sum() / len(df) * 100
missing_value_df = pd.DataFrame({'percent_missing': missing})
missing_value_df.sort_values('percent_missing', ascending=False)


# In[8]:


df.state.value_counts().head(25).iplot(kind = 'bar', theme='solar', title = 'NESRECE PO STATE-OVIMA',)


# In[9]:


df.city_or_county.value_counts().head(10).iplot(kind = 'bar', theme = 'polar', title = 'Nesrece po gradovima', xTitle='Grad')


# * Top 5 gradova po nesrecama
#     * Cikago 
#     * Baltimor
#     * Vasington
#     * Novi Orleans
#     * Filadelfija

# In[10]:


dani = df['date'].value_counts().head(3)
pd.DataFrame(dani)


# * ####  po ovome vidimo da su najopasniji datumi upravo praznici, 1. januar (Nova Godina) i 4. jul (americki dan nezavisnosti)
# 

# In[15]:


broj_oruzja = df['n_guns_involved'].dropna().apply(lambda x: '4+' if x > 4 else float(x)) 
broj_oruzja = broj_oruzja.value_counts()
data = pd.DataFrame({'labels': broj_oruzja.index,
                   'values': broj_oruzja.values
                  })
data.iplot(kind='pie',labels='labels',values='values', title='Raspodela broja oruzja ukljucenih u incident ')


# * #### po ovome jasno vidimo da je velika vecina nesreca jednostrana, odnosno da je korisceno samo 1 oruzje. Ocigledno je da nam treba jos oruzja kako bi ljudi mogli da se brane.  

# In[21]:


bande = df.loc[(df['n_guns_involved'] >= 200)]
bande_df = bande['city_or_county'].value_counts().head(5)
pd.DataFrame(bande_df)


# * #### Gradovi i broj nesreca u koje je bilo ukljuceno vise od 200 oruzja. Treba dalje istraziti da li je to delo aktivnih bandi iz tih gradova. 

# In[82]:


df['povredjeni'] = df['n_injured'] + df['n_killed']

po_godinama = df['povredjeni'].groupby(by=df["godina"]).sum()
po_godinama
po_godinama.plot(figsize=(15,8))


# * #### Gornji plot ne prikazuje opadanje trenda nasilja vec podaci idu samo do marta 2018. godine

# In[83]:


item=df['state'].value_counts().head(30).index.tolist()
item_size=df['state'].value_counts().head(30).values.tolist()

cities = []
scale = 250


for i in range(len(item)):
    lim = item[i]
    df_sub = df.loc[df['state']==lim][:1]
    city = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df_sub['longitude'],
        lat = df_sub['latitude'],
        text = item[i] + '<br>Gun abuse ' + str(item_size[i]),
        marker = dict(
            size = item_size[i]/scale,
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = lim )
    cities.append(city)

layout = dict(
        title = 'Interaktivna mapa',
        
        geo = dict(
            scope='usa',
            projection=dict( type='miller usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

fig = dict( data=cities, layout=layout )
py.iplot( fig, validate=False, filename='d3-bubble-map-populations' )
plt.savefig('abc.png')   

