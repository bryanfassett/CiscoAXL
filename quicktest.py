from CiscoAXL import AxlConnection, WSDL, BuildPartitions

def stagePartitions(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = BuildPartitions(conn.Service,"STAGING",f"CL{ClusterNumber}")
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

for i in range(1,4):

    result = stagePartitions(str(i))
    if result:
        print(f"Partition build successful for cluster {i}")
    else:
        print(f"Partition build failed for cluster {i}")
