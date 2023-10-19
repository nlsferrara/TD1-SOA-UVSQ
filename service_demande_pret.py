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
        
def lecture_bdd(xml_db):

    root = ET.parse(xml_db).getroot()
    prenom_client = root.find('.//PrenomClient')
    prenom_client = prenom_client.text if prenom_client is not None else ''
    nom_client = root.find('.//NomClient')
    nom_client = nom_client.text if nom_client is not None else ''
    adresse_rue = root.find('.//Adresse/Rue')
    adresse_rue = adresse_rue.text if adresse_rue is not None else ''
    adresse_ville = root.find('.//Adresse/Ville')
    adresse_ville = adresse_ville.text if adresse_ville is not None else ''
    adresse_code_postal = root.find('.//Adresse/CodePostal')
    adresse_code_postal = adresse_code_postal.text if adresse_code_postal is not None else ''
    adresse_pays = root.find('.//Adresse/Pays')
    adresse_pays = adresse_pays.text if adresse_pays is not None else ''
    email = root.find('.//Email')
    email = email.text if email is not None else ''
    numero_telephone = root.find('.//NumeroTelephone')
    numero_telephone = numero_telephone.text if numero_telephone is not None else ''
    montant_pret_demande = root.find('.//MontantPretDemande')
    montant_pret_demande = int(montant_pret_demande.text) if montant_pret_demande is not None else 0
    duree_pret = root.find('.//DureePret')
    duree_pret = int(duree_pret.text) if duree_pret is not None else 0
    description_propriete_etage = root.find('.//DescriptionPropriete/Etage')
    description_propriete_etage = description_propriete_etage.text if description_propriete_etage is not None else ''
    description_propriete_taille = root.find('.//DescriptionPropriete/Taille')
    description_propriete_taille = description_propriete_taille.text if description_propriete_taille is not None else ''
    description_propriete_jardin = root.find('.//DescriptionPropriete/Jardin')
    description_propriete_jardin = description_propriete_jardin.text if description_propriete_jardin is not None else ''
    description_propriete_quartier = root.find('.//DescriptionPropriete/Quartier')
    description_propriete_quartier = description_propriete_quartier.text if description_propriete_quartier is not None else ''
    description_propriete_tranquilite = root.find('.//DescriptionPropriete/Tranquilite')
    description_propriete_tranquilite = description_propriete_tranquilite.text if description_propriete_tranquilite is not None else ''
    revenu_mensuel = root.find('.//RevenuMensuel')
    revenu_mensuel = int(revenu_mensuel.text) if revenu_mensuel is not None else 0
    depenses_mensuelles = root.find('.//DepensesMensuelles')
    depenses_mensuelles = int(depenses_mensuelles.text) if depenses_mensuelles is not None else 0
    informations_structurees = {
        'PrenomClient': prenom_client,
        'NomClient': nom_client,
        'Adresse': {
            'Rue': adresse_rue,
            'Ville': adresse_ville,
            'CodePostal': adresse_code_postal,
            'Pays': adresse_pays
        },
        'Email': email,
        'NumeroTelephone': numero_telephone,
        'MontantPretDemande': montant_pret_demande,
        'DureePret': duree_pret,
        'DescriptionPropriete': {
            'Etage': description_propriete_etage,
            'Taille': description_propriete_taille,
            'Jardin': description_propriete_jardin,
            'Quartier': description_propriete_quartier,
            'Tranquilite': description_propriete_tranquilite
        },
        'RevenuMensuel': revenu_mensuel,
        'DepensesMensuelles': depenses_mensuelles
    }
    return informations_structurees

def to_service_verification_solvabilite(lecture_xml_db):

    informations_structurees = lecture_xml_db

    root = ET.Element('DemandePret')
    prenom_client = ET.SubElement(root, 'PrenomClient')
    prenom_client.text = informations_structurees['PrenomClient']
    nom_client = ET.SubElement(root, 'NomClient')
    nom_client.text = informations_structurees['NomClient']
    revenu_mensuel = ET.SubElement(root, 'RevenuMensuel')
    revenu_mensuel.text = str(informations_structurees['RevenuMensuel'])
    depenses_mensuelles = ET.SubElement(root, 'DepensesMensuelles')
    depenses_mensuelles.text = str(informations_structurees['DepensesMensuelles'])
    tree = ET.tostring(root)
    return tree.decode('utf-8')

def to_service_evaluation_propriete(informations_structurees):
    evaluation_propriete_service = ServiceEvaluationPropriete()
    resultat_evaluation_propriete = evaluation_propriete_service.EvaluerPropriete(informations_structurees)


class DemandePret(ServiceBase):

    @rpc(Unicode, _returns=Unicode)
    def demandePret(ctx, demande_xml):
        try:
            xml_db = getExtractInfo(demande_xml)
            infoClient = lecture_bdd(xml_db)
            infoClientSolv = to_service_verification_solvabilite(infoClient)
            scoreSolvabilite = getScoringPret(infoClientSolv)
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
