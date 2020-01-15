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