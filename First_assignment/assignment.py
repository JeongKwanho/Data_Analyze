import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats

####################Pretreatment about disaster#########################
disaster = pd.read_excel('자연재해.xlsx')
disaster.count()

disaster = disaster.drop(columns = ['ISO', 'Total Affected', 'Total Deaths', 'Total Damage (USD, original)', 'Total Damage (USD, adjusted)', 'CPI'])
disaster.groupby('Year').count()
disaster_count = disaster.groupby('Year')['Disaster Group'].count()
disaster_count = pd.DataFrame(disaster_count, disaster_count.index)
disaster_count.drop('#date +occurred', inplace = True)
disaster_count['Year'] = disaster_count.index
disaster_count['Year'] = disaster_count['Year'].astype('int')
disaster_count = disaster_count[['Year', 'Disaster Group']]
disaster_count.reset_index(drop = True, inplace = True)
disaster_count.info()

####################Pretreatment about Temperature######################
temperature = pd.read_csv('세계 온도.csv')
temperature.info()
temperature = temperature.dropna() #too much nan

temperature.count()
temperature.groupby('Country').count()
temperature.groupby('AverageTemperatureUncertainty').count()
temperature.groupby('dt').count()

temperature['dt'] = pd.to_datetime(temperature['dt'])
temperature['Year'] = temperature['dt'].dt.year
temperature.info()

temperature = temperature.drop(columns = ['dt', 'Country'])
temperature.sort_values(by = ['Year'], axis = 0, inplace = True)
temperature = temperature[temperature['Year'] >= 1900]
temp_year = temperature.groupby('Year')['AverageTemperature'].mean()
temp_year = pd.DataFrame(temp_year, temp_year.index)
#temp_year.drop('Year', inplace = True)
temp_year['Year'] = temp_year.index
temp_year = temp_year.astype('float')
temp_year.reset_index(drop = True, inplace = True)
temp_year.info()

####################Pretreatment about Energy Consumption######################
Energy_consuption = pd.read_excel('에너지 모음.xlsx', sheet_name = 'Total energy consumption')
Energy_consuption = Energy_consuption.transpose()
Energy_consuption.drop(columns = 0, index = ['Unnamed: 32', 'Unnamed: 33', 'Unnamed: 34'], inplace = True)

World_consuption = Energy_consuption.iloc[:, :2]
World_consuption.drop(index = ['Unnamed: 0'], inplace = True)
World_consuption.columns = ['Year', 'Consuption']
World_consuption = World_consuption.astype('int')
World_consuption.info()

####################Pretreatment about Oil products############################
Oil_product = pd.read_excel('에너지 모음.xlsx', sheet_name = 'Oil products domestic consumpt')
Oil_product = Oil_product.transpose()
Oil_product.drop(columns = 0, index = ['Unnamed: 32', 'Unnamed: 33', 'Unnamed: 34'], inplace = True)

Oil_product = Oil_product.iloc[:, :2]
Oil_product.drop(index = ['Unnamed: 0'], inplace = True)
Oil_product.columns = ['Year', 'Oil production']
Oil_product = Oil_product.astype('int')
Oil_product.info()

####################Pretreatment about CO2 Emission from fuel############################
CO2_product = pd.read_excel('에너지 모음.xlsx', sheet_name = 'CO2 emissions from fuel combus')
CO2_product = CO2_product.transpose()
CO2_product.drop(columns = 0, index = ['Unnamed: 32', 'Unnamed: 33', 'Unnamed: 34'], inplace = True)

CO2_product = Oil_product.iloc[:, :2]
#CO2_product.drop(index = ['Unnamed: 0'], inplace = True)
CO2_product.columns = ['Year', 'CO2 emissions']
CO2_product = CO2_product.astype('int')
CO2_product.info()

###############################Pretreatment Visulization###################################
sns.jointplot(x = CO2_product['Year'], y = CO2_product['CO2 emissions'])
sns.jointplot(x = Oil_product['Year'], y = Oil_product['Oil production'])
sns.jointplot(x = World_consuption['Year'], y = World_consuption['Consuption'])
sns.jointplot(x = temp_year.index, y = temp_year['AverageTemperature'])
sns.jointplot(x = disaster_count.index, y = disaster_count['Disaster Group'])

