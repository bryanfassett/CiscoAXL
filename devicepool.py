from connect import open_connection, show_history
from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
client, service, history = open_connection() # Open connection using connect.py

devicepool_name = 'Test_CLx_DP'
devicepool_uuid = ''

try:
    resp = service.addDevicePool(
        devicePool = {
            'name' : devicepool_name,
            'dateTimeSettingName' : 'CMLocal',
            'callManagerGroupName' : 'CLx_CMRG_2A',
            'mediaResourceListName' : 'Test_CLx_MRGL',
            'regionName' : 'Test_CLx_R',
            'srstName' : 'Disable',
            'locationName' : 'Test_CLx_L',
            'localRouteGroup' : 'Test_CLx_RG'
        }
    )

    devicepool_uuid = resp['return'].strip('{}').lower()

    print(f"Device pool created with uuid: {devicepool_uuid}")
except Fault as err:
    print(f'Error Inserting Device Pool: {err}')


try:
    resp = service.getRouteGroup(name = 'SBC_CLx_ATT_RG')
    standardrg_uuid = resp['return']['routeGroup']['uuid'].strip("{}").lower()

    sql_stmt = '''
        INSERT INTO devicepoolroutegroupmap (fkdevicepool, fkroutegroup_local, fkroutegroup)
        VALUES ('{devicepool_uuid}', '00000000-1111-0000-0000-000000000000', '{standardrg_uuid}')
    '''.format(
            devicepool_uuid = devicepool_uuid,
            standardrg_uuid = standardrg_uuid
        )

    resp = service.executeSQLUpdate(sql_stmt)

    print("Device pool successfully created")

except Fault as err:
    print (f'Error Updating Device Pool Route Group Map: {err}')