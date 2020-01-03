from classofcontrol import createCSSs, createPartitions

Sitecode = "MN000"
clusterAbbr = "CL3"
CMRG = "CL3_CMRG_2B"
vgType = "VG310"
vgQuantity = 2
mdfFloor = 2
createPartitions (Sitecode,clusterAbbr)
createCSSs(Sitecode,clusterAbbr)
#createAnalogGateway(Sitecode, clusterAbbr, CMRG, vgType, vgQuantity, mdfFloor)
