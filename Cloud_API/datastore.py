from google.cloud import datastore
import google.cloud.exceptions
from settings import PROJECT
import datetime
from collections import defaultdict

class Datastore():

	#initial function declaration
	def __init__(self):
		self.client = datastore.Client(PROJECT)
		self.timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d')
		self.kind_name = 'segmentData'

	#custom function to retrieve all entities here.
	def retrieve_all_entities(self):
		query = self.client.query(kind=self.kind_name)
		all_keys = query.fetch() #fetches all the entities from the datastore

		kinds, recency, monetary, frequency = [] , [], [], []

		for keys in all_keys:
			kinds.append(keys.key.id_or_name)
			recency.append(keys['Recency'])
			monetary.append(keys['Monetarty'])
			frequency.append(keys['Frequency'])

		return kinds, recency, monetary, frequency

	def get_total_entries(self):
		query = self.client.query(kind= self.kind_name)
		all_keys = query.fetch()
		total_len = len(list(all_keys)) #to get total number of rows in the datastore

		return total_len

	#to insert the data objects to the datastore
	def insert(self, Unique_Id, r, m, f, snapshot_Id):
		#[Start Datastore Insert]
		with self.client.transaction():

			incomplete_key = self.client.key('segmentData', str(Unique_Id)+"."+self.snapshotid)

			task = datastore.Entity(key = incomplete_key)

			task.update({
				'Unique_Id': Unique_Id,
				'Recency': r,
				'Monetary': m,
				'Frequency': f,
				'snapshot_Id': snapshot_Id
			})

			return task

	#to do bulk insert
	def bulk_insert(self, values_as_list):

		#[Start Bulk Insert in Datastore]
		self.client.put_multi(values_as_list)
		return "Snapshot Are Successfuly Uploaded to Datastore"

	#to get all Key entites from the datastore
	def get_all_uid(self):
		#[Start returnig all unique_id and key function]
		query = self.client.query(kind=self.kind_name)
		all_keys = query.fetch() #fetches all entities from the datastore

		keys = [entities.key.id_or_name for entities in all_keys]

		return keys
		#[End the function]

	#to get distinct id from the datastore object
	def get_distinct_id(self):
		#[Start getting the distinct id]
		query = self.client.query(kind=self.kind_name)
		all_keys = query.fetch()
		snapshot_ids = []

		for keys in all_keys:
			snapshot_ids.append(keys['snapshot_Id'])

		distinct_ids = set(snapshot_ids)

		#return as list
		return list(distinct_ids)
		#[End]


	#to get the objects by applying filters in the data entities
	def property_filter(self, property_name, value):

		#[Start datastore_property_filter]
		query = self.client.query(kind= self.kind_name)
		query.add_filter (property_name, '=',  value)

		attr = query.fetch()
		uid, r, m, f = [], [], [], []

		for k in attr:
			uid.append(k['Unique_Id'])
			r.append(k['Recency'])
			m.append(k['Monetarty'])
			f.append(k['Frequency'])

		#return as list
		return uid, r, m, f

	#do the batch lookup
	def batch_lookup(self, property, snapshot_ids):
		#[START batch lookup]
		#append the property with snapshot_ids to do batchlookups
		keys = []
		key_Name = [] #now it has keyname.entities

		#do some preprocessing here
		#because we need key entity as UniqueId.SnapshotDate

		snapshot_date = []

		for ids in snapshot_ids:
			d = ids.split('_')[1]
			snapshot_date.append(d)

		for date in snapshot_date:
			key_Name.append(property + "." + date)

		for kname in key_Name:
			keys.append(self.client.key('segmentData',kname))

		#[START datastore_batch_lookup]
		tasks = self.client.get_multi(keys)
		#[END datastore_batch_lookups]

		#return as lists
		return tasks

	#to get summary statistics about the project
	def get_summary_statistics(self):
		#[START getting the Summary Statistics]
		stats = self.client.query(kind= self.kind_name)
		overall_stats = stats.__Stat_Total__ ()

		return overall_stats
		#[END]