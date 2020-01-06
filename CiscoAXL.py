from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree

#
# Config
#

RegionNamesList = ["SBC","BROADCAST"]
WSDL = r'file://C:/Users/kllyh/Documents/GitHub/CiscoAXL/axlsqltoolkit/schema/current/AXLAPI.wsdl'


#
# Classes
#

class AxlConnection:
    def __init__(self, wsdlpath):
        self.wsdl = wsdlpath
        self.host = '10.10.20.1'
        self.binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
        self.username = 'administrator'
        self.password = 'ciscopsdt'
        self.Service = None
        self.__State = False

    def ConnectionState(self):
        return self.__State

    def Open(self, timeout=20):
        try:
            disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate

            session = Session()
            session.verify = False #don't do this in production
            session.auth = HTTPBasicAuth(self.username, self.password)

            location = 'https://{host}:8443/axl/'.format(host=self.host)
            transport = Transport(cache=SqliteCache(), session=session, timeout=timeout)
            history = HistoryPlugin()
            client = Client(wsdl=self.wsdl, transport=transport, plugins=[history])

            self.Service = client.create_service(self.binding, location)
            self.__State = True
            return True

        except Fault as err:
            print (f"{err}")
            return False

    def __del__(self):
        pass

class Site:
    def __init__(self, SiteCode):
        self.SiteCode = SiteCode
        self.ClusterNumber = 0
        self.AbbreviatedCluster = f"CL{self.ClusterNumber}"
        self.CallManagerGroup = "2A"
        self.CAC = 1 
        self.TZ = "CMLocal" # TODO: value checking
        self.Carrier = "ATT" # TODO: value checking

    def Build(self):
        conn = AxlConnection(WSDL)
        if conn.Open():
            try:
                for i in range(1,100):
                    if i == 1:
                        successful, data = BuildRegion(conn.Service, f"{self.SiteCode}_{self.AbbreviatedCluster}_R", self.AbbreviatedCluster)
                    elif i == 2:
                        BuildLocation(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.CAC)
                    elif i == 3:
                        successful, data = BuildDevicePool(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.CallManagerGroup, self.TZ, f"SBC_{self.AbbreviatedCluster}_{self.Carrier}_RG")
                    else:
                        break

                    if not successful:
                        raise Exception(data)

                print("Site build completed successfully")
                return True

            except Exception as err:
                strErr = f"{err}"
                if strErr[0:24] == "Could not insert new row":
                    print("Error: site already exists!")
                else:
                    print(strErr)
                return False
        else:
            print("Error Opening AXL Connection")
            return False



#
# Non-Instanced functions below
#

def BuildRegion(conn, RegionName, AbbrevCluster, AddRegionMatrices = True):
    try:
        resp = conn.addRegion(region={"name" : f"{RegionName}"})
        region_uuid = resp["return"].strip("{}").lower()

        if AddRegionMatrices:
            result, RegionUUIDs = __getRegionUUIDs(conn, AbbrevCluster)

            if result:
                for region in RegionUUIDs:
                    addRegionMatrix(conn, region_uuid, region)
            else:
                print(RegionUUIDs)

        return True, region_uuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def __getRegionUUIDs(conn, AbbrevCluster):
    try:
        ListUUID = []
        for region in RegionNamesList:
            resp = conn.getRegion(name = f"{region}_{AbbrevCluster}_R")
            ListUUID.append(resp['return']['region']['uuid'].strip("{}").lower())
        return True, ListUUID
    except Fault as err:
        return False, err

def addRegionMatrix(conn, Aregionuuid, Bregionuuid):
    try:
        sql_stmt = '''
                INSERT INTO regionmatrix (fkregion_a, fkregion_b, videobandwidth, fkcodeclist, immersivebandwidth, audiobandwidth)
                VALUES ('{new_uuid}', '{target_uuid}', 384, '22910f2b-51ab-4a46-b606-604a28558568', -2, 64)
            '''.format(
                    new_uuid = Aregionuuid,
                    target_uuid = Bregionuuid
                )
        conn.executeSQLUpdate(sql_stmt)
        return True, ""
    except Fault as err:
        return False, err

