import sqlite3 ,os
System = f"{os.path.dirname(os.path.abspath(__file__))}\System.db"
db = sqlite3.connect(System)
cur = db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Users(Username Text , Password Text , Type Int)")

cur.execute("CREATE TABLE IF NOT EXISTS Clients(Id Int ,Username Text , Password Text , Email Text , Address Text , MobileNumber Int , Birthday Date , OrdersNumber Int , Points Int)")

cur.execute("CREATE TABLE IF NOT EXISTS Items(Id Int ,Name Text ,Brand Text ,Category Text , Price Int ,Image Text ,Description Text ,Commission Text ,Discount Int)")

cur.execute("CREATE TABLE IF NOT EXISTS Orders(OrderId int , ClientId Int , Total Int , Address Text , Name Text , Mobile Int, OrderDate Date , OrderTime Time , BuyingMethod Text)")



db.commit()
db.close()