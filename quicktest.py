from CiscoAXL import AxlConnection, WSDL, BuildPartitions, BuildCSS

def stagePartitions(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = BuildPartitions(conn.Service,"AA699",f"CL{ClusterNumber}")
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def stageCSS(ClusterNumber):
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = BuildCSS(conn.Service,"AA699",f"CL{ClusterNumber}")
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

i = 1
result = stagePartitions(str(i))
if result:
    print(f"Partition build successful for cluster {i}")
else:
    print(f"Partition build failed for cluster {i}")

result = stageCSS(str(i))
if result:
    print(f"Calling Search Space build successful for cluster {i}")
else:
    print(f"Calling Search Space build failed for cluster {i}")

# for i in range(1,4):

#     result = stagePartitions(str(i))
#     if result:
#         print(f"Partition build successful for cluster {i}")
#     else:
#         print(f"Partition build failed for cluster {i}")
    
#     result = stageCSS(str(i))
#     if result:
#         print(f"Calling Search Space build successful for cluster {i}")
#     else:
#         print(f"Calling Search Space build failed for cluster {i}")
