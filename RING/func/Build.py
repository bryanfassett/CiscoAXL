from zeep.exceptions import Fault
import RING.conf as Config

def Region(conn, RegionName, AbbrevCluster, AddRegionMatrices = True):
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
        for region in Config.RegionNamesList:
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

def Location(conn, SiteCode, AbbrevCluster, CAC, VideoBandwidth = 512, AssociateE911 = True):
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

def MediaResourceGroup(conn, AbbreviatedCluster, CallManagerGroup, ResourceName):
    try:
        resp = conn.addMediaResourceGroup(
            mediaResourceGroup = {
                'name' : f"{AbbreviatedCluster}_Hardware_MRG_{CallManagerGroup}",
                'description' : f"{AbbreviatedCluster}_Hardware_MRG_{CallManagerGroup}",
                'multicast' : 'f',
                'members' : {
                    'member' : [{
                        'deviceName' : ResourceName 
                    }]
                }
            }
        )

        return True, resp['return'].strip('{}').lower()
    except Fault as err:
        return False, err

def MediaResourceGroupList(conn, AbbreviatedCluster):
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


def RouteGroups(conn, AbbreviatedCluster, Carrier):
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

def DevicePool(conn, SiteCode, AbbrevCluster, CMRG, TZ, StandardLRG = None):
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

def Partitions(conn, PartitionDict):
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

def CallingSearchSpace(conn, CssDict, MemberListofList):
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

# NEED TO BUILD THE ADDITIONAL PARAMETERS AND ALSO CONVERT TO USE LISTS/DICTIONARIES TO HANDLE 5DIGIT, +e164, AND 9. PATTERNS
## This method should be globalized so that it can be used for a variety of different use cases.
def TranslationPattern(conn, SiteCode, AbbreviatedCluster, DNRange):
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

def AnalogGateway(conn, SiteCode, AbbreviatedCluster, CMRG, VGType, VGQuantity, MdfFloor):
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

def TransformationPattern(conn, SiteCode, AbbreviatedCluster, PatternList, Carrier, DiscardType, TransformMask, Prefix):
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

def ServiceProfile(conn, SiteCode, AbbreviatedCluster):
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
        
def CallPark(conn, SiteCode, AbbreviatedCluster):
    try:
        for callParkNum in range(0,4):
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