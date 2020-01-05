from CiscoAXL import AxlConnection, WSDL, BuildRegion, BuildLocation, BuildCMRGs, BuildDTGroups, BuildMRGs, BuildMRGLs, BuildRouteGroups, BuildPartitions

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
        if conn.Open():
            result, details = BuildCMRGs(conn.Service, f"CL{ClusterNumber}", i)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageDTGroups():
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = BuildDTGroups(conn.Service)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageMRGs(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            for GroupNum in ["1","2"]:
                result, details = BuildMRGs(conn.Service,f"CL{ClusterNumber}",GroupNum)
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

def stagePartitions(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.open():
            result, details = BuildRouteGroups(conn.Service,"STAGING",f"CL{ClusterNumber}")
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
        print(f"E911 Location build successful for cluster {i}")
    else:
        print(f"E911 Location build failed for cluster {i}")

    result = stageCMRGs(str(i))
    if result:
        print(f"CMRG build successful for cluster {i}")
    else:
        print(f"CMRG build failed for cluster {i}")

    result = stageMRGs(str(i))
    if result:
        print(f"Resource Group build successful for cluster {i}")
    else:
        print(f"Resource Group build failed for cluster {i}")

    result = stageRouteGroups(str(i))
    if result:
        print(f"Route Group List build successful for cluster {i}")
    else:
        print(f"Route Group List build failed for cluster {i}")

    result = stagePartitions(str(i))
    if result:
        print(f"Partition build successful for cluster {i}")
    else:
        print(f"Partition build failed for cluster {i}")

result = stageDTGroups()
if result:
    print(f"DateTime Group build successful for cluster")
else:
    print(f"DateTime Group failed for cluster")
