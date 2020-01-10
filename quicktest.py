from CiscoAXL import AxlConnection, WSDL, getServiceProfiles

def getServiceProfile():
    try:
        conn = AxlConnection(WSDL)
        if conn.Open():
            result, details = getServiceProfiles(conn.Service)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(f'Exception {err}')
        return False


i = 1

result = getServiceProfile()
if result:
    print(f"Calling Search Space build successful for cluster {i}")
else:
    print(f"Calling Search Space build failed for cluster {i}")
