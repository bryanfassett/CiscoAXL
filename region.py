from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from stagelab import stage_regions

# Create a Dictionary of all regions to create a relationship with the new region
#region_matrix = {
#   # Region Name:  Region uuid
#   'CLx_R': '3a2eb8c1-7f22-dd9e-dfee-ff6179034c57',
#   'SBC_CLx_R':'648e7571-a570-59ae-305c-ca3f1ab73776',
#    'BROADCAST_CLx_R': 'e6efbe6c-5038-1ab8-a3ff-8f18188612d9'
#}

disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
client, service, history = open_connection() # Open connection using connect.py

# Get name of the new region
print("Enter new region name:")
region_name= input() # wait for input
print (f"\nCreating new region named {region_name}...")

# Create new region and store uuid
try:
    # Create the new region
    resp = service.addRegion(region={"name": region_name})

    # Store the returned uuid for later
    region_uuid = resp['return']
    region_uuid = region_uuid.strip("{}").lower()
    print(f"New region uuid: {region_uuid}")

    # Loop through dictionary and run insert statement for each key (informix DB can't do values listing...)
    for region in region_matrix:
        sql_stmt = '''
            INSERT INTO regionmatrix (fkregion_a, fkregion_b, videobandwidth, fkcodeclist, immersivebandwidth, audiobandwidth)
            VALUES ('{new_uuid}', '{target_uuid}', 384, '22910f2b-51ab-4a46-b606-604a28558568', -2, 64)
        '''.format(
                new_uuid = region_uuid,
                target_uuid = region_matrix[region]
            )
        
        resp = service.executeSQLUpdate(sql_stmt)

    print('Region successfully created.')
except Fault as err:
    print(f'Error Inserting Region: {err}')