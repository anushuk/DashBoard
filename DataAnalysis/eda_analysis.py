"""
    Author: Madhivarman
    contact: madhi@pluto7.com
    Project: customer Segmentation
    Version: 1.0
    File Purpose: Data Analysis on the data

"""
import pandas as pd
import matplotlib.pyplot as plt #visualization
import seaborn as sns #modern visualization
import sys 
import io

sys.path.append('F://work projects/customer_segmentation')
from Cloud_API.storage import Storage #to download the data from the bucket
from color import bcolors
from find_outliers import OutlierRules
from ClusterAnalysis.cluster_analysis import ClusterAnalysis #to do the cluster Analysis
from pie_chart import PieChart

""" Declaring Class for Exploratory Data Analysis """
class EDA:
    """ initial function: load all the Variables when this class is Called. """
    def __init__(self, input_data):
        self.input_data = input_data
        self.shape = self.input_data.shape
        print("The Shape of the Dataset is:{ds_shape}".format(ds_shape=self.shape))
        print("*"*50)
        self.column_values = self.input_data.columns.values

    """ Custom function to load the data """
    def get_info_about_data(self):
        """
            Return: info about the dataframe
        """
        info_about_the_data = self.input_data.info()

        return info_about_the_data

    def get_the_attribute_data(self):
        """
            Returns: recency, monetary, frequency
        """
        recency = self.input_data["Recency"]
        monetary = self.input_data["Monetary"]
        frequency = self.input_data["Frequency"]

        return recency, monetary, frequency

    def EDA(self):

        """Exploratory Data Analysis is Done here"""

        #custome function made here
        def check_if_the_input_data_has_index():
            index_column_present = False

            if "Unnamed: 0" in self.column_values:
                index_column_present = True
                return index_column_present

            else:
                return index_column_present

        def check_all_figures_are_stored(path,name):
            import os
            no_of_figs = os.listdir(path)

            return "Total {l} are stored in the {dir} directory".format(l=len(no_of_figs), dir=name)

        def univariate_analysis():
            """
                Description:
                    Find distribution of the data attributes. In our case {"recency","monetary","frequency"}
                    Summary statistics
                Returns:
                    Summary Statistics of the data, 
                    Statistics visualization
            """
            path = "F:/work projects/customer_segmentation/DataAnalysis/visualizations/Distributions/"
            def create_a_distribution_data(data, name, name_to_save_image):
                """
                    Args:
                        data: dataframe.values
                        name: xlabel name
                        name_to_save_image: figure have to be saved in this name

                    Return:
                        Figure address, Successfull Message
                """
                sns.set(color_codes=True)
                ax = sns.distplot(data, kde=True, rug=False)
                ax.set(xlabel=name)
                plt.savefig(path + "{image_name}.png".format(image_name = name_to_save_image))

                return ax, "Image is Sucessfully Saved to the Path."

            
            recency_data, monetary_data, frequency_data = self.get_the_attribute_data()

            fig_1, msg = create_a_distribution_data(recency_data,"Recency Distribution", "Recency_Distribution_Figure")
            fig_2, msg = create_a_distribution_data(frequency_data, "Frequency Distribution", "Frequency_Distribution_Figure")
            fig_3, msg = create_a_distribution_data(monetary_data, "Monetary Distribution", "Monetary_Distribution_Figure")

            #last custom function
            #FYI to know how many figures are stored in the folder
            figure_notification = check_all_figures_are_stored(path, "Distributions")
            
            return figure_notification

        def find_the_outlier_in_the_data():
            """
                Finding the outliers in the data using Box plot.
            """
            path = "F:/work projects/customer_segmentation/DataAnalysis/visualizations/Outlier Visualizations/"

            #custom function
            def getting_box_plot(data, name, name_to_save_image):
                sns.set(color_codes=True)
                ax = sns.boxplot(data)
                ax.set(xlabel=name)

                plt.savefig(path + "{image_name}.png".format(image_name = name_to_save_image))

                return ax

            #function to remove the outliers in the data
            def get_input_data_without_outliers(outlier_data):
                """
                    Args:
                        outlier_data(list): data which are considered as outliers

                    Return:
                        input_df(dataframe): input_dataframe after removing the outliers
                """
                dup_dataframe = self.input_data
                outlier_data_index = dup_dataframe.index[dup_dataframe['Recency'] == outlier_data].tolist()

                #now drop the outliers in the dataframe
                dup_dataframe = dup_dataframe.drop(outlier_data_index)

                return dup_dataframe

            recency_outlier, monetary_outlier, frequency_outlier = self.get_the_attribute_data()

            outlier_fig1 = getting_box_plot(recency_outlier, "Recency Outlier", "Recency_Outlier_Figure")
            outlier_fig2 = getting_box_plot(monetary_outlier, "Monetary_Outlier", "Monetary_Outlier_Figure")
            outlier_fig3 = getting_box_plot(frequency_outlier, "frequency_outlier", "Frequency_Outlier_Figure")

            outlier_notification = check_all_figures_are_stored(path, "Outlier Visualizations")

            return outlier_notification




        #initially check if the input dataframe has a index column
        check_index_column = check_if_the_input_data_has_index()

        if check_index_column:
            self.input_data = self.input_data.drop([self.column_values[0]], axis=1) #drop the column value
            self.shape = self.input_data.shape #change the shape of the dataset

        #Univariate Analysis
        uni_figure_notification= univariate_analysis()
        print(uni_figure_notification)
        print("." * 50)

        #finding the outlier of the data
        outlier_data = find_the_outlier_in_the_data()
        print(outlier_data)
        print("." * 50)

        #now get the mean and std-deviation score from the find_outliers.py file
        outlier_obj = OutlierRules(self.input_data)
        #returns the list data with the outliers list
        outlier_data = outlier_obj.find_outliers()
        print("There are {total} outliers in the dataset".format(total = len(outlier_data)))

        """
        Standard Deviation of above three attributes is almost same
        for reference: https://machinelearningmastery.com/how-to-use-statistics-to-identify-outliers-in-data/

        """
        #get index number of the data in the dataset
        if len(outlier_data) == 0:
            print("There is Zero Ouliers in the input data")
        else:
            #Update the input dataframe
            self.input_data = get_input_data_without_outliers(outlier_data)

        """ 
            Cluster Analysis Code Starts here
        """
        print("*" * 50)

        recency_obj = ClusterAnalysis(5, 500, 'Recency_Cluster_Analysis', 0.0001, self.input_data['Recency'])
        recency_obj.fit()
        vis_recency_obj = PieChart(recency_obj.classes, recency_obj.X, recency_obj.modelname)
        vis_recency_obj.visualize()

        monetary_obj = ClusterAnalysis(5, 500, 'Monetary_Cluster_Analysis', 0.0001, self.input_data['Monetary'])
        monetary_obj.fit()
        vis_monetary_obj = PieChart(monetary_obj.classes, monetary_obj.X, monetary_obj.modelname)
        vis_monetary_obj.visualize()

        frequency_obj = ClusterAnalysis(5, 500, 'Frequency_Cluster_Analysis', 0.0001, self.input_data['Frequency'])
        frequency_obj.fit()
        vis_freq_obj = PieChart(frequency_obj.classes, frequency_obj.X, frequency_obj.modelname)
        vis_freq_obj.visualize()


#custom function 
def main():

    #custom function to change the format of the data
    def convert_byte_to_csv(data):
        """
            Args:
                data(byte): input data
            Return:
                Byte data properly converted to CSV file
        """
        converted_data = pd.read_csv(io.BytesIO(data), encoding='utf-8')
        return converted_data, "Data is Successfully Converted!!!"


    #create an object for calling Storage API
    obj_for_storage = Storage()
    #download the input data from the storage
    input_data_download = input("Enter the Filename to download the data from the bucket: ")
    downloaded_data = obj_for_storage.download_blob(input_data_download) #return the data as class <Byte>
    
    #convert the Byte data to proper csv file
    proper_csv_format,msg = convert_byte_to_csv(downloaded_data)
    print(msg+"\n"+"." * 50)

    #create object for EDA class
    obj_for_EDA = EDA(proper_csv_format)

    choice_about_info = input("Do you want to see the full information about the data:[Y/n]?" )
    
    if choice_about_info == 'Y':
        about_the_data = obj_for_EDA.get_info_about_data()

    #analysis part start here
    obj_for_dataanalysis = obj_for_EDA.EDA()

if __name__ == '__main__':
    main() #main file to do the exploratory data analysis
