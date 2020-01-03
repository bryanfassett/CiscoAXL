from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


def stageRegions():
    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    # Create Blank Region Dictionary
    # region_matrix = {}
    try:
        # Create initial hardcoded Regions List to test with
        baseRegionList = ['BROADCAST_CLx_R','CLX_R','CONF_CLx_R','E911_CLx_R','IVR-QUEUE_CLx_R','MoH_CLx_R','ONNET_CLx_R','SBC_CLx_R','VM_CLx_R']
        
        # Create the new regions from hardcoded region list
        for region_name in baseRegionList:
            print (f"\nCreating new region named {region_name}...")
            service.addRegion(region={"name": region_name})
            # Store the returned uuids not needed.
            # Will query when needed at runtime in each script.
            # region_uuid = resp['return']
            # region_uuid = region_uuid.strip("{}").lower()
            # print(f"New region uuid: {region_uuid}")
            # region_matrix.update({region_name:region_uuid})
            print (f"Region {region_name} successfully created.")
        print(f"\nDONE! Creating Base Regions\n")
    except Fault as err:
        print(f'Error Inserting Region: {err}')

# STAGE LOCATIONS
def stageLocations():

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py
    
    try:
        for clusterNum in range(1,6):
            service.addLocation(
                location = {
                    'name' : f"E911_CL{clusterNum}_L",
                    'withinAudioBandwidth' : 0,
                    'withinVideoBandwidth' : 0,
                    'withinImmersiveKbits' : 0,
                    'betweenLocations' : {
                        'betweenLocation' : {
                            'locationName' : 'Hub_None',
                            'weight' : 50,
                            'audioBandwidth' : 999999,
                            'videoBandwidth' : 384,
                            'immersiveBandwidth' : 384
                        }
                    }      
                }
            )
    except Fault as err:
        print(f'Error Inserting Locations: {err}')

# Build Initial CMRG CL1 Group 1
def stageCMRGs():
    
    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    try:
        for clusterNum in range(1,6):
            for groupNum in range(1,5):
                for side in ["a","b"]:
                    service.addCallManagerGroup(
                        callManagerGroup = {
                            'name' : f"CL{clusterNum}_CMRG_{groupNum}{side}",
                            'members' : {
                                'member' : {
                                    'callManagerName' : 'CM_hq-cucm-pub',
                                    'priority' : 1
                                }
                            }      
                        }
                    )
                print(f"\nCreating Base CMRG for CL{clusterNum} pair {groupNum}\n")

    except Fault as err:
        print(f'Error Inserting CMRG: {err}')

# BUILD PHONE NTP
def stagePhoneNTP():
    
    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    try:
        service.addPhoneNtp(
            phoneNtp = {
                'ipAddress' : '10.10.20.1',
                'description': 'NTP Server 1',
                'mode' : 'Directed Broadcast'
            }
        )
    except Fault as err:
        print(f'Error Inserting NTP: {err}')

# BUILD DATE TIME GROUPS
def stageDTGroups():
    
    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    #CREATE DICTIONARY FOR TIME ZONES --- 
    base_DateTime_List = {'Eastern':'America/New_York','Central':'America/Chicago','Mountain':'America/Denver','Arizona':'America/Phoenix','Pacific':'America/Los_Angeles'}

    try:
        for key in base_DateTime_List:
            resp = service.addDateTimeGroup(
                dateTimeGroup = {
                    'name' : f"{key}",
                    'timeZone' : f"{base_DateTime_List[key]}",
                    'separator' : '/',
                    'dateformat' : 'D/M/Y',
                    'timeFormat' : '12-hour'
                }      
            )        
    except Fault as err:
        print(f'Error Inserting DateTimeGroups: {err}')   

# BUILD MRG
def stageMRGs():
    
    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    try:
        for clusterNum in range(1,6):
            for groupNum in ["1","2"]:
                service.addMediaResourceGroup(
                    mediaResourceGroup = {
                        'name' : f"CL{clusterNum}_Hardware_MRG_{groupNum}",
                        'description' : f"CL{clusterNum}_Hardware_MRG_{groupNum}",
                        'multicast' : 'f',
                        'members' : {
                            'member' : {
                                'deviceName' : 'ANN_2'
                            }   
                        }
                    }      
                )        
    except Fault as err:
        print(f'Error Inserting MRGs: {err}')

# BUILD MRG
def stageMRGLs():

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    try:
        for clusterNum in range(1,6):
            service.addMediaResourceList(
                mediaResourceList = {
                    'name' : f"RemoteSite_CL{clusterNum}_MRGL",
                    'members' : {
                        'member' : {
                            'mediaResourceGroupName' : f"CL{clusterNum}_Hardware_MRG_1",
                            'order' : 1
                        }   
                    }
                }      
            )        
    except Fault as err:
        print(f'Error Inserting MRGLs: {err}')

# BUILD ROUTEGROUPS
def stageRouteGroups():

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    try:
        for clusterNum in range(1,6):
            for carrierName in ["ATT","CTL","VZN"]:
                service.addRouteGroup(
                    routeGroup = {
                        'name' : f"SBC_CL{clusterNum}_{carrierName}_RG",
                        'distributionAlgorithm' : "Circular",
                        'members' : {
                            'member' : {
                                'deviceSelectionOrder' : 1,
                                'deviceName' : "SIPTrunktoCUP",
                                'port' : 1
                            }   
                        }
                    }      
                )        
    except Fault as err:
        print(f'Error Inserting RouteGroups: {err}')

def stagePartitions():

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py
    
    try:
        for clusterNum in range(1,6):
            cluster = f"CL{clusterNum}"
            partitionNames = [f"{cluster}_DN_PT",f"{cluster}_Outbound_PT",f"E911_{cluster}_Hunt_PT",f"{cluster}_CMService_PT"]
            for partitions in partitionNames:
                service.addRoutePartition(
                    routePartition = {
                        'name' : partitions,
                        'description' : partitions
                    }
                )
    except Fault as err:
        print(f'Error Inserting Partitions: {err}')
