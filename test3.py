from CiscoAXL import AxlConnection, WSDL
from zeep.exceptions import Fault

conn = AxlConnection(WSDL)

try:
    if conn.Open():
        print("Trying...")
        SiteCode = "TX999"
        AbbrevCluster = "CLx"
        CAC = 4444
        LocationDict = {
            'name' : f"{SiteCode}_{AbbrevCluster}_L",
            'withinAudioBandwidth' : 0,
            'withinVideoBandwidth' : 0,
            'withinImmersiveKbits' : 0
        }

        betweenLocation = [
            {
                'locationName' : 'Hub_None',
                'weight' : 50,
                'audioBandwidth' : CAC,
                'videoBandwidth' : 512,
                'immersiveBandwidth' : 384
            }
        ]
        if True == True:
            betweenLocation.append(
                {
                    'locationName' : 'Test_CLx_L',
                    'weight' : 50,
                    'audioBandwidth' : CAC,
                    'videoBandwidth' : 512,
                    'immersiveBandwidth' : 384
                }               
            )
        
        print(LocationDict)
        LocationDict.update({'betweenLocations' : { 'betweenLocation': betweenLocation}})
        print(LocationDict)
            
        resp = conn.Service.addLocation(location = LocationDict)

        print("Success")

    else:
        raise Exception("Failed to open connection")

except Fault as err:
    print(err)

except Exception as err:
    print(err)