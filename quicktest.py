from CiscoAXL import AxlConnection, WSDL

def getServiceProfile():
    try:
        conn = AxlConnection(WSDL)
        service = None
        history = None

        if conn.Open():
            service = conn.Service
            history = conn.History

            resp = service.getServiceProfile(name = 'IA021_CL1_MAC_UCService_Profile')
            serviceProfileDict = resp['return']['serviceProfile']
            print(serviceProfileDict)

            serviceProfileDict['name'] = 'ZZYYY_CLx_MAC_UCService_Profile'
            serviceProfileDict['description'] = 'blah'

            service.addServiceProfile(serviceProfile = serviceProfileDict)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(f'Exception {err}')
        return False


i = 1

# result = getServiceProfile()
# if result:
#     print(f"Calling Search Space build successful for cluster {i}")
# else:
#     print(f"Calling Search Space build failed for cluster {i}")
