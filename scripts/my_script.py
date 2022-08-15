#!/usr/bin/env python
# coding: utf-8


import pandas as pd #import pandas and requests
import requests
weather_df = pd.read_csv('weather.csv') #import csvs to 3 separate dataframes
crop_df = pd.read_csv('crop.csv')
spectral_df = pd.read_csv('spectral.csv')
soil_df = pd.read_csv('soil.csv') 


#Q1
crops_2021 = crop_df[crop_df['year'] == 2021] #filter out only entries with year 2021
crops_2021 = crops_2021.drop(['year'], axis = 1) #remove year features
crops_2021 = crops_2021.set_index('field_id') #setting field_id as the index
crops_2021.to_csv('Q1.csv')

#Q2
spectral_df['NDVI'] = (spectral_df['nir'] - spectral_df['red'])/(spectral_df['nir'] + spectral_df['red']) #formula
spectral_df = spectral_df.sort_values(by=['NDVI'], ascending = False) 
largest_NDVI = spectral_df.head(1) #get the largest value after sorting descending
largest_NDVI.rename(columns={'NDVI':'POS value'} ,inplace=True)
largest_NDVI = largest_NDVI.drop(['nir', 'red'], axis = 1)
largest_NDVI.set_index('tile_id')
largest_NDVI.to_csv('Q2.csv')


#Q3
soil_df['horizontal_layer_weights'] = (abs(soil_df['hzdept']-soil_df['hzdepb']))/soil_df['hzdepb'] #formula
soil_df['percentage_component'] = soil_df['comppct']*0.01 #change percentage number to decimal format between 0 and 1
soil_df['weighted_ph'] = soil_df['ph']*soil_df['horizontal_layer_weights']*soil_df['percentage_component'] #weighted sums by percentage component
soil_df['weighted_cec'] = soil_df['cec']*soil_df['horizontal_layer_weights']*soil_df['percentage_component']
soil_df['weighted_om'] = soil_df['om']*soil_df['horizontal_layer_weights']*soil_df['percentage_component']
soil_df = soil_df.groupby(by=["mukey"]).sum() #Total grouped by mukey
soil_final = soil_df[['weighted_ph', 'weighted_cec', 'weighted_om']]
soil_final.rename(columns={'weighted_ph':'ph', 'weighted_cec': 'cec', 'weighted_om': 'om'} ,inplace=True)
soil_final.to_csv('Q3.csv')


#Q4
weather_df = weather_df[weather_df['year'] == 2021]
min_temp = weather_df.groupby(by=["fips_code"]).min() #Min temp group by fips code
max_temp = weather_df.groupby(by=["fips_code"]).max() #Max temp group by fips code
mean_temp = weather_df.groupby(by=["fips_code"]).mean() #mean temp group by fips code
total_precipitation = weather_df.groupby(by=["fips_code"]).sum() #total precipitation

#API was not able to find any countries given the lat and lon values. Below is my attempt

# field_list = crop_df['field_geometry'].tolist()
# for item in field_list: 
#     lat = item.split(",")[0].split("(((")[1].split(" ")[0] #Split to get the latitude and longitude values
#     lon = item.split(",")[0].split("(((")[1].split(" ")[1]
#     url = 'https://geo.fcc.gov/api/census/block/find?latitude=%s&longitude=%s&censusYear=2020&format=json' % (lat, lon)
#     response = session.get(url)
#     data = response.json()



min_temp_list = min_temp['temp'].tolist()
fips_code_list = min_temp.index.tolist()
max_temp_list = max_temp['temp'].tolist()
mean_temp_list = mean_temp['temp'].tolist()
total_precipitation_list = total_precipitation['precip'].tolist()
combined_lists  = list(zip(fips_code_list, total_precipitation_list, min_temp_list,max_temp_list, mean_temp_list)) #combining lists to format a new dataframe of all the results
final_weather_df = pd.DataFrame(combined_lists, columns = ['fips_code', 'precip', 'min_temp',
'max_temp', 'mean_temp'])
final_weather_df.to_csv('Q4.csv')

