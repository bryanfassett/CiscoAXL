from CiscoAXL import AxlConnection, WSDL, BuildCSS

def stageCSS(AbbrevCluster):
    try:
        conn = AxlConnection(WSDL)
        CssDict = {f"{AbbrevCluster}_Trans_CSS":f"Cluster TransPattern CSS",f"{AbbrevCluster}_Inbound_CSS":f"Cluster Inbound Access",f"{AbbrevCluster}_Internal_CSS":f"Cluster Internal Only CSS",f"{AbbrevCluster}_Local_CSS":f"Cluster Local Dialing CSS",f"{AbbrevCluster}_LongDistance_CSS":f"Cluster Long Distance Dialing CSS",f"{AbbrevCluster}_International_CSS":f"Cluster International Dialing CSS"}
        MemberListofList = [
            [f"{AbbrevCluster}_Trans_PT",f"{AbbrevCluster}_Outbound_PT",f"{AbbrevCluster}_Outbound_PT",f"E911_{AbbrevCluster}_Hunt_PT",f"{AbbrevCluster}_CMService_PT"],
            [f"{AbbrevCluster}_DN_PT",f"E911_{AbbrevCluster}_Hunt_PT"],
            [f"{AbbrevCluster}_Trans_PT",f"{AbbrevCluster}_Outbound_PT",f"{AbbrevCluster}_Outbound_PT"],
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


i = 1

result = stageCSS(str(f"CL{i}"))
if result:
    print(f"Calling Search Space build successful for cluster {i}")
else:
    print(f"Calling Search Space build failed for cluster {i}")
