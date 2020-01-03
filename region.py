from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

def createRegion(newRegionName):
    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    # Attempting to pull the uuids for each Region in the base Region List
    try:
        # Creating the base Region List Hardcoding for now
        baseRegionList = ['BROADCAST_CLx_R','CLX_R','CONF_CLx_R','E911_CLx_R','IVR-QUEUE_CLx_R','MoH_CLx_R','ONNET_CLx_R','SBC_CLx_R','VM_CLx_R']
        # Creating an empty regionDict to hold the Region name and uuid results.
        regionDict = {}
        
        # REGION DICTIONARY BUILD
        for regionName in baseRegionList:
            #Pulling the information for each Region in the default list
            getRegResp = service.getRegion(name = regionName)
            # Set the returned name and uuid to a variable
            regionName = getRegResp['return']['region']['name']
            regionUUID = getRegResp['return']['region']['uuid']
            regionUUID = regionUUID.strip("{}").lower()
            print ("Adding " + regionName + ", " + regionUUID + " to the dictionary")
            #Populate the dict with Region Names and UUID key pairs
            regionDict[regionName]=regionUUID
        # print (regionDict)

    # Throw an error if there is a problem building the dictionary
    except Fault as err:
        print(f'Error Building Region UUID Dictionary: {err}')



    # Ask for the name of the new Region to be created
    # print("Enter new region name:")
    # newRegionName= input() # wait for input
    # print (f"\nCreating new region named {newRegionName}...")

    
    # Create the new Region and store uuid
    try:
        # Create the new region
        resp = service.addRegion(region={"name": f"{newRegionName}"})
        # Store the returned uuid of the new Region for later
        newRegionUUID = resp['return']
        newRegionUUID = newRegionUUID.strip("{}").lower()
        # print(f"New region uuid: {newRegionUUID}")

        # Loop through dictionary and run insert statement for each key (informix DB can't do values listing...)
        for regionUUID in regionDict:
            sql_stmt = '''
            INSERT INTO regionmatrix (fkregion_a, fkregion_b, videobandwidth, fkcodeclist, immersivebandwidth, audiobandwidth)
            VALUES ('{target_uuid}', '{new_uuid}', 384, '22910f2b-51ab-4a46-b606-604a28558568', -2, 64)
            '''.format(
            new_uuid = newRegionUUID,
            target_uuid = regionDict[regionUUID]
            )

            resp = service.executeSQLUpdate(sql_stmt)

        print('Relationships successfully created.')
    except Fault as err:
        print(f'Error Inserting Region: {err}')