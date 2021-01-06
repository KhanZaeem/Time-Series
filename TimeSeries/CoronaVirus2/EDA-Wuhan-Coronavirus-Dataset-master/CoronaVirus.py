import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
#reading data from the csv file
data= pd.read_csv("2019_nCoV_data.csv")

#data= pd.read_csv("G:\\PythonWorkSpace\\ML\\Image Processing - SkLearn\\CoronaVirus\\2019_nCoV_data.csv")

#checking the number of rows and columns
print(data.shape)
#checking the top 5 rows
print(data.head())
#dropping the 1st and 5th column
data.drop("Sno", axis=1, inplace=True)
data.drop("Last Update", axis=1, inplace=True)
#getting a summary of the columns
print(data.info())
print(data.describe())
#checking for duplicate rows
duplicate_rows=data.duplicated(['Country','Province/State','Date'])
print(data[duplicate_rows])
#listing all the countries where the virus has spread to
country_list=list(data['Country'].unique())
print(country_list)
print(len(country_list))
#merging China and Mainland China
data.loc[data['Country']=='Mainland China','Country']='China'
print(list(data['Date'].unique()))
print(len(list(data['Date'].unique())))
#converting 'Date' column to datetime object
data['Date'] = pd.to_datetime(data['Date'])
#extracting dates from timestamps
data['Date_date']=data['Date'].apply(lambda x:x.date())
#getting the total number of confirmed cases for each country
df_country=data.groupby(['Country']).max().reset_index(drop=None)
print(df_country[['Country','Confirmed','Deaths','Recovered']])

#preparing data for a time-series analysis
df_by_date=data.groupby(['Date_date']).sum().reset_index(drop=None)
df_by_date['daily_cases']=df_by_date.Confirmed.diff()
df_by_date['daily_deaths']=df_by_date.Deaths.diff()
df_by_date['daily_recoveries']=df_by_date.Recovered.diff()
print('By Date')
print(df_by_date)

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

# 4] Mortality rate over time
#    The mortality rate, at any point in time, 
#    can be roughly calculated by dividing the number of deaths by the number of confirmed cases
df_by_date['mrate']=df_by_date.apply(lambda x: x['Deaths']*100/(x['Confirmed']), axis=1)
plt.plot('Date_date','mrate',data=df_by_date, color='red')
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()

# 5] A closer look at the Ten most affected provinces in China
#    creating a separate dataframe for provinces
df_province=data[data['Country']=='China'].groupby(['Province/State']).max().reset_index(drop=None)

#selecting 10 most affected provinces
df_province=df_province.nlargest(10,'Confirmed')
df_province=df_province[['Province/State','Deaths','Recovered']]

# For multi-bar plots in seaborn, we need to melt the dataframe so that 
# the deaths and recovered values are in the same column
df_province= df_province.melt(id_vars=['Province/State'])

sns.barplot(x='Province/State', y='value', hue='variable', data=df_province)
plt.xlabel('Provinces',fontsize=15)
plt.ylabel('Number of cases',fontsize=15)
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()
plt.show()



