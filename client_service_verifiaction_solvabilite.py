from suds.client import Client

if __name__ == '__main__':
    client = Client('http://localhost:8000/verifSolvabilite?wsdl', cache=None)
    id = client.service.getClientId('Doe', 'John')
    score = client.service.calculateScore(id, 1000, 1000)
    print(score)