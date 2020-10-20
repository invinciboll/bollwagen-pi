import sqlite3
from interfaces.repository import Database


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

if False:
    c.execute("INSERT INTO Person VALUES ('Christian','385650702521',135.50)")
    conn.commit()

if False:
    c.execute("DROP TABLE Purchase")
    c.execute("""CREATE TABLE Purchase (
        rfid TEXT NOT NULL,
        drinkSum INTEGER DEFAULT 0,
        hookahSum INTEGER DEFAULT 0,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """)

    c.execute(
        "INSERT INTO Purchase(rfid, drinkSum, hookahSum) VALUES ('1048046807727',4,3)")
    c.execute(
        "INSERT INTO Purchase(rfid, drinkSum, hookahSum) VALUES ('1048046807727',1,4)")
    c.execute(
        "INSERT INTO Purchase(rfid, drinkSum, hookahSum) VALUES ('1048046807727',5,0)")
    c.execute("SELECT * FROM Purchase")
    print(c.fetchall())
    conn.commit()


class user:
    def __init__(self, name, balance, drinkSum, hookahSum):
        self.name = name
        self.balance = balance
        self.drinkSum = drinkSum
        self.hookahSum = hookahSum
        self.totalExpenses = drinkSum * 1 + hookahSum * 1.5


if False:
    rfid = '1048046807727'
    c.execute(f"SELECT Name, Balance FROM Person WHERE rfid = {rfid}")
    res1 = c.fetchone()

    c.execute(
        f"SELECT SUM(drinkSum), SUM(hookahSum) FROM Purchase WHERE rfid = {rfid}")
    res2 = c.fetchone()

    u = user(res1[0], res1[1], res2[0], res2[1])
    print(
        f"User: {u.name}\nBalance: {u.balance}€\nDrinks: {u.drinkSum}\nHookahs: {u.hookahSum}")
    conn.commit()

if False:
    rfid = '1048046807727'
    c.execute(
        f"SELECT timestamp, drinkSum, hookahSum FROM Purchase WHERE rfid={rfid} ORDER BY timestamp DESC LIMIT 5")
    res1 = c.fetchall()
    print(res1)
    conn.commit()

if True:
    rfid = '1048046807727'
    db = Database("database.db")
    name = db.get_name(rfid)
    print(name)
    
    db.setBalance(rfid, 20)

    sta_life = db.get_statistic(rfid, 'lifetime')
    print("Lifetime: ", sta_life)

    sta_year = db.get_statistic(rfid, 'year')
    print("Year: ", sta_year)

    sta_year = db.get_statistic(rfid, 'month')
    print("Month: ", sta_year)

    sta_year = db.get_statistic(rfid, 'week')
    print("Week: ", sta_year)

