"""
	Author: Madhivarman
	contact: madhi@pluto7.com
	Project: Customer Segmentation
	Version: 1.0
"""
import sys
sys.path.append('F:/work projects/Dash Application')

import pandas as pd 
import io
import numpy as np

from Cloud_API.storage import Storage
from cluster_analysis import ClusterAnalysis

class GetData():
	def __init__(self, input_data):
		self.input_data = input_data
		self.shape = self.input_data.shape
		self.column_values = self.input_data.columns.values

def convert_data_into_bytes(data):
	"""
		Args:
			data(byte): input_data
		Return:
			Byte data properly converted to CSV FILE
	"""
	converted_data = pd.read_csv(io.BytesIO(data), encoding='utf-8')
	return converted_data

#custom function to find the min max function
def find_min_max(recency, monetary, frequency):
	"""
		Args:
			Each object has:
				centroids, classes, X
			centroids(dictionary): {"Cluster ID": Data Points}

		Return: 
			Data Type (Dictionary): {"Key":{"cluster ID": [min, max]}}
	"""
	def min_max(data_dict):
		ids, value = [], []
		for key, values in data_dict.items():
			ids.append(key)
			value.append([min(values), max(values)])

		return {'Cluster ID': ids, 'Values': value}


	r_centroids_and_features = min_max(recency.classes) #return as dictionaries
	m_centroids_and_features = min_max(monetary.classes)
	f_centroids_and_features = min_max(frequency.classes)

	print(r_centroids_and_features)
	print(m_centroids_and_features)
	print(f_centroids_and_features)

	return {'recencey': r_centroids_and_features,
			'monetary': m_centroids_and_features,
			'frequency': f_centroids_and_features}

def save_as_json(data,Filename):
	import json
	with open('dumps/{}'.format(Filename), "w") as fp:
		json.dump(data,fp, sort_keys=True, indent=4)

def main():
	storage = Storage()

	input_data_download = input("Enter the Filename: ")
	downloaded_data = storage.download_blob(input_data_download)

	proper_csv_format = convert_data_into_bytes(downloaded_data)

	#object for storing the data
	input_obj = GetData(proper_csv_format)

	recency_obj = ClusterAnalysis(5, 500, 'Recency_Cluster_Analysis', 0.0001, input_obj.input_data['Recency'])
	recency_obj.fit() #return as dictionary

	monetary_obj = ClusterAnalysis(5, 500, 'Monetary_Cluster_Analysis', 0.0001, input_obj.input_data['Monetary'])
	monetary_obj.fit() #return as dictionary

	frequency_obj = ClusterAnalysis(5, 500, 'Frequency_Cluster_Analysis', 0.0001, input_obj.input_data['Frequency'])
	frequency_obj.fit() #return as dictionary

	#now find the min-max for each cluster
	#type as dictionary
	min_max = find_min_max(recency_obj, monetary_obj, frequency_obj)
	
	#save as json file
	save_as_json(min_max, input_data_download.split('.')[0]+".json")

if __name__ == '__main__':
	main()