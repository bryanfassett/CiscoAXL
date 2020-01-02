from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning



disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
client, service, history = open_connection() # Open connection using connect.py



def stageRegions():
    # Create Blank Region Dictionary
    # region_matrix = {}
    try:
        # Create initial hardcoded Regions List to test with
        base_region_list = ['BROADCAST_CLx_R','CLX_R','E911_CLx_R','MoH_CLx_R','ONNET_CLx_R','SBC_CLx_R','VM_CLx_R']
        
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
        print(f"\nDONE! Creating Base Regions\n")
    except Fault as err:
        print(f'Error Inserting Region: {err}')

# Build Initial CMRG CL1 Group 1
def stageCMRGs():
    try:
        for clusterNum in range(1,3):
            for groupNum in range(1,3):
                resp = service.addCallManagerGroup(
                    callManagerGroup = {
                        'name' : f"CL{clusterNum}_CMRG_{groupNum}",
                        'members' : {
                            'member' : {
                                'callManagerName' : 'CM_hq-cucm-pub',
                                'priority' : 1
                            }
                        }      
                    }
                )
                resp = service.addCallManagerGroup(
                    callManagerGroup = {
                        'name' : f"CL{clusterNum}_CMRG_{groupNum}b",
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
    try:
        resp = service.addPhoneNtp(
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

    #CREATE DICTIONARY FOR TIME ZONES --- 
    base_DateTime_List = {'Eastern':'America/New_York','Central':'America/Chicago','Mountain':'America/Denver','Arizona':'America/Phoenix','Pacific':'America/Los_Angeles'}

    try:
        for keys in base_DateTime_List:
            datetimeName = str(keys)
            timezoneName = base_DateTime_List[datetimeName]
            resp = service.addDateTimeGroup(
                dateTimeGroup = {
                    'name' : f"{datetimeName}",
                    'timeZone' : f"{timezoneName}",
                    'separator' : '/',
                    'dateformat' : 'D/M/Y',
                    'timeFormat' : '24-hour'
                }      
            )        
    except Fault as err:
        print(f'Error Inserting DateTimeGroups: {err}')   
