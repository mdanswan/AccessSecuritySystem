# check if is installed
import pymysql as my

HOST = 'accesssecuritysystem.cxa5ja6qsxdg.us-east-2.rds.amazonaws.com'
USER = 'miles'
PASS = 'ass1916m!'
DB = 'access'

class Database(my):
    
    def __init__(self, host, user, password, db):
        self.HOST = host
        self.USER = user
        self.PASS = password
        self.DB = db
        
    def connect(self):
        try:
            self.conn = my.connect(self.HOST, self.USER, self.PASSWORD, self.DB)
            self.cursor = my.cursor()
        except:
            print("Unable to make a connection to the server")
            
    def query(self, query_string):
        if (not self.conn.open):
            self.connect()
        if (self.conn.open):
            results = None
            try:
                self.cursor.execute(query_string)
                results = self.cursor.fetchall()
                self.conn.commit()
                self.conn.close()
            except:
                print("Unable to execute query")
                self.conn.rollback()
        return results
 
# test
db = Database(HOST, USER, PASS, DB)
db.connect()
db.query("INSERT INTO `owner` (name) VALUES ('owner')");
            
