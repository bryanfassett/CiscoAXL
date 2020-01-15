import os

#
# Start Config Below
#

RegionNamesList = ["SBC","BROADCAST"]
WSDL = r'\axlsqltoolkit\schema\current\AXLAPI.wsdl'
Key = b'l-pDMzxw_svPn1e6rT7bMJTXxqWL8AapGGBSQCGpMw0='


#
# End Config Here
#

# Auto find the WSDL path
_filevar = r"file:\\"
WSDL = f"{_filevar}{os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))}{WSDL}"
print(WSDL)