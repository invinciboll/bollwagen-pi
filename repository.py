import sqlite3

if False:
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    if False:
        c.execute("DROP TABLE Person")
        c.execute("""CREATE TABLE Person (
            name TEXT NOT NULL,
            rfid TEXT,
            balance REAL DEFAULT 0.00
            )
        """)
        c.execute("INSERT INTO Person VALUES ('Sebastian','1048046807727',19.75)")
        conn.commit()

    if False:
        c.execute("SELECT * FROM Person")
        print(c.fetchall())
        conn.commit()

    if True:
        c.execute("INSERT INTO Person VALUES ('Christian','385650702521',135.50)")
        conn.commit()


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
        balance = self.c.fetchone()
        self.close()
        return balance[0]

    def setBalance(self, rfid, balance):
        self.connect()
        self.c.execute("UPDATE Person SET balance = :balance WHERE rfid = :rfid", {
            'balance': balance, 'rfid': rfid})
        self.close()
        return self.getBalance(rfid)
