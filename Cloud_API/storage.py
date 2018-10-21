"""
    author: Madhivarman
    contact: madhi@pluto7.com
    Project: Customer Segmentation
    Version: 1.0

"""
import pandas as pd 
import numpy as np 
import os
from google.cloud import storage



class Storage():

	def __init__(self):

		self.gcp_project_id = 'GOOGLE-CLOUD-PROJECT-ID'
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'PATH_TO_CREDENTIALS'
		self.storage_client = storage.Client(self.gcp_project_id)
		self.bucket_name = "customer_segmentation_input_data"
		self.prediction_bucket_name = "cs_prediction_data"

	def download_blob(self, source_file_name):
	    """download a blob from the bucket"""
	    bucket = self.storage_client.get_bucket(self.bucket_name)
	    blob = bucket.get_blob(source_file_name)
	    file_contents = blob.download_as_string() #read the content from the storage

	    return file_contents

	#custom function to get the file details
	def get_file_details(self, source_file_name):
		"""
			Args:
				source_file_name: Input filename

			Return:
				storage_class, name, size, updated, file_type
		"""
		bucket = self.storage_client.get_bucket(self.bucket_name)
		storage_class = bucket.storage_class

		name, size, updated, generation,md5hash = [], [], [], [], []

		for blob in bucket.list_blobs():
			name.append(blob.name)
			size.append(blob.size)
			updated.append(blob.updated)
			generation.append(blob.generation)
			md5hash.append(blob.md5_hash)

		Zip_bucket_data =  zip(name, size, updated, generation, md5hash)

		f_size, f_modified, f_generation, f_md5hash = None, None, None, None

		for file_info in Zip_bucket_data:
			#write the condition
			if file_info[0] == source_file_name:
				f_size = file_info[1]
				f_modified = file_info[2]
				f_generation = file_info[3]
				f_md5hash = file_info[4]

				break

		#update the dictionary
		info_about_data = {
			'Storage Class': storage_class,
			'Size': str(f_size) + " Bytes",
			'Last Modified':f_modified.strftime('%d/%m/%Y'),
			'Generation': f_generation,
			'Md5Hash': f_md5hash
		}

		return info_about_data


	def convert_the_data_to_serialize_format(self, prediction_data):
	    """
	        load the json library

	        Args:
	            prediction_data(byte): data read from the storage bucket

	        Return:
	            real json formatted data
	    """
	    import json
	    real_json = prediction_data.decode("utf8")

	    return real_json

	#upload the input file data to the bucket
	def upload_input_blob_to_the_bucket(self, filename):
	    """
	        Args:
	            filename: input file to be uploaded
	            bucket_name: Bucket name to store the file
	        Returns:
	            return message if the file is uploaded successfully
	    """
	    bucket = self.storage_client.get_bucket(self.bucket_name)
	    blob = bucket.blob(filename)
	    blob.upload_from_filename(filename)

	    return  "File is Uploaded to the Bucket!!!!"

	#upload the prediction data to the bucket
	def upload_blob_to_the_bucket(self,prediction_data):
	    """
	        Args:
	            prediction_data(list): JSON data result
	            bucket_name(str): Bucket name to store the json data

	        RETURN:
	            show the message if the file is uploaded successfully
	    """
	    source_file_name = 'predicted_test_data.json'
	    #custom function to write the predicted data as json file
	    def write_as_json_file(result_to_write):
	        import json
	        filename = 'prediction_output.json'
	        with open(filename, 'w') as json_file:
	            json.dump(result_to_write, json_file)

	        return filename

	    as_json_file = write_as_json_file(prediction_data) # write as json file
	    bucket = self.storage_client.get_bucket(self.prediction_bucket_name) #get the bucket name
	    blob = bucket.blob(source_file_name) #as blob
	    
	    blob.upload_from_filename(as_json_file) #upload the blob
	    
	    return  "Blob is Successfully uploaded to the Bucket"
