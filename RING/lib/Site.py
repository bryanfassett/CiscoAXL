import RING.lib.AxlConnection as Axl
import RING.conf as Config
import RING.func.Build as Build
from zeep.exceptions import Fault

class Site:
    def __init__(self, SiteCode, ClusterNumber):
        self.SiteCode = SiteCode
        self.ClusterNumber = ClusterNumber
        self.AbbreviatedCluster = f"CL{self.ClusterNumber}"
        self.CallManagerGroup = "2A"
        self.CAC = 1 
        self.TZ = "CMLocal" # TODO: value checking
        self.Carrier = "ATT" # TODO: value checking
        self.CallManagerGroup ="1"
        self.ResourceName = "ANN_2"
        self.PartitionDict = {f"{self.SiteCode}_{self.AbbreviatedCluster}_Outbound_PT":f"{self.SiteCode} Outbound Routing", f"{self.SiteCode}_{self.AbbreviatedCluster}_Trans_PT":f"{self.SiteCode} Intrasite Routing", f"{self.SiteCode}_Park_PT":f"{self.SiteCode} Call Park"}
        self.CSSDict = {f"{self.SiteCode}_{self.AbbreviatedCluster}_Device_CSS":f"{self.SiteCode} Device CSS", f"{self.SiteCode}_{self.AbbreviatedCluster}_Trans_CSS":f"{self.SiteCode} DN Access"}
        self.MemberListofList = [
            [
                f"{self.SiteCode}_{self.AbbreviatedCluster}_Trans_PT",
                f"{self.SiteCode}_{self.AbbreviatedCluster}_Outbound_PT",
                f"{self.AbbreviatedCluster}_Outbound_PT",
                f"E911_{self.AbbreviatedCluster}_Hunt_PT",
                f"{self.SiteCode}_Park_PT",
                f"{self.AbbreviatedCluster}_CMService_PT"
            ],
            [f"{self.AbbreviatedCluster}_DN_PT"]
        ]
        self.DNRange = "5XXXX"
        self.VGType = "VG204"
        self.VGQuantity = 1
        self.MdfFloor = 1
        self.PatternList = ["1.XXXX","2.XXXX"]
        self.DiscardType = "PreDot"
        self.TransformMask = "+2"
        self.Prefix = "+1"

    def Build(self):
        try:
            with Axl.Connection(Config.Host, Config.Username, Config.Password) as conn:
                for i in range(1,100):
                    if i == 1:
                        successful, data = Build.Region(conn.Service, f"{self.SiteCode}_{self.AbbreviatedCluster}_R", self.AbbreviatedCluster)
                    elif i == 2:
                        successful, data = Build.Location(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.CAC)
                    elif i == 3:
                        successful, data = Build.DevicePool(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.CallManagerGroup, self.TZ, f"SBC_{self.AbbreviatedCluster}_{self.Carrier}_RG")
                    elif i == 4:
                        # TODO MRG and MRGL's methods are currently only built for staging, not new sites. need to globalize the method!
                        #successful, data = Build.MediaResourceGroup(conn.Service, self.AbbreviatedCluster, self.CallManagerGroup, self.ResourceName)
                        pass
                    elif i == 5:
                        # TODO MRG and MRGL's methods are currently only built for staging, not new sites. need to globalize the method!
                        #successful, data = Build.MediaResourceGroupList(conn.Service, self.AbbreviatedCluster)
                        pass
                    elif i == 6:
                        # TODO Route group method is only built for staging, not new sites. need to globalize the method!
                        #successful, data = Build.RouteGroups(conn.Service, self.AbbreviatedCluster, self.Carrier)
                        pass
                    elif i == 7:
                        successful, data = Build.Partitions(conn.Service, self.PartitionDict)
                    elif i == 8:
                        successful, data = Build.CallingSearchSpace(conn.Service, self.CSSDict, self.MemberListofList)
                    elif i == 9:
                        successful, data = Build.TranslationPattern(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.DNRange) # TODO INCOMPLETE
                    elif i == 10:
                        successful, data = Build.AnalogGateway(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.CallManagerGroup, self.VGType, self.VGQuantity, self.MdfFloor)
                    elif i == 11:
                        successful, data = Build.TransformationPattern(conn.Service, self.SiteCode, self.AbbreviatedCluster, self.PatternList, self.Carrier, self.DiscardType, self.TransformMask, self.Prefix)
                    elif i == 12:
                        # TODO this is throwing an error because the service profile is not staged?
                        #successful, data = Build.ServiceProfile(conn.Service, self.SiteCode, self.AbbreviatedCluster)
                        pass
                    elif i == 13:
                        successful, data = Build.CallPark(conn.Service, self.SiteCode, self.AbbreviatedCluster)
                    else:
                        break

                    if not successful:
                        print(f"error on {i}")
                        raise Exception(data)

                print("Site build completed successfully")
                return True

        except (Fault, Exception) as err:
            strErr = f"{err}"
            if strErr[0:24] == "Could not insert new row":
                print("Error: site already exists!")
            else:
                print(strErr)
            return False