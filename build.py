from stagelab import stage_regions
from region import createRegion(siteCode)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
# Give the option to prebuild the lab
print("Do you need to prebuild a lab site?  Y/N")
needPrebuild = str(input())

if needPrebuild == "Y":
    # stage_regions()
    print("The lab has been staged.")

# Start gathering info for the New Site Build Portion
print("Moving on to site build...")

print("Enter the new site code:")
siteCode = input() #Wait for Input of Site Code
createRegion(siteCode)
print("New Region and relationships created for:")



print ("Enter the cluster number (1,2,3,4,etc.):")
clusterNum = input()
clusterAbbr = "CL" + clusterNum
print(clusterAbbr)

print("Enter the priority queue amount from the router:")
efQueue = input()
cac = int((int(efQueue) / 92) * 80)
print (cac)

print("Enter the CMRG suffix (2a, 2b, 3a, 3b, etc.") #This will be automated someday
cmrgSuffix = input()
cmrg = clusterAbbr + "_CMRG_" + cmrgSuffix.upper()
print (cmrg)

print("Enter a DateTime Group --Use CMLocal, ZipCode eventually")
dateTimeGroup = input()
print (dateTimeGroup)


    

