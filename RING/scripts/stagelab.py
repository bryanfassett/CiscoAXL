import RING.func.Stage as Stage

for i in range(1,4):
    result = Stage.Regions(str(i))
    if result:
        print(f"Region build successful for cluster {i}")
    else:
        print(f"Region build failed for cluster {i}")

    result = Stage.Locations(str(i))
    if result:
        print(f"E911 Location build was successful for cluster {i}")
    else:
        print(f"E911 Location build failed for cluster {i}")

    Stage.CMRGs(str(i))
    if result:
        print(f"CMRG build was successful for cluster {i}")
    else:
        print(f"CMRG build failed for cluster {i}")

    result = Stage.MediaResourceGroups(str(i))
    if result:
        print(f"Resource Group build was successful for cluster {i}")
    else:
        print(f"Resource Group build failed for cluster {i}")

    result = Stage.MediaResourceGroupLists(str(i))
    if result:
        print(f"Resource Group List build was successful for cluster {i}")
    else:
        print(f"Resource Group List build failed for cluster {i}")

    result = Stage.RouteGroups(str(i))
    if result:
        print(f"Route Group List build was successful for cluster {i}")
    else:
        print(f"Route Group List build failed for cluster {i}")

    result = Stage.Partitions(str(f"CL{i}"))
    if result:
        print(f"Partition build was successful for cluster {i}")
    else:
        print(f"Partition build failed for cluster {i}")
    
    result = Stage.CallingSearchSpaces(str(f"CL{i}"))
    if result:
        print(f"Calling Search Space build was successful for cluster {i}")
    else:
        print(f"Calling Search Space build failed for cluster {i}")
    
Stage.DTGroups()
print(f"DateTime Group failed for cluster")