from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
import RING.conf as Config

class Connection:
    def __init__(self, host, username, password, WSDL = Config.WSDL, timeout = 20):
        self.binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

        disable_warnings(InsecureRequestWarning) # Disable warning output due to invalid certificate
        try:
            session = Session()
            self.Session = session
            session.verify = False #don't do this in production
            session.auth = HTTPBasicAuth(username, password)

            location = f'https://{host}:8443/axl/'
            transport = Transport(cache=SqliteCache(), session=session, timeout=timeout)
            self.History = HistoryPlugin()
            self.Client = Client(wsdl=Config.WSDL, transport=transport, plugins=[self.History])
            self.Service = self.Client.create_service(self.binding, location)

        except Fault as err:
            print(err)

    def __del__(self):
        self.Session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.Session.close()

    def LastSentMessage(self):
        # TODO
        #envelope = self.History.last_sent
        pass

    def LastRecvMessage(self):
        # TODO
        #envelope = self.History.last_received
        pass