from stagelab import stageRegions,stageLocations,stageCMRGs,stagePhoneNTP,stageDTGroups,stageMRGs,stageMRGLs,stageRouteGroups,stagePartitions
from region import createRegion
from location import createLocation
from devicepool import createDevicePool
from classofcontrol import createPartitions, createCSSs
from analog import createAnalogGateway


# Give the option to prebuild the lab
print("Do you need to prebuild a lab site?  Y/N")
needPrebuild = str(input())

if needPrebuild == "Y":
    stageRegions()
    print("The Regions have been staged.")
    stageLocations()
    print("The Locations have been staged.")
    stageCMRGs()
    print("The CMRGs have been staged.")
    stagePhoneNTP()
    print("The Phone NTP has been staged.")
    stageDTGroups()
    print("The DateTime Groups have been staged.")
    stageMRGs()
    print("The MRGs Groups have been staged.")
    stageMRGLs()
    print("The MRGLs have been staged.")
    # stageGateways()
    # print("The Gateways have been staged.")
    stageRouteGroups()
    print("The RouteGroups have been staged.")

# Start gathering info for the New Site Build Portion
print("Moving on to site build...")




print ("Enter the cluster number (1-5):")
clusterNum = input()
clusterAbbr = "CL" + clusterNum
# print(clusterAbbr)
print("Enter the new site code:")
siteCode = input() #Wait for Input of Site Code
regionName = f"{siteCode}_CL{clusterNum}_R"
createRegion(regionName)
print("Enter the priority queue amount from the router:")
efQueue = input()
cacValue = int((int(efQueue) / 92) * 80)
# print (cacValue)

# CALL LOCATION FUNTION
createLocation(siteCode, clusterAbbr, cacValue)

# Gather final information for building device pool
print("Enter the CMRG suffix (pair 1-5 a or b") #This will be automated someday
cmrgSuffix = input()
cmrg = clusterAbbr + "_CMRG_" + cmrgSuffix.upper()
# print (cmrg)

print("Enter a DateTime Group --Use CMLocal, Eastern, Central, etc")
datetimeGroup = input()

print("Who is the SIP carrier for the site (ATT,CTL,VZB)")
sipCarrier = input()

createDevicePool(siteCode, clusterAbbr, cmrg, datetimeGroup, sipCarrier)

# createPartitions (siteCode,clusterAbbr)
createCSSs(siteCode,clusterAbbr)

# Build the analog voice gateways
print("What type of analog gateway? (VG204, VG310)")
vgType = input()
print("How many do you need?")
vgQuantity = input()
print("What floor will it be located on?")
mdfFloor = input()

createAnalogGateway(siteCode,clusterAbbr,cmrg,vgType,vgQuantity,mdfFloor)
print("Done")
