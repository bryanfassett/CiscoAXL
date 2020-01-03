from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

    
def createPartitions(SiteCode):

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py
    
    try:
        partitionNames = [f"{SiteCode}_Trans_PT",f"{SiteCode}_Outbound_PT",f"{SiteCode}_Park_PT"]
        for partitions in partitionNames:
            service.addRoutePartition(
                routePartition = {
                    'name' : partitions,
                    'description' : partitions
                }
            )
    except Fault as err:
        print(f'Error Inserting Site Partitions: {err}')


def createCSSs(SiteCode):

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py
    
    try:
        cssNames = [f"{SiteCode}_Device_CSS",f"{SiteCode}_Trans_CSS"]
        for css in cssNames:
            service.addCss(
                css = {
                    'name' : css,
                    'description' : css
                }
            )
    except Fault as err:
        print(f'Error Inserting Site CSSs: {err}')
        
    try:
        cssNames = [f"{SiteCode}_Device_CSS",f"{SiteCode}_Trans_CSS"]
        for css in cssNames:
            service.addCss(
                css = {
                    'name' : css,
                    'description' : css
                }
            )
    except Fault as err:
        print(f'Error Inserting Site CSSs: {err}')
