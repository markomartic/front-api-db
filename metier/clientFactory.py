import metier

class ClientFactory():

    def json2client(json):
        if(len(json) != 3):
            return None
        if("firstName" not in json):
            return None
        if("lastName" not in json):
            return None
        if("emailId" not in json):
            return None
        new_client = metier.Client(json['firstName'], json['lastName'], json['emailId'])
        return new_client

if(__name__ == "__main__"):
    json_ex = {'firstName': 'fn', 'lastName': 'ln', 'emailId': 'emalalalail@test.fr'}

    new_client = metier.ClientFactory.json2client(json_ex)
    print(new_client.firstName)
