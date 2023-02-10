import re
import string

class Client:
    def __new__(self, firstName, lastName, emailId):
        if(self.__is_valid_firstName(firstName)):
            self.firstName = firstName
        if(self.__is_valid_lastName(lastName)):
            self.lastName = lastName
        if(self.__is_valid_emailId(emailId)):
            self.emailId = emailId
        
        self.accountBalance = None
        self.accountId = None

    def __has_numbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def __is_resistant_sql_injection(self, inputString):
        if "'" in inputString:
            return False,"Nice try."
        return True,""

    def __without_special_characters(self, inputString):
        if(set(inputString).difference(string.ascii_letters)):
            return False,"No special characters allowed."
        return True,""

    def __is_valid_firstName(self, firstName):
        """check if firstName is valid
        return is a tuple val,msg
        if it's valid msg is empty
        if it's not valid a msg is returned
        ex : 
        valid first name :
          return True, ''
        invalid first name:
          return False, 'Bad first name length.'
        """
        lon = len(firstName)
        if(lon < 2 or lon > 15):
            return False,"Bad first name length."
        if(" " in firstName):
            return False, "Composed first names not allowed"
        if(self.__has_numbers(firstName)):
            return False, "Numeric characters in first name are not allowed"
        return True, ""

    def __is_valid_lastName(self, lastName):
        """check if lastName is valid
        return is a tuple val,msg
        if it's valid msg is empty
        if it's not valid a msg is returned
        ex : 
        valid last name :
          return True, ''
        invalid last name:
          return False, 'Bad first name length.'
        """
        lon = len(lastName)
        if(lon < 2 or lon > 15):
            return False,"Bad last name length."
        if(" " in lastName):
            return False, "Composed last names not allowed."
        if(self.__has_numbers(lastName)):
            return False, "Numeric characters in last name are not allowed."
        return True, ""

    def __is_valid_emailId(self, emailId):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex,emailId)):
            return True,""
        return False,"Invalid mail address."

if(__name__ == "__main__"):
    myClient = Client("fn", "ln", "emailid")
    print(myClient.firstName)
