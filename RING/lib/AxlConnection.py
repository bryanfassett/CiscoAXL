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

#
# Classes
#
class Connection:
    def __init__(self, wsdlpath = Config.WSDL):
        self.wsdl = wsdlpath
        self.host = '10.10.20.1'
        self.binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
        self.username = 'administrator'
        self.password = 'ciscopsdt'
        self.Service = None
        self.__State = False

    def ConnectionState(self):
        return self.__State

    def Open(self, timeout=20):
        try:
            disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate

            session = Session()
            session.verify = False #don't do this in production
            session.auth = HTTPBasicAuth(self.username, self.password)

            location = 'https://{host}:8443/axl/'.format(host=self.host)
            transport = Transport(cache=SqliteCache(), session=session, timeout=timeout)
            history = HistoryPlugin()
            client = Client(wsdl=self.wsdl, transport=transport, plugins=[history])

            self.Service = client.create_service(self.binding, location)
            self.__State = True
            return True

        except Fault as err:
            print (f"{err}")
            return False

    def __del__(self):
        pass