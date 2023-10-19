from suds.client import Client
from suds import WebFault


if __name__ == '__main__':

    # Créez un client SOAP pour votre service
    url = "http://localhost:8002/DemandePret?wsdl"
    client = Client(url, cache=None)

    # data prend la valeur du XML à envoyer 'johndoe.xml'
    # Lisez le contenu du fichier XML de la demande
    data = 'johndoe.xml'

    try:
        # Appelez la méthode du service en lui passant le XML comme argument
        response = client.service.demandePret(data)

        # Vérifiez la réponse du service
        if response:
            print("Réponse du service DemandePret:")
            print(response)
        else:
            print("La réponse du service est vide.")
    except WebFault as e:
        # En cas d'erreur, imprimez le message d'erreur
        print(f"Erreur lors de l'appel au service : {e}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
