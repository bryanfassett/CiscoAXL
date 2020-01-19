from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import RING.conf as Config

class Connection:
    def __init__(self, wsdlpath = Config.WSDL, timeout = 20):
        self.wsdl = wsdlpath
        self.host = '10.10.20.1'
        self.binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
        self.username = 'administrator'
        self.password = 'ciscopsdt'
        self.Session = None
        self.Service = None

        disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
        try:
            session = Session()
            self.Session = session
            session.verify = False #don't do this in production
            session.auth = HTTPBasicAuth(self.username, self.password)



            location = 'https://{host}:8443/axl/'.format(host=self.host)
            transport = Transport(cache=SqliteCache(), session=session, timeout=timeout)
            history = HistoryPlugin()
            client = Client(wsdl=self.wsdl, transport=transport, plugins=[history])

            self.Service = client.create_service(self.binding, location)

        except Fault as err:
            print(err)

    def __del__(self):
        self.Session.close()
    
    def __enter__(self):
        return self.Service
    
    def __exit__(self, type, value, traceback):
        self.Session.close()