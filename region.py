from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import json

# Create a Dictionary of all regions to create a relationship with the new region
#region_matrix = {
#   # Region Name:  Region uuid
#   'CLx_R': '3a2eb8c1-7f22-dd9e-dfee-ff6179034c57',
#   'SBC_CLx_R':'648e7571-a570-59ae-305c-ca3f1ab73776',
#    'BROADCAST_CLx_R': 'e6efbe6c-5038-1ab8-a3ff-8f18188612d9'
#}

disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
client, service, history = open_connection() # Open connection using connect.py

# Attempting to pull the uuids for each Region in the base Region List
try:
    # Creating the base Region List
    base_region_list = ['CLX_R','SBC_CLx_R','BROADCAST_CLx_R']
    # Creating an empty region_dict to hold the Region name and uuid results, maybe not needed since I can create it during the for loop
    region_dict = {}

    for region_name in base_region_list:
        getRegResp = service.getRegion(name = region_name)
        #NO IDEA... I don't know the syntax of .getRegion and don't know what is returned
        #json_string = str(getRegResp['return'])
        #region_dict = json.loads(json_string)
        region_name = getRegResp['return']['region']['name']
        region_uuid = getRegResp['return']['region']['uuid']
        region_uuid = region_uuid.strip("{}").lower()
        print ("Adding " + region_name + ", " + region_uuid + " to the dictionary")
        region_dict[region_name]=region_uuid
    print (region_dict)


except Fault as err:
    print(f'Error Building Region UUID Dictionary: {err}')



#Get name of the new region
print("Enter new region name:")
new_region_name= input() # wait for input
print (f"\nCreating new region named {new_region_name}...")

 
# Create new region and store uuid
try:
    # Create the new region
    resp = service.addRegion(region={"name": new_region_name})

    # Store the returned uuid for later
    new_region_uuid = resp['return']
    new_region_uuid = region_uuid.strip("{}").lower()
    print(f"New region uuid: {new_region_uuid}")

    # Loop through dictionary and run insert statement for each key (informix DB can't do values listing...)
    for region_uuid in region_dict:
        sql_stmt = '''
        INSERT INTO regionmatrix (fkregion_a, fkregion_b, videobandwidth, fkcodeclist, immersivebandwidth, audiobandwidth)
        VALUES ('{target_uuid}', '{new_uuid}', 384, '22910f2b-51ab-4a46-b606-604a28558568', -2, 64)
        '''.format(
        new_uuid = region_dict[region_uuid],
        target_uuid = new_region_uuid
        )
        
        resp = service.executeSQLUpdate(sql_stmt)

        print('Relationships successfully created.')
except Fault as err:
    print(f'Error Inserting Region: {err}')