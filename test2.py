from CiscoAXL import BuildRegion, AxlConnection, WSDL

service = AxlConnection(WSDL)
service.Open()

regions = ["BROADCAST", "SBC"]
for index, region in enumerate(regions):
    result, details = BuildRegion(service, region, f"CL{index+1}", False)
    if result:
        print(f"UUID: {details}")

del service