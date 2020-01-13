from CiscoAXL import *

def stageRegions(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            base_regions = ["BROADCAST_", "SBC_", "CONF_", "E911_", "IVR-QUEUE_", "MoH_", "ONNET_", "VM_", ""]
            for region in base_regions:
                result, details = BuildRegion(conn.Service, f"{region}CL{ClusterNumber}_R", "", False)
                if not result:
                    raise Exception(details)

            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageLocations(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = BuildLocation(conn.Service, "E911", f"CL{ClusterNumber}", 999999, 384, False)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageCMRGs(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        service = None
        # history = None
        if conn.Open():
            service = conn.Service
            # history = conn.History
            try:
                for groupNum in range(1,4):
                    for groupLetter in ["A","B"]:
                        service.addCallManagerGroup(
                            callManagerGroup = {
                                'name' : f"CL{ClusterNumber}_CMRG_{groupNum}{groupLetter}",
                                'members' : {
                                    'member' : {
                                        'callManagerName' : 'CM_hq-cucm-pub',
                                        'priority' : 1
                                    }
                                }      
                            }
                        )
                    groupNum = groupNum + 1
            except Fault as err:
                print(f'Error Inserting CMRGs: {err}')
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageDTGroups():
    try:
        conn = AxlConnection(WSDL)    
        base_DateTime_List = {'Eastern':'America/New_York','Central':'America/Chicago','Mountain':'America/Denver','Arizona':'America/Phoenix','Pacific':'America/Los_Angeles'}
        if service.Open():
            service = conn.Service
            try:
                for key in base_DateTime_List:
                    service.addDateTimeGroup(
                        dateTimeGroup = {
                            'name' : f"{key}",
                            'timeZone' : f"{base_DateTime_List[key]}",
                            'separator' : '/',
                            'dateformat' : 'D/M/Y',
                            'timeFormat' : '12-hour'
                        }      
                    )
            except Fault as err:
                print(f'Error Inserting CMRGs: {err}')
        else:
                raise Exception("Error Opening Connection")
    except Exception as err:
            print(err)
            return False

def stageMRGs(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            for GroupNum in ["1","2"]:
                result, details = BuildMRGs(conn.Service,f"CL{ClusterNumber}",GroupNum, deviceName='ANN2')
                if not result:
                    raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageMRGLs(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = BuildMRGLs(conn.Service,f"CL{ClusterNumber}")
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageRouteGroups(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            for Carrier in ["ATT","CTL","VZN"]:
                result, details = BuildRouteGroups(conn.Service,f"CL{ClusterNumber}",Carrier)
                if not result:
                    raise Exception(details)
                return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stagePartitions(AbbrevCluster):
    try:
        partitionDict = {f'{AbbrevCluster}_Trans_PT':'Cluster Translation Partition',f'{AbbrevCluster}_DN_PT':f'{AbbrevCluster} DN Partition',f'{AbbrevCluster}_Outbound_PT':f'{AbbrevCluster} Outbound Partition',f'E911_{AbbrevCluster}_Hunt_PT':f'{AbbrevCluster} 911 Hunt Partition',f'{AbbrevCluster}_CMService_PT':f'{AbbrevCluster} Service Partition'}
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = BuildPartitions(conn.Service,partitionDict)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageCSS(AbbrevCluster):
    try:
        conn = AxlConnection(WSDL)
        CssDict = {f"{AbbrevCluster}_Trans_CSS":f"Cluster TransPattern CSS",f"{AbbrevCluster}_Inbound_CSS":f"Cluster Inbound Access",f"{AbbrevCluster}_Internal_CSS":f"Cluster Internal Only CSS",f"{AbbrevCluster}_Local_CSS":f"Cluster Local Dialing CSS",f"{AbbrevCluster}_LongDistance_CSS":f"Cluster Long Distance Dialing CSS",f"{AbbrevCluster}_International_CSS":f"Cluster International Dialing CSS"}
        MemberListofList = [
            [f"{AbbrevCluster}_Trans_PT",f"{AbbrevCluster}_Outbound_PT",f"E911_{AbbrevCluster}_Hunt_PT",f"{AbbrevCluster}_CMService_PT"],
            [f"{AbbrevCluster}_DN_PT",f"E911_{AbbrevCluster}_Hunt_PT"],
            [f"{AbbrevCluster}_Trans_PT",f"{AbbrevCluster}_Outbound_PT"],
            [f"{AbbrevCluster}_DN_PT"],
            [f"{AbbrevCluster}_DN_PT",f"{AbbrevCluster}_Outbound_PT"],
            [f"{AbbrevCluster}_DN_PT",f"{AbbrevCluster}_Outbound_PT"]
        ]

        if conn.Open():
            result, details = BuildCSS(conn.Service, CssDict, MemberListofList)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False


for i in range(1,4):

    result = stageRegions(str(i))
    if result:
        print(f"Region build successful for cluster {i}")
    else:
        print(f"Region build failed for cluster {i}")

    result = stageLocations(str(i))
    if result:
        print(f"E911 Location build was successful for cluster {i}")
    else:
        print(f"E911 Location build failed for cluster {i}")

    stageCMRGs(str(i))
    if result:
        print(f"CMRG build was successful for cluster {i}")
    else:
        print(f"CMRG build failed for cluster {i}")

    result = stageMRGs(str(i))
    if result:
        print(f"Resource Group build was successful for cluster {i}")
    else:
        print(f"Resource Group build failed for cluster {i}")

    result = stageMRGLs(str(i))
    if result:
        print(f"Resource Group List build was successful for cluster {i}")
    else:
        print(f"Resource Group List build failed for cluster {i}")

    result = stageRouteGroups(str(i))
    if result:
        print(f"Route Group List build was successful for cluster {i}")
    else:
        print(f"Route Group List build failed for cluster {i}")

    result = stagePartitions(str(f"CL{i}"))
    if result:
        print(f"Partition build was successful for cluster {i}")
    else:
        print(f"Partition build failed for cluster {i}")
    
    result = stageCSS(str(f"CL{i}"))
    if result:
        print(f"Calling Search Space build was successful for cluster {i}")
    else:
        print(f"Calling Search Space build failed for cluster {i}")
    
stageDTGroups()
if result:
    print(f"DateTime Group build was successful for cluster")
else:
    print(f"DateTime Group failed for cluster")
