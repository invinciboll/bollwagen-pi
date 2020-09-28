import sqlite3

#c.execute("DROP TABLE Person")
# c.execute("""CREATE TABLE Person (
#        name TEXT NOT NULL,
#        rfid TEXT,
#        balance REAL DEFAULT 0.00
#        )
#    """)


class Database:
    def __init__(self, connectionName):
        self.connectionName = connectionName

    def connect(self):
        self.conn = sqlite3.connect(self.connectionName)
        self.c = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def insertPerson(self, name, rfid):
        self.connect()
        self.c.execute("INSERT INTO Person VALUES (:name, :rfid)",
                       {'name': name, 'rfid': rfid})
        self.close()

    def getBalance(self, rfid):
        self.connect()
        self.c.execute("SELECT balance FROM Person WHERE rfid = :rfid",
                       {'rfid': rfid})
        balance = self.c.fetchall()
        self.close()
        return balance

    def setBalance(self, rfid, balance):
        self.connect()
        self.c.execute("INSERT INTO Person VALUES (:balance) WHERE rfid = :rfid", {
            'balance': balance, 'rfid': rfid})
        self.close()
        return self.getBalance(rfid)