##########################check normaltest###########################################
stats.normaltest(disaster_count) #accept H1
stats.normaltest(temp_year) #accept H1
stats.normaltest(World_consuption) #accept H1
stats.normaltest(Oil_product) #accept H1
stats.normaltest(CO2_product) #accept H1

#Inappropriate use Pearson

##############################correlation coefficient###########################
disaster_corr = disaster_count.corr()
temp_corr = temp_year.corr()
Consuption_corr = World_consuption.corr()
Oil_corr = Oil_product.corr()
CO2_corr = CO2_product.corr()

###########################Merge Data####################################
merge_data = pd.merge(World_consuption, Oil_product, on = 'Year')
merge_data = pd.merge(merge_data, CO2_product, on = 'Year')
merge_data = pd.merge(merge_data, temp_year, on = 'Year')
merge_data = pd.merge(merge_data, disaster_count, on = 'Year')

##############################corrlation Merge######################
merge_corr = merge_data.corr()
sns.heatmap(data = merge_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')

merge_pe = merge_data.corr(method = 'pearson')
merge_kt = merge_data.corr(method = 'kendall')
merge_sp = merge_data.corr(method = 'spearman')

sns.heatmap(data = merge_pe, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
sns.heatmap(data = merge_kt, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
sns.heatmap(data = merge_sp, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')

sns.pairplot(merge_data)
sns.pairplot(merge_pe) # we have to use not pearson, not pass normaltest
sns.pairplot(merge_kt)
sns.pairplot(merge_sp)

# about kendall, disaster not realation other things. reason : result < 0.4

###########################relation graph(standard = kendall, y >= 0.4)###########################################
#Please, do it once

sns.lineplot(x = merge_data['Year'], y = merge_data['Consuption'], data = merge_data, label = 'con')
sns.lineplot(x = merge_data['Year'], y = merge_data['Oil production'], data = merge_data, label = 'Oil')
sns.lineplot(x = merge_data['Year'], y = merge_data['CO2 emissions'], data = merge_data, label = 'CO2')
sns.lineplot(x = merge_data['Year'], y = merge_data['AverageTemperature'], data = merge_data, label = 'Temp')

###########################additional : correlation about each(only kendall. not pass normaltest, use not pearson)#######################
con_oil = pd.merge(World_consuption, Oil_product, on = 'Year')
con_CO2 = pd.merge(World_consuption, CO2_product, on = 'Year')
con_temp = pd.merge(World_consuption, temp_year, on = 'Year')
con_dis = pd.merge(World_consuption, disaster_count, on = 'Year')
con_oil_corr = con_oil.corr(method = 'kendall')
con_CO2_corr = con_CO2.corr(method = 'kendall')
con_temp_corr = con_temp.corr(method = 'kendall')
con_dis_corr = con_dis.corr(method = 'kendall')

sns.heatmap(data = con_oil_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
sns.heatmap(data = con_CO2_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
sns.heatmap(data = con_temp_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
sns.heatmap(data = con_dis_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')

oil_CO2 = pd.merge(Oil_product, CO2_product, on = 'Year')
oil_temp = pd.merge(Oil_product, temp_year, on = 'Year')
oil_dis = pd.merge(Oil_product, disaster_count, on = 'Year')
oil_CO2_corr = oil_CO2.corr(method = 'kendall')
oil_temp_corr = oil_temp.corr(method = 'kendall')
oil_dis_corr = oil_temp.corr(method = 'kendall')

sns.heatmap(data = oil_CO2_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
sns.heatmap(data = oil_temp_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
sns.heatmap(data = oil_dis_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')

CO2_temp = pd.merge(CO2_product, temp_year, on = 'Year')
CO2_dis = pd.merge(CO2_product, disaster_count, on = 'Year')
CO2_temp_corr = CO2_temp.corr(method = 'kendall')
CO2_dis_corr = CO2_dis.corr(method = 'kendall')

sns.heatmap(data = CO2_temp_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
sns.heatmap(data = CO2_dis_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')

temp_dis = pd.merge(temp_year, disaster_count, on = 'Year')
temp_dis_corr = temp_dis.corr(method = 'kendall')

sns.heatmap(data = temp_dis_corr, annot = True, fmt = '.2f', linewidths = .5, cmap = 'Blues')
