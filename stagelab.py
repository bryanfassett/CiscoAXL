from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning



disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
client, service, history = open_connection() # Open connection using connect.py

def add_staged_regions():
    # Region Name:  Region uuid
    region_list = ['CLX_R','SBC_CLx_R','BROADCAST_CLx_R']

    # Create the new regions from hardcoded region list
    for region_name in region_list:
        print (f"Creating new region named {region_name}...")
        resp = service.addRegion(region={"name": region_name})
        # Store the returned uuids for later
        region_uuid = resp['return']
    region_uuid = region_uuid.strip("{}").lower()
    print(f"New region uuid: {region_uuid}")

def update_region_matrix
# Create a Dictionary of all regions to create a relationship with the new region
region_matrix = {
    # Region Name:  Region uuid
    'CLx_R': '3a2eb8c1-7f22-dd9e-dfee-ff6179034c57',
    'SBC_CLx_R':'648e7571-a570-59ae-305c-ca3f1ab73776',
    'BROADCAST_CLx_R': 'e6efbe6c-5038-1ab8-a3ff-8f18188612d9'
}


    print('Regions successfully created.')
except Fault as err:
    print(f'Error Inserting Region: {err}')