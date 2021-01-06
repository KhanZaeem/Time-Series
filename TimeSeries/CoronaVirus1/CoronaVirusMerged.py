#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np  
import pandas as pd  
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os
import plotly.express as px # Display Plot in Browser
from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
sns.set_context('paper')


# In[2]:


data = pd.read_csv('2019_nCoV_data.csv') # Daily level information on the number of 2019-nCoV affected cases across the globe	


# In[3]:


#data = pd.read_csv('covid_19_data.csv') # Daily level information on the number of Covid 2019 affected cases across the globe	
print('Head\n',data.head())
print('\nInfo\n',data.info())
print('\nStatistical Description\n',data.describe())
print('\nStatistical Description (Zeros)\n',data.describe(include="O"))


# In[4]:


data['Last Update'] = pd.to_datetime(data['Last Update'])
data['Day'] = data['Last Update'].apply(lambda x:x.day)
data['Hour'] = data['Last Update'].apply(lambda x:x.hour)


# In[5]:


print('\nDay 30 Data\n',data[data['Day'] == 30])


# In[6]:


print('\nDay 30 Sum\n',data[data['Day'] == 30].sum())


# In[7]:


latest_data = data[data['Day'] == 30]
print(latest_data.head())


# In[8]:


print('\nGlobally Confirmed Cases: ',latest_data['Confirmed'].sum())
print('Global Deaths: ',latest_data['Deaths'].sum())
print('Globally Recovered Cases: ',latest_data['Recovered'].sum())


# In[9]:


