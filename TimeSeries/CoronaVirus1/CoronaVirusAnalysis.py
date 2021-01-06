# Epidemiological Analysis of the Novel Coronavirus Disease 2019 outbreak
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
"""
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory


for dirname, _, filenames in os.walk('.'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
"""
"""
def random_colours(number_of_colors):
    '''
    Simple function for random colours generation.
    Input:
        number_of_colors - integer value indicating the number of colours which are going to be generated.
    Output:
        Color in the following format: ['#E86DA4'] .
    '''
    colors = []
    for i in range(number_of_colors):
        colors.append("#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]))
    return colors
"""
# Statistical Analysis
data = pd.read_csv('2019_nCoV_data.csv') # Daily level information on the number of 2019-nCoV affected cases across the globe	
#data = pd.read_csv('covid_19_data.csv') # Daily level information on the number of Covid 2019 affected cases across the globe	
print('Head\n',data.head())
print('\nInfo\n',data.info())
print('\nStatistical Description\n',data.describe())
print('\nStatistical Description (Zeros)\n',data.describe(include="O"))

data['Last Update'] = pd.to_datetime(data['Last Update'])
data['Day'] = data['Last Update'].apply(lambda x:x.day)
data['Hour'] = data['Last Update'].apply(lambda x:x.hour)

print('\nDay 30 Data\n',data[data['Day'] == 30])

print('\nDay 30 Sum\n',data[data['Day'] == 30].sum())

latest_data = data[data['Day'] == 30]
print(latest_data.head())

print('\nGlobally Confirmed Cases: ',latest_data['Confirmed'].sum())
print('Global Deaths: ',latest_data['Deaths'].sum())
print('Globally Recovered Cases: ',latest_data['Recovered'].sum())

plt.figure(figsize=(16,6))
data.groupby('Day').sum()['Confirmed'].plot()
plt.show()

plt.figure(figsize=(16,6))
sns.barplot(x='Day',y='Confirmed',data=data)
plt.show()

# In Depth EDA
print(latest_data.groupby('Country').sum())
# Mainland China has Non-Zero values for Recovery and Deaths that can be explored later By creating a separate DataFrame

print(data[data['Confirmed']==0])

# It is interesting to see that there are parts of Mainland China which have not been affected by the Virus yet
# There are some countries with zero confirmed reports and we will drop those data
data = data[data['Confirmed'] != 0]
plt.figure(figsize=(18,8))
sns.barplot(x='Country',y='Confirmed',data=data)
locs, labels = plt.xticks()
plt.setp(labels, rotation=90)
plt.tight_layout()
plt.show()
# 1] The Graph Shows the fact we all know that the virus has affected mainland china the most.
#    However there are also victims reported in nearby countries, suggesting that the virus is spreading

# 2] There are also reports confirmed in countries that are very much far away like US,Thailand,Japan, etc. 
#    Wonder how the virus got there. 
#    The guess is someone was in Wuhan or nearby area at the time of virus spread and carried it with them back home
#    and indeed this outbreak is dangerous.

# Display in Browser
fig = px.bar(data, x='Province/State', y='Confirmed')
fig.show()
plt.show()

plt.figure(figsize=(16,6))
temp = latest_data.groupby(['Province/State']).sum()['Confirmed'].plot.bar()
plt.show()

# A look at the growth of corona virus in each country individually
pivoted = pd.pivot_table(data, values='Confirmed', columns='Country', index='Day')
pivoted.plot(figsize=(16,10))
plt.show()

# Visualizing the outbreak Province wise
pivoted = pd.pivot_table(data, values='Confirmed', columns='Province/State', index='Day')
pivoted.plot(figsize=(20,15))
plt.show()

# Hubei Seems to be the most badly affected province.
# Also the reported cases show an increasing trend and it seems the condition is getting worse

# Now Lets Look at the Countries that were affected initially and the countries to which corona virus has reached now.
data[data['Day'] == 22]['Country'].unique()
# So on the starting day that is 22nd Jan, reports were found in China , USA , Japan , Thailand.
temp = data[data['Day'] == 22]
temp.groupby('Country').sum()['Confirmed'].plot.bar()
plt.show()

# Looking at The latest Data
print(data[data['Day'] == 30]['Country'].unique())
# We can see that the outbreak has spread to 23 countries now.

# Looking at only Mainland China
data_main_china = latest_data[latest_data['Country']=='Mainland China']
print((data_main_china['Deaths'].sum() / data_main_china['Confirmed'].sum())*100)

print((data_main_china['Recovered'].sum() / data_main_china['Confirmed'].sum())*100)

# We can see the death percentage for coronavirus is at 2 percent so its not as deadly as other virus outbreaks
# Since we still do not have a cure for the virus we see that the recovery percentage is at 1.87, thats scary

# Let's See where the most of deaths have happened
print(data_main_china.groupby('Province/State')['Deaths'].sum().reset_index().sort_values(by=['Deaths'],ascending=False).head())

plt.figure(figsize=(16,6))
data.groupby('Day').sum()['Deaths'].plot()
plt.show()

pivoted = pd.pivot_table(data[data['Country']=='Mainland China'] , values='Confirmed', columns='Province/State', index='Day')
pivoted.plot(figsize=(20,15))
plt.show()

pivoted = pd.pivot_table(data, values='Deaths', columns='Province/State', index='Day')
pivoted.plot(figsize=(20,15))
plt.show()

