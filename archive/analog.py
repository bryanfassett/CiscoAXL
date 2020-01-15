from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

    
def createAnalogGateway(SiteCode, Cluster, CMRG, vgType, vgQuantity, mdfFloor):

    disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
    client, service, history = open_connection() # Open connection using connect.py

    try:
        unit = 'ANALOG'
        subunit = '4FXS-MGCP'
        if vgType == 'VG310':
            unit = 'VG-2VWIC-MBRD'
            subunit = '24FXS'
        for count in range(1,int(vgQuantity) + 1):
            service.addGateway(
                gateway = {
                    'domainName' : f"vgc{SiteCode}a0{mdfFloor}a0{count}.uhc.com",
                    'description' : f"{SiteCode}_{Cluster}_{vgType}_GW{count}",
                    'product' : vgType,
                    'protocol' : 'MGCP',
                    'callManagerGroupName' : CMRG,
                    'units' : {
                        'unit' : {
                            'index' : 0,
                            'product' : unit,
                            'subunits' : {
                                'subunit' : {
                                    'index' : 0,
                                    'product' : subunit
                                }

                            }
                        }
                    }
                }
            )

    except Fault as err:
        print(f'Error Inserting Analog Gateway(s): {err}')

