import CiscoAXL
from CiscoAXL import Site

print("Creating site")


newsite = Site("KY999") # created an instance of the class
newsite.ClusterNumber = 1
newsite.TZ = "Central"
newsite.Carrier = "VZB"
newsite.CallManagerGroup = "2A"
newsite.CAC = 44444
newsite.Build()