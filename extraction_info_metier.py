import logging
import sys
from spyne import ServiceBase, Unicode, Application, rpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
import xml.etree.ElementTree as ET

class ServiceExtractionInformation(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def ExtraireInformations(ctx, demande_pret_xml):
        # Analyser le XML pour extraire les informations
        informations_structurees = extraire_informations(demande_pret_xml)

        # 5. Stockage des informations (Supposons que vous utilisiez une base de données)
        # Vous devez adapter cette partie à votre système de stockage.

        # Renvoyez le résultat de l'extraction des informations
        return informations_structurees

# Fonction d'extraction des informations à partir du XML
def extraire_informations(demande_pret_xml):
    informations_structurees = {}

    try:
        root = ET.fromstring(demande_pret_xml)

        # Exemple d'extraction d'informations à partir du XML
        prenom_client = root.find('.//PrenomClient')
        nom_client = root.find('.//NomClient')
        adresse_rue = root.find('.//Adresse/Rue')
        adresse_ville = root.find('.//Adresse/Ville')
        adresse_code_postal = root.find('.//Adresse/CodePostal')
        adresse_pays = root.find('.//Adresse/Pays')
        montant_pret_demande = root.find('.//MontantPretDemande')
        # Continuez d'extraire d'autres informations

        # Stocker les informations dans un dictionnaire
        informations_structurees['prenom_client'] = prenom_client.text if prenom_client is not None else ''
        informations_structurees['nom_client'] = nom_client.text if nom_client is not None else ''
        informations_structurees['adresse_rue'] = adresse_rue.text if adresse_rue is not None else ''
        informations_structurees['adresse_ville'] = adresse_ville.text if adresse_ville is not None else ''
        informations_structurees['adresse_code_postal'] = adresse_code_postal.text if adresse_code_postal is not None else ''
        informations_structurees['adresse_pays'] = adresse_pays.text if adresse_pays is not None else ''
        informations_structurees['montant_pret_demande'] = montant_pret_demande.text if montant_pret_demande is not None else ''
        # Continuez d'extraire et de stocker d'autres informations

    except ET.ParseError as e:
        # Gérer les erreurs d'analyse XML
        return {'erreur': 'Erreur d\'analyse XML: ' + str(e)}
    except Exception as e:
        # Gérer d'autres erreurs possibles
        return {'erreur': 'Erreur inattendue: ' + str(e)}

    return informations_structurees

if __name__ == '__main__':
    application = Application([ServiceExtractionInformation],
                              tns='votre_namespace',
                              in_protocol=Soap11(validator='lxml'),
                              out_protocol=Soap11())

    wsgi_app = WsgiApplication(application)

    twisted_apps = [
        (wsgi_app, b'ServiceExtractionInformation')
    ]

    sys.exit(run_twisted(twisted_apps, 8000))
