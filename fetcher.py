#!/usr/bin/python3
import pandas as pd
import requests
import json
from datetime import datetime,date
from pytz import timezone
from csv import writer
from os.path import exists

def fetch_latest():
	with open('data-2024-04-20.log','r') as f:
		data = f.readlines()
	parsed_data = [json.loads(lines) for lines in data]
	data_dict = {}
	for data in parsed_data:
		for key, value in data.items():
			if key not in data_dict:
				data_dict[key] = [value]
			else:
				data_dict[key].append(value)

	df_new = pd.json_normalize(data_dict,record_path=['message'])
	df_new['date'] = df_new['date'].str.replace(',','')
	df_new['date'] = pd.to_datetime(df_new['date'])
	df_new['long'] = df_new['long'].astype(float)
	df_new['lat'] = df_new['lat'].astype(float)
	df_new['speed'] = df_new['speed'].astype(float)

	latencylist = [0]
	# if exists('errors-'+str(date.today())+'.csv'):
	# 	with open('errors-'+str(date.today())+'.csv','a') as f:
	# 		pd.to_datetime(df_new['date'])
	# 		d = []
	# 		for i in range(len(df_new.index)-1):
	# 			diff = (df_new['date'][i+1]-df_new['date'][i]).total_seconds()
	# 			latencylist.append(diff)
	# 			if latencylist[i]>10:
	# 				d.append(df_new['date'][i])
	# 				d.append(df_new['lat'][i])
	# 				d.append(df_new['long'][i])
	# 				d.append(df_new['speed'][i])
	# 				d.append(latencylist[i])
	# 				with open('errors-'+str(date.today())+'.csv','a') as f:
	# 					write = writer(f)
	# 					write.writerow(d)
	# 					d = []
	# 					f.close()
	# else:
	with open('errors-'+str(date.today())+'.csv','w') as f:
		write = writer(f)
		write.writerow(['timestamp','latitude','longitude','speed','latency'])
		f.close()
		pd.to_datetime(df_new['date'])
		d = []
		for i in range(len(df_new.index)-1):
			diff = (df_new['date'][i+1]-df_new['date'][i]).total_seconds()
			latencylist.append(diff)
			if latencylist[i]>10:
				d.append(df_new['date'][i])
				d.append(df_new['lat'][i])
				d.append(df_new['long'][i])
				d.append(df_new['speed'][i])
				d.append(latencylist[i])
				with open('errors-'+str(date.today())+'.csv','a') as f:
					write = writer(f)
					write.writerow(d)
					d = []
					f.close()
	print("Successfully Written Error Logs")

	# if exists('log-'+str(date.today())+'.csv'):
	# 	with open("log-"+str(date.today())+'.csv','a') as f:
	# 		d=[]
	# 		for i in range(len(df_new.index)):
	# 			d.append(df_new['date'][i])
	# 			d.append(df_new['lat'][i])
	# 			d.append(df_new['long'][i])
	# 			d.append(df_new['speed'][i])
	# 			d.append(latencylist[i])
	# 			with open("log-"+str(date.today())+'.csv','a') as f:
	# 				write = writer(f)
	# 				write.writerow(d)
	# 				d = []
	# 				f.close()
	# else:
	with open("log-"+str(date.today())+".csv",'w') as f:
		d=[]
		write = writer(f)
		write.writerow(['timestamp','latitude','longitude','speed','latency'])
		f.close()
		for i in range(len(df_new.index)):
				d.append(df_new['date'][i])
				d.append(df_new['lat'][i])
				d.append(df_new['long'][i])
				d.append(df_new['speed'][i])
				d.append(latencylist[i])
				with open("log-"+str(date.today())+".csv",'a') as f:
					write = writer(f)
					write.writerow(d)
					d=[]
					f.close()
	print("Successfully Written Logs")
