"""
	Author: Madhivarman
	contact: madhi@pluto7.com
	Project: Customer Segmentation
	Version: 1.0
	File Description: To do Cluster Analysis

	Tutorial Process: http://madhugnadig.com/articles/machine-learning/2017/03/04/implementing-k-means-clustering-from-scratch-in-python.html
"""

class ClusterAnalysis:
	"""
		Initial function: (Args)
			Cluster_number: total number of clusters,
			epochs: Number of epochs the model should run,
			model_name: describe model name,
			bs: batch size
			tolerance: when the difference between the old and new centroid is less than tolerance value, stop the further iteration
			data: X data
	"""
	def __init__(self, cluster_number, epochs, modelname, tolerance, data):
		self.no_of_clusters = cluster_number
		self.epochs = epochs
		self.modelname = modelname
		self.tolerance = tolerance
		self.X = data
		self.centroids = {} #dict to store the Centroids
		self.classes = {}

	#custom function to train the Kmeans clustering for the data
	def fit(self):
		#Numerical library for Mathematical calculations
		import numpy as np 
		"""
			Distance metric(Eucledian Distance): Eucledian Distance metric is used
		"""
		print("Started Clustering the Data")

		for i in range(self.no_of_clusters):
			self.centroids[i] = self.X[i] #randomly assign the data
			
			#begin the iterations
		for i in range(self.epochs):
			"""
				 Variables:
				  	self.classes (list): Represents what data belongs to what class
			"""
			for i in range(self.no_of_clusters):
				self.classes[i] = []

			#find the distance between the point and cluster; choose the nearest centroid
			for features in self.X:
				#calculate distance metric of the data to the centroid points
				distance = [np.linalg.norm(features - self.centroids[centroid]) for centroid in self.centroids]
				classification = distance.index(min(distance)) #get the minimum distance
				self.classes[classification].append(features) #append the data to that particular class

			previous = dict(self.centroids)

			for classification in self.classes:
				self.centroids[classification] = np.average(self.classes[classification], axis=0)

			isOptimal = True

			for centroid in self.centroids:

				original_centroid = previous[centroid]
				curr = self.centroids[centroid]

				if np.sum((curr - original_centroid)/original_centroid * 100.0) > self.tolerance:
					isOptimal = False

			#if the point reaches it optimal position break the loop
			if isOptimal:
				print("Cluster Centroids:{}".format(self.centroids))
				break 
