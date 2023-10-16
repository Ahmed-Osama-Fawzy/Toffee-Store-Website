import sqlite3 , os 
class DB:
    Tablename = ''
    DBName = ''

    def __init__(self , T):
        self.DBName = f"{os.path.dirname(os.path.abspath(__file__))}\System.db"
        self.Tablename = T

    def Create(self ,*Data):
        try:
            with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                M = ''
                for One in Data:
                    M += f"{One[0]} {One[1]} {One[2]},"
                M.rstrip(",")
                cur.execute(f"CREATE TABLE IF NOT EXISTS {self.Tablename}({M})")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
    
    
    def SelectAll(self):
        try:
            with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                cur.execute(f"SELECT * FROM {self.Tablename}")
                data = [list(tup) for tup in cur.fetchall()]
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        return data
    
    
    
    def SelectAllWhere(self , Key , Value, Numrical = True):
        try:
            with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                if Numrical == True:
                    cur.execute(f"SELECT * FROM {self.Tablename} WHERE {Key} = {Value}")
                else:
                    cur.execute(f"SELECT * FROM {self.Tablename} WHERE {Key} = '{Value}'")
                data = [list(tup) for tup in cur.fetchall()]
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        return data
    
    def SelectAllTWhere(self , Key , Value, Numrical , XKey , XValue , XNumrical ):
        try:
            with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                if Numrical == True and XNumrical == True:
                    cur.execute(f"SELECT * FROM {self.Tablename} WHERE {Key} = {Value} AND {XKey} = {XValue}")

                elif Numrical == False and XNumrical == False:
                    cur.execute(f"SELECT * FROM {self.Tablename} WHERE {Key} = '{Value}' AND {XKey} = '{XValue}'")

                elif Numrical == False and XNumrical == True:
                    cur.execute(f"SELECT * FROM {self.Tablename} WHERE {Key} = '{Value}' AND {XKey} = {XValue}")

                elif Numrical == True and XNumrical == False:
                    cur.execute(f"SELECT * FROM {self.Tablename} WHERE {Key} = {Value} AND {XKey} = '{XValue}'")

                data = [list(tup) for tup in cur.fetchall()]
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        return data
    
    
    
    def SelectOneWhere(self , One , Key , Value, Numrical = True):
        try:
            with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                if Numrical == True:
                    cur.execute(f"SELECT {One} FROM {self.Tablename} WHERE {Key} = {Value}")
                else:
                    cur.execute(f"SELECT {One} FROM {self.Tablename} WHERE {Key} = '{Value}'")
                data = [list(tup) for tup in cur.fetchall()]
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        d = data[0][0]
        return d
    
    def SelectOneTWhere(self , One , Key , Value, Numrical , XKey , XValue , XNumrical ):
        try:
            with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                if Numrical == True and XNumrical == True:
                    cur.execute(f"SELECT {One} FROM {self.Tablename} WHERE {Key} = {Value} AND {XKey} = {XValue}")

                elif Numrical == False and XNumrical == False:
                    cur.execute(f"SELECT {One} FROM {self.Tablename} WHERE {Key} = '{Value}' AND {XKey} = '{XValue}'")

                elif Numrical == False and XNumrical == True:
                    cur.execute(f"SELECT {One} FROM {self.Tablename} WHERE {Key} = '{Value}' AND {XKey} = {XValue}")

                elif Numrical == True and XNumrical == False:
                    cur.execute(f"SELECT {One} FROM {self.Tablename} WHERE {Key} = {Value} AND {XKey} = '{XValue}'")

                data = [list(tup) for tup in cur.fetchall()]
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        d = data[0][0]
        return d
        

    
    def SelectManyWhere(self , *Many , Key , Value, Numrical = True):
        try:
            with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                M = ''
                for One in Many:
                    M += f"{One},"
                M.rstrip(",")
                if Numrical == True:
                    cur.execute(f"SELECT {M} FROM {self.Tablename} WHERE {Key} = {Value}")
                else:
                    cur.execute(f"SELECT {M} FROM {self.Tablename} WHERE {Key} = '{Value}'")
                data = cur.fetchall()
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        return data
    

    def InsertAll(self , *Many):
        try:
           with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                M = ''
                for One in Many:
                    if One[1] == True:
                        M+=f"'{One[0]}',"
                    else:
                        M+=f"{One[0]},"
                M.rstrip(",")
                cur.execute(f"INSERT INTO {self.Tablename} VALUES({M})")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
    

    def InsertOne(self ,Key , Value , Numrical ):
        try:
           with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                if Numrical == True:
                    cur.execute(f"INSERT INTO {self.Tablename}({Key}) VALUES({Value})")
                else:
                    cur.execute(f"INSERT INTO {self.Tablename}({Key}) VALUES('{Value}')")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        


    def DropTable(self):
        try:
           with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                cur.execute(f"DROP TABLE IF EXISTS {self.Tablename}")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()



    def ClearTable(self):
        try:
           with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                cur.execute(f"DELETE FROM {self.Tablename}")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()



    def DeleteAllWhere(self ,Key , Value , Numrical ):
        try:
           with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                if Numrical == True:
                    cur.execute(f"DELETE FROM {self.Tablename} WHERE {Key} = {Value}")
                else:
                    cur.execute(f"DELETE FROM {self.Tablename} WHERE {Key} = '{Value}'")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()



    def UpdateOne(self , Key , Value , Numrical , XKey , XValue , XNumarical ):
        try:
           with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                if Numrical == True and XNumarical == True:
                    cur.execute(f"UPDATE {self.Tablename} SET {Key} = {Value} WHERE {XKey} = {XValue}")

                elif Numrical == False and XNumarical == False:
                    cur.execute(f"UPDATE {self.Tablename} SET {Key} = '{Value}' WHERE {XKey} = '{XValue}'")
                
                elif Numrical == True and XNumarical == False:
                    cur.execute(f"UPDATE {self.Tablename} SET {Key} = {Value} WHERE {XKey} = '{XValue}'")

                elif Numrical == False and XNumarical == True:
                    cur.execute(f"UPDATE {self.Tablename} SET {Key} = '{Value}' WHERE {XKey} = {XValue}")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()



    def UpdateMany(self ,*Many , XKey , XValue , XNumarical ):
        try:
           with sqlite3.connect(self.DBName) as con :
                cur = con.cursor()
                for One in Many:
                    if One[2] == True and XNumarical == True:
                        cur.execute(f"UPDATE {self.Tablename} SET {One[0]} = {One[1]} WHERE {XKey} = {XValue}")

                    elif One[2] == False and XNumarical == False:
                        cur.execute(f"UPDATE {self.Tablename} SET {One[0]} = '{One[1]}' WHERE {XKey} = '{XValue}'")
                    
                    elif One[2] == True and XNumarical == False:
                        cur.execute(f"UPDATE {self.Tablename} SET {One[0]} = {One[1]} WHERE {XKey} = '{XValue}'")

                    elif One[2] == False and XNumarical == True:
                        cur.execute(f"UPDATE {self.Tablename} SET {One[0]} = '{One[1]}' WHERE {XKey} = {XValue}")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()

    

