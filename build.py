from region import createRegion

print("Enter the new site code:")
SiteCode = input() #Wait for Input of Site Code
print("Enter the Cluster number:")
Cluster = input() # Wait for cluster input
Cluster = "CL"+ Cluster
print("Enter the CMRG (CMRG_1, CMRG_2)")
CMRG = input()
print("Enter a timezone offset like -5")
Timezone = input()
print("Do you need to prebuild a lab site?  Y/N")
needPrebuild = str(input())
if needPrebuild == "Y":
    createRegion(SiteCode, Cluster, CMRG, Timezone)
print("Done")
    

