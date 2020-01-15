import RING.lib.AxlConnection as Axl
import RING.conf as Config
import RING.func.Build as Build

class Site:
    def __init__(self, SiteCode):
        self.SiteCode = SiteCode
        self.ClusterNumber = 0
        self.AbbreviatedCluster = f"CL{self.ClusterNumber}"
        self.CallManagerGroup = "2A"
        self.CAC = 1 
        self.TZ = "CMLocal" # TODO: value checking
        self.Carrier = "ATT" # TODO: value checking

    def Build(self):
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            try:
                for i in range(1,100):
                    if i == 1:
                        successful, data = Build.Region(conn.Service, f"{self.SiteCode}_{self.AbbreviatedCluster}_R", self.AbbreviatedCluster)
                    elif i == 2:
                        Build.Location(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.CAC)
                    elif i == 3:
                        successful, data = Build.DevicePool(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.CallManagerGroup, self.TZ, f"SBC_{self.AbbreviatedCluster}_{self.Carrier}_RG")
                    else:
                        break

                    if not successful:
                        raise Exception(data)

                print("Site build completed successfully")
                return True

            except Exception as err:
                strErr = f"{err}"
                if strErr[0:24] == "Could not insert new row":
                    print("Error: site already exists!")
                else:
                    print(strErr)
                return False
        else:
            print("Error Opening AXL Connection")
            return False