import abc
import psycopg2
import metier

class AbstractDatabase(abc.ABC):
    
    @abc.abstractmethod
    def get_body_type(self):
        pass

    @abc.abstractmethod
    def connexion(self):
        pass

    @abc.abstractmethod
    def add_client(self, client: metier.Client):
        pass

    @abc.abstractmethod
    def get_all_clients(self):
        pass

    @abc.abstractmethod
    def get_client(self, id):
        pass


class PostgresDB(AbstractDatabase):

    def __init__(self):
        self.connector = None
        self.cursor = None
        self.connexion()
        self.create_client_table_if_not_exist()
        self.connected = False

    def connexion(self):
        try:
            self.connector = psycopg2.connect(
                host="127.0.0.1",
                database="my_company_db",
                user="postgres",
                password="password",
                port="5432"
            )
            self.cursor = self.connector.cursor()
            self.connected = True
        except:
            print("connection impossible")

    def add_client(self, newClient: metier.Client):
        self.cursor.execute("INSERT INTO clients(firstName, lastName, emailId) values(%s,%s,%s)",(newClient.firstName, newClient.lastName, newClient.emailId))
        self.connector.commit()

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM clients")
        res = self.cursor.fetchall()
        ret = []
        for row in res:
            new_row = { 'id': row[0], 'firstName': row[1], 'lastName':row[2], 'emailId':row[3]}
            ret.append(new_row)

        return ret

    def get_client(self, id):
        self.cursor.execute("SELECT * FROM clients WHERE id=%s", str(id))
        res = self.cursor.fetchall()
        if(len(res) == 0):
            return None
        return res[0]

    def create_client_table_if_not_exist(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS clients (id serial NOT NULL PRIMARY KEY, firstName varchar(255) NOT NULL, lastName varchar(255) NOT NULL, emailId varchar(255) NOT NULL);')
        self.connector.commit()

    def get_body_type(self):
        return "test"
    
class JsonDB(AbstractDatabase):
    
    def __init__(self):
        pass
        
    def get_body_type(self):
        pass

class DatabaseFactory():
    
    def build_db(plan):
        try:
            if plan == "postgres":
                return PostgresDB()
            elif plan == "json":
                return JsonDB()
            raise AssertionError("Type is not valid.")
        except AssertionError as e:
            print(e)

if(__name__ == "__main__"):
    db = DatabaseFactory.build_db("postgres")
    newone = metier.Client("fn", "ln", "email@email.com")
    db.add_client(newone)
