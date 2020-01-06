from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

    
def createPartitions(SiteCode, Cluster):

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py
    
    try:
        partitionNames = [f"{SiteCode}_{Cluster}_Trans_PT",f"{SiteCode}_{Cluster}_Outbound_PT",f"{SiteCode}_Park_PT"]
        for partitions in partitionNames:
            service.addRoutePartition(
                routePartition = {
                    'name' : partitions,
                    'description' : partitions
                }
            )
    except Fault as err:
        print(f'Error Inserting Site Partitions: {err}')


def createCSSs(SiteCode, Cluster):

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py
    
    try:
        cssNames = {f"{SiteCode}_{Cluster}_Device_CSS":f"{SiteCode} Device CSS",f"{SiteCode}_{Cluster}_Trans_CSS":f"{SiteCode} DN Access"}
        for css in cssNames:
            service.addCss(
                css = {
                    'name' : css,
                    'description' : cssNames[css]
                }
            )
    except Fault as err:
        print(f'Error Inserting Site CSSs: {err}')

    try:
        cssDeviceMembers = [f"{SiteCode}_{Cluster}_Trans_PT",f"{SiteCode}_{Cluster}_Outbound_PT",f"{Cluster}_Outbound_PT",f"E911_{Cluster}_Hunt_PT",f"{SiteCode}_Park_PT",f"{Cluster}_CMService_PT"]
        for i, member in enumerate(cssDeviceMembers):
            service.updateCss(
                name = f"{SiteCode}_{Cluster}_Device_CSS",
                addMembers = {
                    'member' : {
                        'routePartitionName' : member,
                        'index' : ++i
                    }
                }
            )
    except Fault as err:
        print(f'Error Inserting CSSs Members: {err}')
