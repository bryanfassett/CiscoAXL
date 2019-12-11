from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree

history = None
client = None
service = None

def open_connection():
    username = 'administrator'
    password = 'ciscopsdt'
    #username = 'TestAdmin'
    #password = '012005'
    host = '10.10.20.1'

    wsdl = r'file://C:/Users/kllyh/Documents/GitHub/CiscoAXL/axlsqltoolkit/schema/current/AXLAPI.wsdl'
    location = 'https://{host}:8443/axl/'.format(host=host)
    binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

    # Create custom session
    session = Session()
    session.verify = False #don't do this in production
    session.auth = HTTPBasicAuth(username, password)

    transport = Transport(cache=SqliteCache(), session=session, timeout=20)
    history = HistoryPlugin()
    client = Client(wsdl=wsdl, transport=transport, plugins=[history])
    service = client.create_service(binding, location)
    return client, service, history

def show_history(history):
    for item in [history.last_sent, history.last_received]:
        print(etree.tostring(item["envelope"], encoding="unicode", pretty_print=True))