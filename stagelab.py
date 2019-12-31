from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning



disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
client, service, history = open_connection() # Open connection using connect.py



def stage_regions():
    # Create Blank Region Dictionary
    # region_matrix = {}
    try:
        # Create initial hardcoded Regions List to test with
        base_region_list = ['CLX_R','SBC_CLx_R','BROADCAST_CLx_R']
        
        # Create the new regions from hardcoded region list
        for region_name in base_region_list:
            print (f"\nCreating new region named {region_name}...")
            service.addRegion(region={"name": region_name})
            # Store the returned uuids not needed.
            # Will query when needed at runtime in each script.
            # region_uuid = resp['return']
            # region_uuid = region_uuid.strip("{}").lower()
            # print(f"New region uuid: {region_uuid}")
            # region_matrix.update({region_name:region_uuid})
            print (f"Region {region_name} successfully created.")
        print(f"\nDONE!\n")


    except Fault as err:
        print(f'Error Inserting Region: {err}')
