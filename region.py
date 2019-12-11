from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# Create a Dictionary of all regions to create a relationship with the new region
region_matrix = {
    # Region Name:  Region uuid
    'CLx_R': 'e80815d6-da74-033c-6294-d6fce4fc7da9',
    'SBC_CLx_R':'138bb056-38bf-956a-7a54-e1d122521e6a',
    'BROADCAST_CLx_R': '09835766-1838-9229-faff-bdda583af704'
}

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