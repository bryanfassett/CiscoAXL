from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
client, service, history = open_connection() # Open connection using connect.py

# Attempting to pull the uuids for each Region in the base Region List
try:
    # Creating the base Region List Hardcoding for now
    base_region_list = ['CLX_R','SBC_CLx_R','BROADCAST_CLx_R']
    # Creating an empty region_dict to hold the Region name and uuid results.
    region_dict = {}
    
    # REGION DICTIONARY BUILD
    for region_name in base_region_list:
        #Pulling the information for each Region in the default list
        getRegResp = service.getRegion(name = region_name)
        # Set the returned name and uuid to a variable
        region_name = getRegResp['return']['region']['name']
        region_uuid = getRegResp['return']['region']['uuid']
        region_uuid = region_uuid.strip("{}").lower()
        print ("Adding " + region_name + ", " + region_uuid + " to the dictionary")
        #Populate the dict with Region Names and UUID key pairs
        region_dict[region_name]=region_uuid
    print (region_dict)

# Throw an error if there is a problem building the dictionary
except Fault as err:
    print(f'Error Building Region UUID Dictionary: {err}')



# Ask for the name of the new Region to be created
print("Enter new region name:")
new_region_name= input() # wait for input
print (f"\nCreating new region named {new_region_name}...")

 
# Create the new Region and store uuid
try:
    # Create the new region
    resp = service.addRegion(region={"name": new_region_name})
    # Store the returned uuid of the new Region for later
    new_region_uuid = resp['return']
    new_region_uuid = new_region_uuid.strip("{}").lower()
    print(f"New region uuid: {new_region_uuid}")

    # Loop through dictionary and run insert statement for each key (informix DB can't do values listing...)
    for region_uuid in region_dict:
        sql_stmt = '''
        INSERT INTO regionmatrix (fkregion_a, fkregion_b, videobandwidth, fkcodeclist, immersivebandwidth, audiobandwidth)
        VALUES ('{target_uuid}', '{new_uuid}', 384, '22910f2b-51ab-4a46-b606-604a28558568', -2, 64)
        '''.format(
        new_uuid = new_region_uuid,
        target_uuid = region_dict[region_uuid]
        )

        resp = service.executeSQLUpdate(sql_stmt)

    print('Relationships successfully created.')
except Fault as err:
    print(f'Error Inserting Region: {err}')