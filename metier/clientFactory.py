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

if(__name__ == "__main__"):
    json_ex = {'firstName': 'fn', 'lastName': 'ln', 'emailId': 'emalalalail@test.fr'}

    print(len(json_ex))
    print(json_ex['firstName'])
    print(json_ex['test'])
