import sys
sys.path.append('F://work projects/Dash Application')
from Cloud_API.storage import Storage
from Cloud_API.datastore import DataStore

#import necessary libraries
import csv
import datetime
import pandas as pd
import io
#custom function
def upload_into_datastore(df):
	#get the dataframe values as list
	unique_id = df.Unique_Id.tolist() 
	r = df.Recency.tolist()
	m = df.Monetary.tolist()
	f = df.Frequency.tolist()

	zipped_data = zip(unique_id, r, m, f)

	#Create an object for Datastore
	datastore = Datastore()
	#to insert the data into datastore
	i=1
	multi_data_entry = [] #list to store the data

	print("Data is Ready to Upload into DataStore!!!")
	print("*" * 75)

	for uniq_id, r, m, f in zipped_data:
		#calling the function
		entry = datastore.insert(uniq_id, r, m, f)
		multi_data_entry.append(entry)

		if len(multi_data_entry) == 500:
			#push multiple data  into the datastore
			print("Batch Data is Uploading Now!!")

			#[START datastore_batch_upsert]
			datastore.client.put_multi(multi_data_entry)
			#[END datastore_batch_upser]

			multi_data_entry = [] #clear the list

			print("{} Batch is Uploaded into DataStore".format(500 *  i))
			i += 1
			print("-" * 75)


	return "Data is Successfully Uploaded into DataStore"


def dataflow(option_for_run_local):

	if option_for_run_local:
		input_file_path = 'inputs/input_data.csv'
	else:
		Obj_for_Storage = Storage()
		downloaded_file = Obj_for_Storage.download_blob('input_data.csv')
		csv_format = pd.read_csv(io.BytesIO(downloaded_file), encoding='utf-8')

		start_time = datetime.datetime.now().strftime('%H:%M:%S')

		msg = upload_into_datastore(csv_format)

		end_time = datetime.datetime.now().strftime('%H:%M:%S')

		print("Starting Time:{}, Ending Time:{}".format(start_time, end_time))



if __name__ == '__main__':
	run_locally = False
	dataflow(run_locally)