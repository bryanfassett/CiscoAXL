from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

    
# def createTransPatterns(SiteCode, Cluster, didRange):

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    # Calculate the transpatterns
    didRange = 111-222-3333 to 4444
    
    print (didRange)

    try:
        # COPIED FROM GATEWAYS AS TEMPLATE
        # for count in range(1,vgQuantity + 1):
        #     service.addGateway(
        #         gateway = {
        #             'domainName' : f"vgc{SiteCode}a0{mdfFloor}a0{count}.uhc.com",
        #             'description' : f"{SiteCode}_{Cluster}_{vgType}_GW{count}",
        #             'product' : vgType,
        #             'protocol' : 'MGCP',
        #             'callManagerGroupName' : CMRG,
        #             'units' : {
        #                 'unit' : {
        #                     'index' : 0,
        #                     'product' : unit,
        #                     'subunits' : {
        #                         'subunit' : {
        #                             'index' : 0,
        #                             'product' : subunit
        #                         }

        #                     }
        #                 }
        #             }
        #         }
        #     )

    except Fault as err:
        print(f'Error Inserting Translation Patterns: {err}')
