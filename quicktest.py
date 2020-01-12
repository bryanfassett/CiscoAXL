from CiscoAXL import AxlConnection, WSDL, buildTransformations

def stageTransformations(AbbrevCluster):
    PatternList = ["1.333333333333[4-9]","1.222222222222[4-9]","1.11111111111[4-9]"] # DN Range Calculation goes here
    SiteCode = "KY111"
    CarrierAbbr = "ATT"
    DiscardType = "PreDot"
    TransformMask = "12"
    Prefix = "12"
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = buildTransformations(conn.Service, PatternList, SiteCode, AbbrevCluster, CarrierAbbr, DiscardType, TransformMask, Prefix)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

i = 1

result = stageTransformations(f'CL{i}')
if result:
    print(f"Calling Search Space build successful for cluster {i}")
else:
    print(f"Calling Search Space build failed for cluster {i}")
