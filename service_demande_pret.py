import xml.etree.ElementTree as ET
from spyne import Application, ServiceBase, rpc, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
from suds import WebFault
from suds.client import Client
import sys


def getExtractInfo(demande_xml):
    url = "http://localhost:8000/ServiceExtractionInformation?wsdl"
    client = Client(url, cache=None)

    try:
        # Appelez la méthode du service en lui passant le JSON comme argument
        response = client.service.ExtraireInformations(demande_xml)

        # Vérifiez la réponse du service
        print("Réponse du service ExtractionInformation:")
        print(response)

        return response

    except WebFault as e:
        # En cas d'erreur, imprimez le message d'erreur
        print(f"Erreur lors de l'appel au service : {e}")
    except Exception as e:
        # Gérez d'autres exceptions possibles ici
        print(f"Une erreur s'est produite : {e}")


def getScoringPret(tree):
    # Créez un client SOAP pour le service solvabilité
    url = "http://localhost:8001/VerifSolvabilite?wsdl"
    client = Client(url, cache=None)

    try:
        # Appelez la méthode du service en lui passant le XML comme argument
        response = client.service.calculateScore(tree)

        # Vérifiez la réponse du service
        print("Réponse du service solvabilité:")
        print(f"Response : {response}")

        return response
    except WebFault as e:
        # En cas d'erreur, imprimez le message d'erreur
        print(f"Erreur lors de l'appel au service : {e}")
    except Exception as e:
        # Gérez d'autres exceptions possibles ici
        print(f"Une erreur s'est produite : {e}")


class DemandePret(ServiceBase):

    @rpc(Unicode, _returns=Unicode)
    def demandePret(ctx, demande_xml):
        try:
            infoClient = getExtractInfo(demande_xml)
            scoreSolvabilite = getScoringPret(infoClient)
            print("Score solvabilité : ", scoreSolvabilite)
            return scoreSolvabilite
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")
            # Vous pouvez retourner une valeur ou un message d'erreur personnalisé ici


if __name__ == '__main__':

    application = Application([DemandePret],
                              tns='DemandePret',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())

    wsgi_app = WsgiApplication(application)

    twisted_apps = [
        (wsgi_app, b'DemandePret')
    ]

    sys.exit(run_twisted(twisted_apps, 8002))