def BuildLocation(conn, SiteCode, AbbrevCluster, CAC, VideoBandwidth = 512, AssociateE911 = True):
    LocationDict = {
        'name' : f"{SiteCode}_{AbbrevCluster}_L",
        'withinAudioBandwidth' : 0,
        'withinVideoBandwidth' : 0,
        'withinImmersiveKbits' : 0
    }

    BetweenLocationList = [
        {
            'locationName' : 'Hub_None',
            'weight' : 50,
            'audioBandwidth' : CAC,
            'videoBandwidth' : VideoBandwidth,
            'immersiveBandwidth' : 384
        }
    ]
    if AssociateE911:
        BetweenLocationList.append(
            {
                'locationName' : f"E911_{AbbrevCluster}_L",
                'weight' : 50,
                'audioBandwidth' : 999999,
                'videoBandwidth' : 384,
                'immersiveBandwidth' : 384
            } 
        )
    LocationDict.update({'betweenLocations' : { 'betweenLocation': BetweenLocationList}})

    try:
        resp = conn.addLocation(location = LocationDict)
        return True, resp['return'].strip("{}").lower()
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def BuildDevicePool(conn, SiteCode, AbbrevCluster, CMRG, TZ, StandardLRG = None):
    try: 
        resp = conn.addDevicePool(
            devicePool = {
                "name" : f"{SiteCode}_{AbbrevCluster}_DP1",
                "dateTimeSettingName" : TZ,
                'callManagerGroupName' : f"{AbbrevCluster}_CMRG_{CMRG}",
                'mediaResourceListName' : f'{SiteCode}_{AbbrevCluster}_MRGL',
                'regionName' : f'{SiteCode}_{AbbrevCluster}_R',
                'srstName' : 'Disable',
                'locationName' : f'{SiteCode}_{AbbrevCluster}_L'
            }
        )
        devicepool_uuid = resp['return'].strip('{}').lower()
        
        if not StandardLRG == None:
            result, details = setStandardLRG(conn, devicepool_uuid, StandardLRG)
            if not result:
                raise Exception(details)
    
        return True, devicepool_uuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def setStandardLRG(conn, DevicePoolUUID, RouteGroup):
    try:
        resp = conn.getRouteGroup(name = RouteGroup)
        RouteGroupUUID = resp['return']['routeGroup']['uuid'].strip("{}").lower()

        sql_stmt = '''
            INSERT INTO devicepoolroutegroupmap (fkdevicepool, fkroutegroup_local, fkroutegroup)
            VALUES ('{DevicePoolUUID}', '00000000-1111-0000-0000-000000000000', '{standardrg_uuid}')
        '''.format(
             DevicePoolUUID = DevicePoolUUID,
             standardrg_uuid = RouteGroupUUID
        )
        conn.executeSQLUpdate(sql_stmt)
    
        return True, ""
    except Fault as err:
        return False, err

def BuildPartitions(conn, SiteCode, AbbrevCluster):
    if SiteCode == 'STAGING':
        partitionNames = {f'{AbbrevCluster}_DN_PT':f'{AbbrevCluster} DN Partition',f'{AbbrevCluster}_Outbound_PT':f'{AbbrevCluster} Outbound Partition',f'E911_{AbbrevCluster}_Hunt_PT':f'{AbbrevCluster} 911 Hunt Partition',f'{AbbrevCluster}_CMService_PT':f'{AbbrevCluster} Service Partition'}
    else:
        partitionNames = {f'{SiteCode}_{AbbrevCluster}_Trans_PT':f'{SiteCode} Translation Partition',f'{SiteCode}_{AbbrevCluster}_Outbound_PT':f'{SiteCode} Outbound Partition',f'{SiteCode}_Park_PT':f'{SiteCode} Park Partition'}
    try:
        for partition in partitionNames:
            resp = conn.addRoutePartition(
                routePartition = {
                    'name' : f"{partition}",
                    'description' : f"{partitionNames[partition]}"
                }
            )
        partition_uuid = resp['return'].strip('{}').lower()
            
        return True, partition_uuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def BuildCSS(conn, SiteCode, AbbrevCluster):
    try:
        cssNames = {f"{SiteCode}_{AbbrevCluster}_Device_CSS":f"{SiteCode} Device CSS",f"{SiteCode}_{AbbrevCluster}_Trans_CSS":f"{SiteCode} DN Access"}
        for css in cssNames:
            resp = conn.addCss(
                css = {
                    'name' : css,
                    'description' : cssNames[css]
                }
            )
        css_uuid = resp['return'].strip('{}').lower()
            
        cssDeviceMembers = [f"{SiteCode}_{AbbrevCluster}_Trans_PT",f"{SiteCode}_{AbbrevCluster}_Outbound_PT",f"{AbbrevCluster}_Outbound_PT",f"E911_{AbbrevCluster}_Hunt_PT",f"{SiteCode}_Park_PT",f"{AbbrevCluster}_CMService_PT"]
        for i, member in enumerate(cssDeviceMembers):
            resp = conn.updateCss(
                name = f"{SiteCode}_{AbbrevCluster}_Device_CSS",
                addMembers = {
                    'member' : {
                        'routePartitionName' : member,
                        'index' : ++i
                    }
                }
            )
        resp = conn.updateCss(
            name = f"{SiteCode}_{AbbrevCluster}_Trans_CSS",
            addMembers = {
                'member' : {
                    'routePartitionName' : f"{AbbrevCluster}_DN_PT",
                    'index' : 1
                }
            }
        )
        cssMembers_uuid = resp['return'].strip('{}').lower()
        return True, cssMembers_uuid
            
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def BuildTransPatterns(conn, SiteCode, AbbrevCluster, DNRange):
    try:
        pattern = "5XXXX"# DN Range Calculation goes here
        prefixDigits = "111114"
        resp = conn.addTransPattern(
            transPattern = {
                'pattern' : pattern,
                'description' : f"{SiteCode} Incoming for {DNRange}",
                'usage' : 'Translation',
                'routePartitionName' : f"{SiteCode}_{AbbrevCluster}_Trans_PT",
                'useCallingPartyPhoneMask' : "On",
                'patternUrgency' : True,
                'prefixDigitsOut' : prefixDigits,#string
                'provideOutsideDialtone' : False,
                'callingSearchSpaceName' : f"{SiteCode}_{AbbrevCluster}_Trans_CSS"
            }
        )
        transpattern_uuid = resp['return'].strip('{}').lower()
            
        return True, transpattern_uuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err
