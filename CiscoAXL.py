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
        self.History = None
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
            history = HistoryPlugin(maxlen = 25)
            client = Client(wsdl=self.wsdl, transport=transport, plugins=[history])
            self.History = history

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
        ########### Kelly Added for MRG ##############
        # self.GroupNum ="1"
        # self.ResourceName = "ANN_2"
        # self.PartitionDict = {f"{self.SiteCode}_{self.AbbreviatedCluster}_Outbound_PT":f"{self.SiteCode} Outbound Routing", f"{self.SiteCode}_{self.AbbreviatedCluster}_Trans_PT":f"{self.SiteCode} Intrasite Routing", f"{self.SiteCode}_Park_PT":f"{self.SiteCode} Call Park"}
        # self.CSSDict = {f"{self.SiteCode}_{self.AbbreviatedCluster}_Device_CSS":f"{self.SiteCode} Device CSS", f"{self.SiteCode}_{self.AbbreviatedCluster}_Trans_CSS":f"{self.SiteCode} DN Access"}
        # self.MemberListofList = [
        #     [
        #         f"{self.SiteCode}_{self.AbbreviatedCluster}_Trans_PT",
        #         f"{self.SiteCode}_{self.AbbreviatedCluster}_Outbound_PT",
        #         f"{self.AbbreviatedCluster}_Outbound_PT",
        #         f"E911_{self.AbbreviatedCluster}_Hunt_PT",
        #         f"{self.SiteCode}_Park_PT",
        #         f"{self.AbbreviatedCluster}_CMService_PT"
        #     ],
        #     [f"{self.AbbreviatedCluster}_DN_PT"]
        # ]
        # self.DNRange = "5XXXX"
        # self.VGType = vgtype
        # self.VGQuantity = 0
        # self.MdfFloor = 1
        # self.PatternList = []
        # self.DiscardType = discardType

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
                    # elif i == 4:
                    #     successful, data = BuildMRGs(conn.Service, self.AbbreviatedCluster, self.GroupNum, self.ResourceName)
                    # elif i == 5:
                    #     successful, data = BuildMRGLs(conn.Service, self.AbbreviatedCluster)
                    # elif i == 6:
                    #     successful, data = BuildRouteGroups(conn.Service, self.AbbreviatedCluster, self.Carrier)
                    # elif i == 7:
                    #     successful, data = BuildPartitions(conn.Service, self.PartitionDict)
                    # elif i == 8:
                    #     successful, data = BuildCSS(conn.Service, self.CSSDict, self.MemberListofList)
                    # elif i == 9:
                    #     successful, data = BuildPartitions(conn.Service, self.PartitionDict)
                    # elif i == 10:
                    #     successful, data = BuildTransPatterns(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.DNRange)#INCOMPLETE
                    # elif i == 11:
                    #     successful, data = createAnalogGateway(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.CallManagerGroup, self.VGType, self.VGQuantity, self.MdfFloor)
                    # elif i == 12:
                    #     successful, data = BuildTransformations(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.PatternList, self.Carrier, self.DiscardType, self.TransformMask, self.Prefix)
                    # elif i == 13:
                    #     successful, data = AddServiceProfile(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.DNRange)
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

def BuildRegion(conn, RegionName, AbbreviatedCluster, AddRegionMatrices = True):
    try:
        resp = conn.addRegion(region={"name" : f"{RegionName}"})
        region_uuid = resp["return"].strip("{}").lower()

        if AddRegionMatrices:
            result, RegionUUIDs = __getRegionUUIDs(conn, AbbreviatedCluster)

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

def __getRegionUUIDs(conn, AbbreviatedCluster):
    try:
        ListUUID = []
        for region in RegionNamesList:
            resp = conn.getRegion(name = f"{region}_{AbbreviatedCluster}_R")
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

