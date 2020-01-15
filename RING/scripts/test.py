import RING.lib.Site as Whatever

print("Creating site")


newsite = Whatever.Site("TX999") # created an instance of the class
newsite.TZ = "CMLocal"
newsite.Carrier = "ATT"
newsite.CallManagerGroup = "2A"
newsite.CAC = 4444
newsite.Build()

