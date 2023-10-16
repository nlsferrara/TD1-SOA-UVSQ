from suds.client import Client
from suds import WebFault
import json

# Créez un client SOAP pour votre service
url = "http://localhost:8000/ServiceExtractionInformation?wsdl"  # Assurez-vous d'ajuster l'URL de votre service WSDL
client = Client(url)

# data prend la valeur du JSON à envoyer 'johndoe.json'
data = json.load(open('johndoe.json'))

try:
    # Appelez la méthode du service en lui passant le JSON comme argument
    response = client.service.ExtraireInformations(json.dumps(data))

    # Vérifiez la réponse du service
    print("Réponse du service:")
    print(response)
except WebFault as e:
    # En cas d'erreur, imprimez le message d'erreur
    print(f"Erreur lors de l'appel au service : {e}")
except Exception as e:
    # Gérez d'autres exceptions possibles ici
    print(f"Une erreur s'est produite : {e}")