def BuildLocation(conn, SiteCode, AbbreviatedCluster, CAC, VideoBandwidth = 512, AssociateE911 = True):
    LocationDict = {
        'name' : f"{SiteCode}_{AbbreviatedCluster}_L",
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
                'locationName' : f"E911_{AbbreviatedCluster}_L",
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

def BuildMRGs(conn, AbbreviatedCluster, GroupNum, ResourceName):
    try:
        resp = conn.addMediaResourceGroup(
            mediaResourceGroup = {
                'name' : f"{AbbreviatedCluster}_Hardware_MRG_{GroupNum}",
                'description' : f"{AbbreviatedCluster}_Hardware_MRG_{GroupNum}",
                'multicast' : 'f',
                'members' : {
                    'member' : [{
                        'deviceName' : ResourceName 
                    }]
                }
            }
        )      
        mrg_uuid = resp['return'].strip('{}').lower()

        return True, mrg_uuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err
        
def BuildMRGLs(conn, AbbreviatedCluster):
    try:
        resp = conn.addMediaResourceList(
            mediaResourceList = {
                'name' : f"RemoteSite_{AbbreviatedCluster}_MRGL",
                'members' : {
                    'member' : {
                        'mediaResourceGroupName' : f"{AbbreviatedCluster}_Hardware_MRG_1",
                        'order' : 1
                    }   
                }
            }      
        )        
        mrgl_uuid = resp['return'].strip('{}').lower()
        
        return True, mrgl_uuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def BuildRouteGroups(conn, AbbreviatedCluster, Carrier):
    try:
        resp = conn.addRouteGroup(
            routeGroup = {
                'name' : f"SBC_{AbbreviatedCluster}_{Carrier}_RG",
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
        routegroup_uuid = resp['return'].strip('{}').lower()
        
        return True, routegroup_uuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err
   
def BuildDevicePool(conn, SiteCode, AbbreviatedCluster, CMRG, TZ, StandardLRG = None):
    try: 
        resp = conn.addDevicePool(
            devicePool = {
                "name" : f"{SiteCode}_{AbbreviatedCluster}_DP1",
                "dateTimeSettingName" : TZ,
                'callManagerGroupName' : f"{AbbreviatedCluster}_CMRG_{CMRG}",
                'mediaResourceListName' : f'{SiteCode}_{AbbreviatedCluster}_MRGL',
                'regionName' : f'{SiteCode}_{AbbreviatedCluster}_R',
                'srstName' : 'Disable',
                'locationName' : f'{SiteCode}_{AbbreviatedCluster}_L'
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

def BuildPartitions(conn, PartitionDict):
    try:
        for partition in PartitionDict:
            resp = conn.addRoutePartition(
                routePartition = {
                    'name' : f"{partition}",
                    'description' : f"{PartitionDict[partition]}"
                }
            )
                
        return True, resp['return'].strip('{}').lower()
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def BuildCSS(conn, CssDict, MemberListofList):
    try:
        for CssKeyList, MemberList in zip(CssDict.items(), MemberListofList):
            CssMemberList = []
            for i, member in enumerate(MemberList):
                CssMemberList.append(
                    {
                        'routePartitionName' : member,
                        'index' : i+1
                    }
                )
            CssAddDict = {
                'name' : CssKeyList[0],
                'description' : f"{CssDict[CssKeyList[0]]}"
            }
            CssAddDict.update({'members' : {'member' : CssMemberList}})
            resp = conn.addCss(css = CssAddDict)

        return True, resp['return'].strip('{}').lower()
    except Fault as err:
        print(err)
    except Exception as err:
        print(err)

# NEED TO BUILD THE ADDITIONAL PARAMETERS AND ALSO CONVERT TO USE LISTS/DICTIONARIES TO HANDLE 5DIGIT, +e164, AND 9. PATTERNS
def BuildTransPatterns(conn, SiteCode, AbbreviatedCluster, DNRange):
    try:
        Pattern = "5XXXX"# DN Range Calculation goes here
        prefixDigits = "111114"
        resp = conn.addTransPattern(
            transPattern = {
                'pattern' : Pattern,
                'description' : f"{SiteCode} Incoming for {DNRange}",
                'usage' : 'Translation',
                'routePartitionName' : f"{SiteCode}_{AbbreviatedCluster}_Trans_PT",
                'useCallingPartyPhoneMask' : "On",
                'patternUrgency' : True,
                'prefixDigitsOut' : prefixDigits,#string
                'provideOutsideDialtone' : False,
                'callingSearchSpaceName' : f"{SiteCode}_{AbbreviatedCluster}_Trans_CSS"
            }
        )
        gatewayuuid = resp['return'].strip('{}').lower()
            
        return True, gatewayuuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def createAnalogGateway(conn, SiteCode, AbbreviatedCluster, CMRG, VGType, VGQuantity, MdfFloor):
    try:
        unit = 'ANALOG'
        subunit = '4FXS-MGCP'
        if VGType == 'VG310':
            unit = 'VG-2VWIC-MBRD'
            subunit = '24FXS'
        for count in range(1,int(VGQuantity) + 1):
            resp = conn.addGateway(
                gateway = {
                    'domainName' : f"vgc{SiteCode}a0{MdfFloor}a0{count}.uhc.com",
                    'description' : f"{SiteCode}_{AbbreviatedCluster}_{VGType}_GW{count}",
                    'product' : VGType,
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
        gatewayuuid = resp['return'].strip('{}').lower()
            
        return True, gatewayuuid
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def buildTransformations(conn, SiteCode, AbbreviatedCluster, PatternList, CarrierAbbr, DiscardType, TransformMask, Prefix):
    try:
        for Pattern in PatternList:
            resp = conn.addCallingPartyTransformationPattern(
                callingPartyTransformationPattern = {
                    'pattern' : Pattern,
                    'description' : f"{SiteCode} SBC Outbound ANI", #Update this
                    'routePartitionName' : "Global Learned E164 Numbers",# f"SBC_{AbbreviatedCluster}_{CarrierAbbr}_Outbound_ANI_xform_PT", #Update this
                    'digitDiscardInstructionName' : DiscardType,
                    'callingPartyTransformationMask' : TransformMask,
                    'callingPartyPrefixDigits' : Prefix
                }
            )
            transforminfo = resp['return'].strip('{}').lower()
                
        return True, transforminfo
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err

def AddServiceProfile(conn, SiteCode, AbbreviatedCluster):
    try:
        if conn.Open():
            resp = conn.getServiceProfile(name = f'AAA_{AbbreviatedCluster}_MAC_UCService_Profile')
            serviceProfileDict = resp['return']['serviceProfile']

            serviceProfileDict['name'] = f'{SiteCode}_{AbbreviatedCluster}_MAC_UCService_Profile'
            serviceProfileDict['description'] = f'{SiteCode} {AbbreviatedCluster} MAC UCService Profile'

            conn.addServiceProfile(serviceProfile = serviceProfileDict)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(f'Exception {err}')
        return False
        
def BuildCallPark(conn, SiteCode, AbbreviatedCluster):
    try:
        for callParkNum in range(1,4):
            resp = conn.addCallPark(
                routePartition = {
                    'pattern' : f"896{callParkNum}X",
                    'description' : f"{SiteCode} Call Park",
                    'routePartitionName' : f"{SiteCode}_Park_PT",
                    'callManagerName' : f"CM_hq-cucm-pub"
                }
            )
                
        return True, resp['return'].strip('{}').lower()
    except Fault as err:
        return False, err
    except Exception as err:
        return False, err
