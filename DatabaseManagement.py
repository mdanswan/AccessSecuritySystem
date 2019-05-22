import pymysql as my

class Database:
    
    def __init__(self, host, port, user, password, db):
        self.HOST = host
        self.PORT = port
        self.USER = user
        self.PASS = password
        self.DB = db
        
    def connect(self):
        try:
            conn = my.connect(self.HOST, self.USER, self.PASS, self.DB, self.PORT)
            return conn
        except Exception as e:
            print("Unable to make a connection to the server: {}".format(e))
            
    def query(self, query_string):
        conn = self.connect()
        
        if conn is None:
            print("No connection available")
            return None
            
        results = None
        try:
            with conn.cursor() as cur:
                cur.execute(query_string)
                results = cur.fetchall()
            conn.commit()
        except Exception as e:
            print("Unable to execute query: {}".format(e))
            conn.rollback()
        finally:
            conn.close()
            
        return results
