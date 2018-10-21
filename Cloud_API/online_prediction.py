"""
    author: Madhivarman
    contact: madhi@pluto7.com
    Project: Customer Segmentation
    Version: 1.0

"""
import os
import googleapiclient.discovery
from google.cloud import storage

class Prediction():

	def __init__(self):

		self.project_id = 'gcp-de-exp'
		os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../google-credentials/application_default_credentials.json'
		self.storage_client = storage.Client(self.project_id)
		self.model_name = 'CustomerSegmentationTensorflowEstimator'
		self.version = 'CS_03'

	def get_online_predictions(self, data_file):
	    """
	        Send json daata to a deployed model for predictions.
	        
	        Args:
	            project(str): project where the cloud ML is deployed
	            model(str): model name
	            data_file(str): prediction data file
	                    Keys should be the name of your deployed model expects as inputs. Values should 
	                    be convertible to Tensors, or (potentially nested) listed convertible to tensors.
	            version(str): version of the model to target.

	        Returns:
	            Mapping[str:any]: dictionary of prediction results defined by the model.
	    """
	    service = googleapiclient.discovery.build('ml', 'v1')
	    name = 'projects/{project_name}/models/{model_name}'.format(project_name=self.project_id, model_name=self.model_name)

	    if self.version is not None:
	        name +=  '/versions/{}'.format(self.version)

	    response = service.projects().predict(
	            name = name,
	            body = {'instances': [{"renancy":7.0,"freq":5.0,"monetary":6.0},{"renancy":9.0,"freq":6.0,"monetary":8.0}]}
	    ).execute()

	    if 'error' in response:
	        raise RuntimeError(response['error'])

	    return response['predictions']