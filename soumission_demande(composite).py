from suds.client import Client
from suds import WebFault

# Créez un client SOAP pour votre service
url = "http://localhost:8000/ServiceExtractionInformation?wsdl"  # Assurez-vous d'ajuster l'URL de votre service WSDL
client = Client(url)

# data prend la valeur du XML à envoyer 'johndoe.xml'
data = 'johndoe.xml'

try:
    # Appelez la méthode du service en lui passant le JSON comme argument
    response = client.service.ExtraireInformations(data)

    # Vérifiez la réponse du service
    print("Réponse du service:")
    print(response)
except WebFault as e:
    # En cas d'erreur, imprimez le message d'erreur
    print(f"Erreur lors de l'appel au service : {e}")
except Exception as e:
    # Gérez d'autres exceptions possibles ici
    print(f"Une erreur s'est produite : {e}")