plt.figure(figsize=(16,6))
data.groupby('Day').sum()['Confirmed'].plot()
plt.ylabel('Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[10]:


plt.figure(figsize=(16,6))
sns.barplot(x='Day',y='Confirmed',data=data)
plt.show()


# In[11]:


# In Depth EDA
print(latest_data.groupby('Country').sum())


# In[12]:


# Mainland China has Non-Zero values for Recovery and Deaths that can be explored later By creating a separate DataFrame
print(data[data['Confirmed']==0])


# In[13]:


# It is interesting to see that there are parts of Mainland China which have not been affected by the Virus yet
# There are some countries with zero confirmed reports and we will drop those data
data = data[data['Confirmed'] != 0]
plt.figure(figsize=(18,8))
sns.barplot(x='Country',y='Confirmed',data=data)
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
plt.tight_layout()
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[14]:


# 1] The Graph Shows the fact we all know that the virus has affected mainland china the most.
#    However there are also victims reported in nearby countries, suggesting that the virus is spreading

# 2] There are also reports confirmed in countries that are very much far away like US,Thailand,Japan, etc. 
#    Wonder how the virus got there. 
#    The guess is someone was in Wuhan or nearby area at the time of virus spread and carried it with them back home
#    and indeed this outbreak is dangerous.

# Display in Browser
fig = px.bar(data, x='Province/State', y='Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
fig.show()
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[15]:


plt.figure(figsize=(16,6))
temp = latest_data.groupby(['Province/State']).sum()['Confirmed'].plot.bar()
plt.ylabel('Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[16]:


# A look at the growth of corona virus in each country individually
pivoted = pd.pivot_table(data, values='Confirmed', columns='Country', index='Day')
pivoted.plot(figsize=(16,10))
plt.ylabel('Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[17]:


# Visualizing the outbreak Province wise
pivoted = pd.pivot_table(data, values='Confirmed', columns='Province/State', index='Day')
pivoted.plot(figsize=(20,15))
plt.ylabel('Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[18]:


# Hubei Seems to be the most badly affected province.
# Also the reported cases show an increasing trend and it seems the condition is getting worse

# Now Lets Look at the Countries that were affected initially and the countries to which corona virus has reached now.
data[data['Day'] == 22]['Country'].unique()


# In[19]:


# So on the starting day that is 22nd Jan, reports were found in China , USA , Japan , Thailand.
temp = data[data['Day'] == 22]
temp.groupby('Country').sum()['Confirmed'].plot.bar()
plt.ylabel('Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[20]:


# Looking at The latest Data
print(data[data['Day'] == 30]['Country'].unique())


# In[21]:


# We can see that the outbreak has spread to 23 countries now.

# Looking at only Mainland China
data_main_china = latest_data[latest_data['Country']=='Mainland China']
print((data_main_china['Deaths'].sum() / data_main_china['Confirmed'].sum())*100)
print((data_main_china['Recovered'].sum() / data_main_china['Confirmed'].sum())*100)


# In[22]:


# We can see the death percentage for coronavirus is at 2 percent so its not as deadly as other virus outbreaks
# Since we still do not have a cure for the virus we see that the recovery percentage is at 1.87, thats scary

# Let's See where the most of deaths have happened
print(data_main_china.groupby('Province/State')['Deaths'].sum().reset_index().sort_values(by=['Deaths'],ascending=False).head())

plt.figure(figsize=(16,6))
data.groupby('Day').sum()['Deaths'].plot()
plt.ylabel('Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[23]:


pivoted = pd.pivot_table(data[data['Country']=='Mainland China'] , values='Confirmed', columns='Province/State', index='Day')
pivoted.plot(figsize=(20,15))
plt.ylabel('Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[24]:


pivoted = pd.pivot_table(data, values='Deaths', columns='Province/State', index='Day')
pivoted.plot(figsize=(20,15))
plt.ylabel('Confirmed')
plt.title('Epidemiological Analysis of the Novel Coronavirus Disease 2019 Outbreak')
plt.show()


# In[25]:


#dropping the 1st and 5th column
#data.drop("SNo", axis=1, inplace=True)
#data.drop("Last Update", axis=1, inplace=True)
data






# In[26]:


#getting a summary of the columns
print(data.info())
print(data.describe())


# In[27]:


#checking for duplicate rows
duplicate_rows=data.duplicated(['Country','Province/State','Date'])
print(data[duplicate_rows])


# In[28]:


#listing all the countries where the virus has spread to
country_list=list(data['Country'].unique())
print(country_list)
print(len(country_list))


# In[29]:


#merging China and Mainland China
data.loc[data['Country']=='Mainland China','Country']='China'
print(list(data['Date'].unique()))
print(len(list(data['Date'].unique())))


# In[30]:


#converting 'Date' column to datetime object
data['Date'] = pd.to_datetime(data['Date'])
#extracting dates from timestamps
data['Date_date']=data['Date'].apply(lambda x:x.date())
#getting the total number of confirmed cases for each country
df_country=data.groupby(['Country']).max().reset_index(drop=None)
print(df_country[['Country','Confirmed','Deaths','Recovered']])


# In[31]:


#preparing data for a time-series analysis
df_by_date=data.groupby(['Date_date']).sum().reset_index(drop=None)
df_by_date['daily_cases']=df_by_date.Confirmed.diff()
df_by_date['daily_deaths']=df_by_date.Deaths.diff()
df_by_date['daily_recoveries']=df_by_date.Recovered.diff()
print('By Date')
print(df_by_date)


# In[32]:


# Plotting the data

# 1] Plotting a bar chart of confirmed cases over time
sns.axes_style("whitegrid")
sns.barplot(x="Date_date", y="Confirmed", data=data.groupby(['Date_date']).sum().reset_index(drop=None))
plt.xticks(rotation=60)
plt.ylabel('Number of confirmed cases',fontsize=15)
plt.xlabel('Dates',fontsize=15)
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()


# In[33]:


# 2] Rate of death vs rate of recovery
#    Plotting two line plots for deaths and recoveries respectively
plt.plot('daily_cases', 'Deaths', data=df_by_date.groupby(['daily_cases']).sum().reset_index(drop=None), color='red')
plt.plot('daily_cases', 'Recovered', data=df_by_date.groupby(['daily_cases']).sum().reset_index(drop=None), color='green')
plt.xticks(rotation=60)
plt.ylabel('Number of cases',fontsize=15)
plt.xlabel('Dates',fontsize=15)
plt.legend()
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()


# In[34]:


# 3] Ten most affected countries, besides China
#    We know that China is the most affected country by a large margin, 
#    so lets create a bar plot to compare countries other than China increasing the figure size
plt.rcParams['figure.figsize']=(15,7)
sns.barplot(x="Country",y="Confirmed",data=df_country[df_country.Country!='China'].nlargest(10,'Confirmed'),
            palette=sns.cubehelix_palette(15, reverse=True))
plt.ylabel('Number of cases',fontsize=15)
plt.xlabel('Countries',fontsize=15)
plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()


# In[35]:


# 4] Mortality rate over time
#    The mortality rate, at any point in time, 
#    can be roughly calculated by dividing the number of deaths by the number of confirmed cases
df_by_date['mrate']=df_by_date.apply(lambda x: x['Deaths']*100/(x['Confirmed']), axis=1)
plt.plot('Date_date','mrate',data=df_by_date, color='red')
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()


# In[36]:


# 5] A closer look at the Ten most affected provinces in China
#    creating a separate dataframe for provinces
df_province=data[data['Country']=='China'].groupby(['Province/State']).max().reset_index(drop=None)

#selecting 10 most affected provinces
df_province=df_province.nlargest(10,'Confirmed')
df_province=df_province[['Province/State','Deaths','Recovered']]


# In[37]:


# For multi-bar plots in seaborn, we need to melt the dataframe so that 
# the deaths and recovered values are in the same column
df_province= df_province.melt(id_vars=['Province/State'])

sns.barplot(x='Province/State', y='value', hue='variable', data=df_province)
plt.xlabel('Provinces',fontsize=15)
plt.ylabel('Number of cases',fontsize=15)
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()


# In[ ]:




