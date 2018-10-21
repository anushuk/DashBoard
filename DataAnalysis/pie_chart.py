import matplotlib.pyplot as plt 
from matplotlib import style
style.use('ggplot')

class PieChart():
	def __init__(self, classes, data, name):
		self.classes = classes
		self.X = data
		self.modelname = name

	def visualize(self):
		cluster_id, percentage = [], []
		explode = (0,0.1,0.1,0.1,0.1)

		for classification in self.classes:
			cluster_id.append(classification)
			percentage_value = ((len(self.classes[classification]) / len(self.X))) * 100
			percentage.append(percentage_value)

		plt.pie(percentage, labels=cluster_id, explode=explode, autopct='%1.0f%%', shadow=True)
		file_path = "F:/work projects/customer_segmentation/DataAnalysis/visualizations/Cluster_Analysis/"
		plt.savefig(file_path+"{}.png".format(self.modelname))
		plt.clf() #clear the figure
