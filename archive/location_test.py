from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning



def createLocation(SiteCode, Cluster, CAC):

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    service = open_connection()
    
    try:
        resp = service.addLocation(
            location = {
                'name' : f"{SiteCode}_{Cluster}_L",
                'withinAudioBandwidth' : 0,
                'withinVideoBandwidth' : 0,
                'withinImmersiveKbits' : 0,
                'betweenLocations' : {
                    'betweenLocation' : {
                        'locationName' : 'Hub_None',
                        'weight' : 50,
                        'audioBandwidth' : CAC,
                        'videoBandwidth' : 512,
                        'immersiveBandwidth' : 384
                    }
                }      
            }
        )

        # location_uuid = resp['return'].strip("{}").lower()

        # resp = service.getLocation(
        #         name = f"E911_{Cluster}_L",
        #         returnedTags = 'uuid'
        # )
        # e911_location_uuid = resp['return']['location']['uuid'].strip("{}").lower()

        # sql_stmt = '''
        #     INSERT INTO locationmatrix (fklocation_a, fklocation_b, weight, kbits, videokbits, immersivekbits)
        #     VALUES ('{location_uuid}','{e911_location_uuid}', 50, 999999, 384, 384)
        # '''.format(
        #      location_uuid = location_uuid,
        #      e911_location_uuid = e911_location_uuid
        # )
        # service.executeSQLUpdate(sql_stmt)

        # return location_uuid
    
    except Fault as err:
        print(f"Error Inserting Location: {err}")
        return ""







# # Get name of the new location and CAC
# print("Enter new location name:")
# location_name= input() # wait for input
# print("Enter CAC value in kbits:")
# location_cac = input() # wait for input
# print (f"\nCreating new location named {location_name}...")

# disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
# client, service, history = open_connection() # Open connection using connect.py

# try:
#     resp = service.getLocation(
#         name = 'E911_CLx_L',
#         returnedTags = 'uuid'
#     )

#     e911_location_uuid = resp['return']['location']['uuid'].strip("{}").lower()

#     resp = service.addLocation(
#         location = {
#             'name' : location_name,
#             'withinAudioBandwidth' : 0,
#             'withinVideoBandwidth' : 0,
#             'withinImmersiveKbits' : 0,
#             'betweenLocations' : {
#                 'betweenLocation' : {
#                     'locationName' : 'Hub_None',
#                     'weight' : 50,
#                     'audioBandwidth' : location_cac,
#                     'videoBandwidth' : 512,
#                     'immersiveBandwidth' : 384
#                 }
#             }      
#         }
#     )

#     location_uuid = resp['return'].strip("{}").lower()
#     print(f"New location uuid: {location_uuid}")

#     sql_stmt = '''
#         INSERT INTO locationmatrix (fklocation_a, fklocation_b, weight, kbits, videokbits, immersivekbits)
#         VALUES ('{location_uuid}','{e911_location_uuid}', 50, 999999, 384, 384)
#     '''.format(
#             location_uuid = location_uuid,
#             e911_location_uuid = e911_location_uuid
#         )  

#     service.executeSQLUpdate(sql_stmt)
#     print('Location created successfully')

# except Fault as err:
#     print(f'Error Inserting Location: {err}')