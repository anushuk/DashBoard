"""
	Author: Madhivarman 
	contact: madhi@pluto7.com
	Project: Customer Segmentation
	Version: 1.0
	File Description: 
		Calculating the outliers and segment the data
		Recency determines How recent the customer often purchased
                Monetary determines How much the customer Spends on the product. For example: 10,000 rupees on the data
                Frequency determines How often the customer purchase. For example: how many times customer have purchased. 
"""

class OutlierRules:
    
    #initial function  to load the dataframe
    def __init__(self, data):
        self.input_dataframe = data

    """
        A function to find the outliers and label the data as outlier.
        Method: A Rule based approach to state that the data is outliered.
    """
    def find_outlier_score(self):
        """
            calculating 'Mean' and 'Standard Deviation' of the data. 
            And consider all the value which deviated from "Mean_value (+-) Standard Deviation"
        """
        import numpy as np
        data_to_find_outliers = self.input_dataframe
        mean_for_recency, std_for_recency = np.mean(data_to_find_outliers['Recency']), np.std(data_to_find_outliers['Recency'])
        mean_for_monetary, std_for_monetary = np.mean(data_to_find_outliers['Monetary']), np.std(data_to_find_outliers['Monetary'])
        mean_for_frequency, std_for_frequency = np.mean(data_to_find_outliers['Frequency']), np.std(data_to_find_outliers['Frequency'])

        #now zip the data
        scores = zip([mean_for_recency, mean_for_monetary, mean_for_recency],[std_for_recency, std_for_monetary, std_for_frequency])

        return scores

    def find_outliers(self):
        import numpy as np
        #custom function for returning mean,std value
        def mean_std_value(zip_data):
            """
                Args:
                    zip_data : Zipped data of mean and standard deviation

                Returns:
                    outliers list
            """
            m, s = [],[]

            for (mean, std) in zip_data:
                m.append(mean)
                s.append(std)

            return m,s

        scores= self.find_outlier_score()
        mean, std  = mean_std_value(scores)

        #find the cutoff value
        cutoff = std[0] *  3
        lower, upper = np.array(mean) - cutoff, np.array(mean) + cutoff
        
        """
            Return Type:
                lower(lower cut off value) - numpy.ndarray
                upper(upper cut off value) - numpy.ndarray
        """
        #find the outliers and remove from the dataset
        recency_outliers = [x for x in self.input_dataframe['Recency'] if x < lower[0] and x > upper[0]]

        return recency_outliers


