import RING.conf as Config
import RING.lib.AxlConnection as Axl
import RING.func.Build as Build

def stageRegions(ClusterNumber):
    try:
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            base_regions = ["BROADCAST_", "SBC_", "CONF_", "E911_", "IVR-QUEUE_", "MoH_", "ONNET_", "VM_", ""]
            for region in base_regions:
                result, details = Build.Region(conn.Service, f"{region}CL{ClusterNumber}_R", "", False)
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
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            result, details = Build.Location(conn.Service, "E911", f"CL{ClusterNumber}", 999999, 384, False)
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


