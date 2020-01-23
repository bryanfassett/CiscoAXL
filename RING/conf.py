import os

#
# Start Config Below
#

RegionNamesList = ["SBC","BROADCAST"]
WSDL = r'\axlsqltoolkit\schema\current\AXLAPI.wsdl'
Key = b'l-pDMzxw_svPn1e6rT7bMJTXxqWL8AapGGBSQCGpMw0='

# Connection Info
Host = "10.10.20.1"
Username = "administrator"
Password = "ciscopsdt"

#
# End Config Here
#

# Auto find the WSDL path
#WSDL = f"{_filevar}{os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))}{WSDL}"
WSDL = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}{WSDL}"
print(WSDL)