import xml.etree.ElementTree as ET
from spyne import Application, ServiceBase, rpc, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted

import sys

class decisionApprobation(ServiceBase):

if __name__ == '__main__':
    tree = ET.parse('bureauCredit.xml')
    root = tree.getroot()

    application = Application([decisionApprobation],
                              tns='decisionApprobation',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())

    wsgi_app = WsgiApplication(application)

    twisted_apps = [
        (wsgi_app, b'decisionApprobation')
    ]

    sys.exit(run_twisted(twisted_apps, 8001))