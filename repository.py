import sqlite3
from datetime import datetime, date, timedelta


class user:
    def __init__(self, name, balance, drinkSum, hookahSum):
        self.name = name
        self.balance = balance
        self.drinkSum = drinkSum if drinkSum is not None else 0
        self.hookahSum = hookahSum if hookahSum is not None else 0
        self.totalExpenses = self.drinkSum * 1 + self.hookahSum * 1.5


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

    def get_name(self, rfid):
        self.connect()
        self.c.execute("SELECT name FROM Person WHERE rfid = :rfid",
                       {'rfid': rfid})
        res = self.c.fetchone()
        self.close()
        return res[0]

    def get_statistic(self, rfid, interval):
        self.connect()
        if interval == "lifetime":
            self.c.execute(
                f"SELECT SUM(drinkSum), SUM(hookahSum) FROM Purchase WHERE rfid = {rfid}")
        elif interval == "year":
            last_accepted_timestamp = datetime.now() - timedelta(days=365)
            self.c.execute(
                f"SELECT SUM(drinkSum), SUM(hookahSum) FROM Purchase WHERE rfid = {rfid} AND timestamp >= '{last_accepted_timestamp}'")
        elif interval == "month":
            last_accepted_timestamp = datetime.now() - timedelta(days=31)
            self.c.execute(
                f"SELECT SUM(drinkSum), SUM(hookahSum) FROM Purchase WHERE rfid = {rfid} AND timestamp >= '{last_accepted_timestamp}'")
        elif interval == "week":
            last_accepted_timestamp = datetime.now() - timedelta(days=7)
            self.c.execute(
                f"SELECT SUM(drinkSum), SUM(hookahSum) FROM Purchase WHERE rfid = {rfid} AND timestamp >= '{last_accepted_timestamp}'")

        res = self.c.fetchone()
        self.close()
        if res is not None: 
            return res
        else:
            return [0,0]

    def getAccountInformation(self, rfid):
        self.connect()
        self.c.execute(f"SELECT Name, Balance FROM Person WHERE rfid = {rfid}")
        res1 = self.c.fetchone()

        self.c.execute(
            f"SELECT SUM(drinkSum), SUM(hookahSum) FROM Purchase WHERE rfid = {rfid}")
        res2 = self.c.fetchone()

        u = user(res1[0], res1[1], res2[0], res2[1])
        print(
            f"User: {u.name}\nBalance: {u.balance}€\nDrinks: {u.drinkSum}\nHookahs: {u.hookahSum}")
        self.close()
        return u

    def insertPurchase(self, rfid, drinkSum, hookahSum):
        self.connect()
        self.c.execute(
            f"INSERT INTO Purchase(rfid, drinkSum, hookahSum) VALUES ({rfid},{drinkSum},{hookahSum})")
        self.close()

    def get_purchase_history(self, rfid):
        self.connect()
        self.c.execute(
            f"SELECT timestamp, drinkSum, hookahSum FROM Purchase WHERE rfid={rfid} ORDER BY timestamp DESC LIMIT 10")
        res = self.c.fetchall()
        self.close()
        return res
