from flask import Flask,render_template,request
from jinja2 import Template
import sqlite3 , os , DB , math , random , smtplib , time

app = Flask(__name__)


def SelectAll(TableName):
    db = sqlite3.connect(DB.System)
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {TableName}")
    data = [list(tup) for tup in cur.fetchall()]
    db.commit()
    db.close()
    return data

def GetOneWhere(data , TableName , Key , Value , Numrical):
    db = sqlite3.connect(DB.System)
    cur = db.cursor()
    if Numrical == True:
        cur.execute(f"SELECT {data} FROM {TableName} WHERE {Key} = {Value}")
    elif Numrical == False:
        cur.execute(f"SELECT {data} FROM {TableName} WHERE {Key} = '{Value}'")
    else:
        cur.execute(f"SELECT {data} FROM {TableName} WHERE {Key} = '{Value}'")
    data = [list(tup) for tup in cur.fetchall()]
    db.commit()
    db.close()
    return data[0][0]

def GetAllWhere(TableName , Key , Value , Numrical):
    db = sqlite3.connect(DB.System)
    cur = db.cursor()
    if Numrical == True:
        cur.execute(f"SELECT * FROM {TableName} WHERE {Key} = {Value}")
    elif Numrical == False:
        cur.execute(f"SELECT * FROM {TableName} WHERE {Key} = '{Value}'")
    else:
        cur.execute(f"SELECT * FROM {TableName} WHERE {Key} = '{Value}'")
    data = [list(tup) for tup in cur.fetchall()]
    db.commit()
    db.close()
    return data

############################################################################
############### Controlling Functions


@app.route('/', methods=["POST","GET"])
def HomePage():
    Items = SelectAll("Items")
    return render_template('Home Page.html', title="Toffee Home Page" , User = "Visitor" , Status = 0 , Items = Items)

############## Login Functions
@app.route('/Login' , methods=["POST","GET"])
def LogIn():
    return render_template('Controlling Side/Log In Page.html', title="Log In Page" , User = "Visitor" , Status = 0)

@app.route('/AccessToAccount' , methods = ["POST" , "GET"])
def AccessToAccount():
    if request.method == "POST":
        try:
            Username = request.form.get("Username")
            Password = request.form.get("Password")
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()
                cur.execute(f"SELECT Type FROM Users WHERE Username= '{Username}' AND Password = '{Password}'")
                Result = [list(tup) for tup in cur.fetchall()]
                cur.execute(f"SELECT Id FROM Clients WHERE Username= '{Username}' AND Password = '{Password}'")
                Id = [list(tup) for tup in cur.fetchall()]
                if Result:
                    if int(Result[0][0]) == 1:
                        Items = SelectAll("Items")
                        return render_template('Home Page.html', title="Client Home Page" , User = "Client" , Status = 1 , Name = Username , CId = int(Id[0][0]) , Items = Items)
                    elif int(Result[0][0]) == 2:
                        return render_template('Home Page.html', title="Admin Home Page" , User = "Admin" , Status = 1 , Name = Username)
                    elif int(Result[0][0]) == 3:
                        return render_template('Home Page.html', title="Owner Home Page" , User = "Owner" , Status = 1 , Name = Username)
                    else:
                        return render_template('Error.html', title="Error Page" , User = "Visitor" , Status = 0)
                else:
                    return render_template('Error.html', title="Error Page" , User = "Visitor" , Status = 0 , Number = Result)
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()

@app.route('/ForgetPassword'  , methods = ["POST" , "GET"])
def ForgetPassword():
    return render_template('Controlling Side/Forget Password Page.html', title="Forget Password Page" , User = "Visitor" , Status = 0)

def GenrateOTP():
    digits="0123456789"
    OTP=""
    for i in range(6):
        OTP+=digits[math.floor(random.random()*10)]
    return OTP

OTPCode = GenrateOTP()

@app.route('/SendOTP'  , methods = ["POST" , "GET"])
def SendOTP():
    if request.method == "POST":
        Email = request.form.get("Email")
        msg = OTPCode + " is your OTP Code"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('ahmd.osama2611@gmail.com', 'yvhvsvqismmbfwiz')
        s.sendmail('ahmd.osama2611@gmail.com',Email,msg)
        s.quit()
    return render_template('Controlling Side/OTP Page.html', title="OTP Page" , User = "Visitor" , Status = 0)

@app.route('/GetOTP'  , methods = ["POST" , "GET"])
def GetOTP():
    if request.method == "POST":
        otpCode = request.form.get("OTP")
        if otpCode == OTPCode:
            return render_template('Controlling Side/Username Page.html', title="OTP Page" , User = "Visitor" , Status = 0)
        else:
            return render_template('Error.html', title="Error Page" , User = "Visitor" , Status = 0)

@app.route('/GetUsername'  , methods = ["POST" , "GET"])
def GetUsername():
    if request.method == "POST":
        Username = request.form.get("Username")
    return render_template('Controlling Side/Set New Password Page.html', title="OTP Page" , User = "Visitor" , Status = 0 , Username = Username)

@app.route('/SetPassword'  , methods = ["POST" , "GET"])
def SetPassword():
    if request.method == "POST":
        Username = request.form.get("Username")
        NewPassword = request.form.get("NewPassword")
        RenewPassword = request.form.get("RenewPassword")
        with sqlite3.connect(DB.System) as con:
            cur = con.cursor()
            data = GetOneWhere("Type" , "Users" , "Username" , Username , False)
            if data == 1:
                cur.execute(f"UPDATE Clients SET Password = '{NewPassword}' WHERE Username = '{Username}'")
            if NewPassword == RenewPassword:
                cur.execute(f"UPDATE Users SET Password = '{NewPassword}' WHERE Username = '{Username}'")
            con.commit()
    return render_template('Controlling Side/Log In Page.html', title="Log In Page" , User = "Visitor" , Status = 0)

############# Sign Up Functions
@app.route('/Signup' , methods=["POST","GET"])
def SignUp():
    return render_template('Controlling Side/Sign Up Page.html', title="Sign Up Page" , User = "Visitor" , Status = 0)

@app.route('/NewAccount' , methods = ["POST" , "GET"])
def NewAccount():
    if request.method == "POST":
        try:
            Username = request.form.get("Username")
            Password = request.form.get("Password")
            Email = request.form.get("Email")
            Address = request.form.get("Address")
            Mobile = request.form.get("Mobile")
            Birthday = request.form.get("Birthday")
            Id = len(SelectAll("Clients"))
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO Clients VALUES({Id},'{Username}','{Password}','{Email}','{Address}',{Mobile},'{Birthday}',0 , 5)")
                cur.execute(f"INSERT INTO Users VALUES('{Username}' , '{Password}' , 1)")
                cur.execute(f"CREATE TABLE IF NOT EXISTS C{Id}(OrderId Int , Id Int ,Name Text ,Brand Text ,Category Text , Price Int ,Image Text ,Description Text ,Commission Text ,Discount Int , Amount Int , Total Int GENERATED ALWAYS AS (Price*Amount*Discount/100))")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
    return render_template('Controlling Side/Log In Page.html', title="Log In Page" , User = "Visitor" , Status = 0)
   

@app.route('/PublicStore' , methods=["POST","GET"])
def PublicStore():
    Items = SelectAll("Items")
    return render_template('Controlling Side/Public Store Page.html', title="Public Store Page" , User = "Visitor" , Status = 0 , Items = Items)

@app.route('/SignOut')
def SignOut():
    return render_template('Home Page.html', title="Toffee Home Page" , User = "Visitor" , Status = 0)

@app.route('/ChangePassword' , methods=["POST","GET"])
def ChangePassword():
    if request.method == "POST":
        try:
            Username = request.form.get("Username")
            UserType = int(request.form.get("UserType"))
            OldPassword = request.form.get("OldPassword")
            NewPassword = request.form.get("NewPassword")
            RenewPassword = request.form.get("RenewPassword")
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()
                if UserType == 1:
                    data = GetOneWhere("Password" , "Users" , "Username" , Username , False)
                    if OldPassword == data:
                        if NewPassword == RenewPassword:
                            cur.execute(f"UPDATE Users SET Password = '{NewPassword}' WHERE Username = '{Username}' AND Password = '{OldPassword}'")
                            cur.execute(f"UPDATE Clients SET Password = '{NewPassword}' WHERE Username = '{Username}' AND Password = '{OldPassword}'")
                            Xdata = GetOneWhere("Id" , "Clients" , "Username" , Username , False)
                            return render_template('Home Page.html', title="Client Home Page" , User = "Client" , Status = 1 , Name = Username, CId = Xdata)
                    else:
                        return render_template("Error.html" , title = "Error Page" , User = "Client" ,  Status = 1)
                elif UserType == 2:
                    data = GetOneWhere("Password" , "Users" , "Username" , Username , False)
                    if OldPassword == data:
                        if NewPassword == RenewPassword:
                            cur.execute(f"UPDATE Users SET Password = '{NewPassword}' WHERE Username = '{Username}' AND Password = '{OldPassword}'")
                            return render_template("Admin Side/Admin Profile Page.html" , title = "Admin Profile Page" , User = "Admin" ,  Status = 1)
                    else:
                        return render_template("Error.html" , title = "Error Page" , User = "Admin" ,  Status = 1)
                elif UserType == 3:
                    data = GetOneWhere("Password" , "Users" , "Username" , Username , False)
                    if OldPassword == data:
                        if NewPassword == RenewPassword:
                            cur.execute(f"UPDATE Users SET Password = '{NewPassword}' WHERE Username = '{Username}' AND Password = '{OldPassword}'")
                        return render_template("Owner Side/Owner Profile Page.html" , title = "Owner Profile Page" , User = "Owner" ,  Status = 1)
                else:
                    return render_template("Error.html" , title = "Error Page" , User = "Owner" ,  Status = 1)
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()

############################################################################
################### Admin Functions
@app.route('/AdminHome' , methods=["POST","GET"])
def AdminHome():
    if request.method == "POST":
        Username = request.form.get("Username")
    return render_template('Home Page.html', title="Admin Home Page" , User = "Admin" , Status = 1 , Name = Username)

@app.route('/AdminStore' , methods=["POST","GET"])
def AdminStore():
    if request.method == "POST":
        Username = request.form.get("Username")
    Items = SelectAll("Items")
    return render_template('Admin Side/Admin Store Page.html', title="Admin Store Page" , User = "Admin" , Status = 1 , Items = Items , Name = Username)

@app.route('/AdminOrders' , methods=["POST","GET"])
def AdminOrders():
    Items = SelectAll("Orders")
    return render_template('Admin Side/Admin Orders Page.html', title="Admin Orders Page" , User = "Admin" , Status = 1 ,Items = Items)

@app.route('/AdminProfile' , methods=["POST","GET"])
def AdminProfile():
    if request.method == "POST":
        Username = request.form.get("Username")
    return render_template('Admin Side/Admin Profile Page.html', title="Admin Profile Page" , User = "Admin" , Status = 1 , Name = Username)

@app.route('/BetaAdminChangePassword' , methods = ["POST" , "GET"])
def BetaAdminChangePassword():
    if request.method == "POST":
        Username = request.form.get("Username")
    return render_template('Fixed Side/Change Password Page.html', title="Change Password Page" , User = "Admin" , Status = 1 , Name = Username)

############################################################################
################## Item Functions - Admin
@app.route('/AddItem' , methods=["POST","GET"])
def AddItem():
    if request.method == "POST":
        try:
            Name = request.form.get("Name")
            Brand = request.form.get("Brand")
            Category = request.form.get("Category")
            Image = request.form.get("Image")
            Price = request.form.get("Price")
            Description = request.form.get("Description")
            Commission = request.form.get("Commission")
            Discount = request.form.get("Discount")
            Id = len(SelectAll("Items"))
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO Items VALUES({Id},'{Name}','{Brand}','{Category}',{Price},'{Image}','{Description}','{Commission}',{Discount})")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
    return render_template('Item Side/Add Item Page.html', title="Add Item Page" , User = "Admin" , Status = 1)

@app.route('/ModifyItem' , methods=["POST","GET"])
def ModifyItem():
    if request.method == "POST":
        try:
            Id = request.form.get("Id")
            Name = request.form.get("Name")
            Brand = request.form.get("Brand")
            Category = request.form.get("Category")
            Image = request.form.get("Image")
            Price = request.form.get("Price")
            Description = request.form.get("Description")
            Commission = request.form.get("Commission")
            Discount = request.form.get("Discount")
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()
                if Name:
                    cur.execute(f"UPDATE Items SET Name = '{Name}' WHERE Id = {Id}")
                if Price:
                    cur.execute(f"UPDATE Items SET Price = {Price} WHERE Id = {Id}")
                if Description:
                    cur.execute(f"UPDATE Items SET Description = '{Description}' WHERE Id = {Id}")
                if Category:
                    cur.execute(f"UPDATE Items SET Category = '{Category}' WHERE Id = {Id}")
                if Brand:
                    cur.execute(f"UPDATE Items SET Brand = '{Brand}' WHERE Id = {Id}")
                if Image:
                    cur.execute(f"UPDATE Items SET Image = '{Image}' WHERE Id = {Id}")
                if Commission:
                    cur.execute(f"UPDATE Items SET Commission = '{Commission}' WHERE Id = {Id}")
                if Discount:
                    cur.execute(f"UPDATE Items SET Discount = {Discount} WHERE Id = {Id}")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
    return render_template('Item Side/Modify Item Page.html', title="Modify Item Page" , User = "Admin" , Status = 1)

@app.route('/BetaModify' , methods=["POST","GET"])
def BetaModify():
    if request.method == "POST":
        Id = request.form.get("Id")
    return render_template("Item Side//Modify Item Page.html" , title = "Modify Item Page", User = 'Admin' , Value = Id , Status = 1)

@app.route('/RemoveItem' , methods=["POST","GET"])
def RemoveItem():
    if request.method == "POST":
        try:
            Id = request.form.get("Id")
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()
                cur.execute(f"DELETE FROM Items WHERE Id = {Id}")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
    return render_template('Item Side/Remove Item Page.html', title="Remove Item Page" , User = "Admin" , Status = 1)

@app.route('/BetaRmove' , methods=["POST","GET"])
def BetaRemove():
    if request.method == "POST":
        Id = request.form.get("Id")
    return render_template("Item Side/Remove Item Page.html" , title = "Remove Item Page" , Value = Id , Status = 1)

############################################################################
################## Client Functions
@app.route('/ClientHome' , methods=["POST","GET"])
def ClientHome():
    if request.method == "POST":
        CId = request.form.get("CId")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
        Items = SelectAll("Items")
    return render_template('Home Page.html', title="Client Home Page" , User = "Client" , Status = 1 , CId = CId , Name  = Name , Items = Items )

@app.route('/ClientOrder' , methods=["POST","GET"])
def ClientOrder():
    if request.method == "POST":
        CId = request.form.get("CId")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
        try:
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()
                cur.execute(f"SELECT OrderId FROM C{CId}  ORDER BY rowid  DESC LIMIT 1")
                data = [list(tup) for tup in cur.fetchall()]
                con.commit()
        except sqlite3.Error as er :
            print(er)
        finally:
            con.close()
        Items = GetAllWhere(f'C{CId}' , "OrderId" , data[0][0] , True)
        data = GetAllWhere("Orders" , "ClientId" , CId , True)
    return render_template('Client Side/Client Order Page.html', title="Client Order Page" , User = "Client" , Status = 1 , CId = CId , Name  = Name , Items = Items , data = data )

@app.route('/ClientStore' , methods=["POST","GET"])
def ClientStore():
    if request.method == "POST":
        CId = request.form.get("CId")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
        Items = SelectAll("Items")
    return render_template('Client Side/Client Store Page.html', title="Client Store Page" , User = "Client" , Status = 1 , CId = CId , Name  = Name , Items = Items )

@app.route('/ClientOrders' , methods=["POST","GET"])
def ClientOrders():
    if request.method == "POST":
        CId = request.form.get("CId")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
        Items = SelectAll(f"C{CId}")
    data = SelectAll(f"C{CId}")
    return render_template('Client Side/Client Orders Page.html', title="Client Orders Page" , User = "Client" , Status = 1, CId = CId , Name  = Name , Items = data )

@app.route('/ClientCart' , methods=["POST","GET"])
def ClientCart():
    if request.method == "POST":
        CId = request.form.get("CId")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
        Items = SelectAll(f"C{CId}")
    return render_template('Client Side/Client Cart Page.html', title="Client Cart Page" , User = "Client" , Status = 1 , CId = CId , Name  = Name , Cart = Items )

@app.route('/ClientProfile' , methods=["POST","GET"])
def ClientProfile():
    if request.method == "POST":
        CId = request.form.get("CId")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
        Items = GetAllWhere("Clients" , "Id" , CId , True) 
    return render_template('Client Side/Client Profile Page.html', title="Client Profile Page" , User = "Client" , Status = 1 , Name = Name , data = Items , CId = CId)

@app.route('/UpdateData' , methods=["POST","GET"])
def UpdateData():
    if request.method == "POST":
        try:
            Id = request.form.get("CId")
            Username = request.form.get("Username")
            Email = request.form.get("Email")
            Address = request.form.get("Address")
            Mobile = request.form.get("Mobile")
            Birthday = request.form.get("Birthday")
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()            
                OUsername = GetOneWhere("Username" , "Clients" , "Id" , Id , True)
                if Username:
                    cur.execute(f"UPDATE Users SET Username = '{Username}' WHERE Username = '{OUsername}'")
                    cur.execute(f"UPDATE Clients SET Username = '{Username}' WHERE Id = {Id}")
                if Email:
                    cur.execute(f"UPDATE Clients SET Email = '{Email}' WHERE  Id = {Id}")
                if Address:
                    cur.execute(f"UPDATE Clients SET Address = '{Address}' WHERE  Id = {Id}")
                if Mobile:
                    cur.execute(f"UPDATE Clients SET Mobile = {Mobile} WHERE  Id = {Id}")
                if Birthday:
                    cur.execute(f"UPDATE Clients SET Birthday = '{Birthday}' WHERE  Id = {Id}")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        Username = GetOneWhere("Username" , "Clients" , "Id" , Id , True)
    return render_template('Home Page.html', title="Client Home Page" , User = "Client" , Status = 1 , Name = Username , CId  = Id)

@app.route('/BetaClientChangePassword' , methods = ["POST" , "GET"])
def BetaClientChangePassword():
    if request.method == "POST":
        Username = request.form.get("Username")
    return render_template('Fixed Side/Change Password Page.html', title="Change Password Page" , User = "Client" , Status = 1 , Name = Username)

############################################################################
##################### Order Functions 
@app.route('/AddToCart' , methods=["POST","GET"])
def AddToCart():
    if request.method == "POST":
        try:
            CId = request.form.get("CId")
            IId = request.form.get("IId")
            Status = request.form.get("Status")
            with sqlite3.connect(DB.System) as con:
                if int(Status) == 1:
                    cur = con.cursor()
                    OrderId = len(SelectAll("Orders"))
                    Item = GetAllWhere("Items" , "Id" , IId , True)
                    cur.execute(f"INSERT INTO C{CId} VALUES({OrderId} , {Item[0][0]} , '{Item[0][1]}' , '{Item[0][2]}' , '{Item[0][3]}' , {Item[0][4]} , '{Item[0][5]}' , '{Item[0][6]}' , '{Item[0][7]}' , {Item[0][8]} , 1)")
                    con.commit() 
                else:
                    return render_template('Controlling Side/Log In Page.html', title="Log In Page" , User = "Visitor" , Status = 0)
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        Items = SelectAll("Items")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True) 
    return render_template('Client Side/Client Store Page.html', title="Client Store Page" , User = "Client" , Status = 1 , Items = Items , CId = CId , Name = Name)

@app.route('/Plus'  , methods=["POST","GET"])
def Plus():
    if request.method == "POST":
        CId = request.form.get("CId")
        IId = request.form.get("IId")
        db = sqlite3.connect(DB.System)
        cur = db.cursor()
        cur.execute(f"UPDATE C{CId} SET Amount = Amount +1 WHERE Id = {IId}")
        db.commit()
        db.close()
        Items = SelectAll(f'C{CId}')
    return render_template('Client Side/Client Cart Page.html', title="Client Cart Page" , User = "Client" , Status = 1 , Cart = Items , CId = CId)

@app.route('/Miunes'  , methods=["POST","GET"])
def Miunes():
    CId = request.form.get("CId")
    IId = request.form.get("IId")
    db = sqlite3.connect(DB.System)
    cur = db.cursor()
    cur.execute(f"UPDATE C{CId} SET Amount = Amount -1 WHERE Id = {IId}")
    db.commit()
    db.close()
    Items = SelectAll(f'C{CId}')
    return render_template('Client Side/Client Cart Page.html', title="Client Cart Page" , User = "Client" , Status = 1 , Cart = Items , CId = CId)

@app.route('/Bill'  , methods=["POST","GET"]) 
def Bill():
    if request.method == "POST":
        CId = request.form.get("CId")
        db = sqlite3.connect(DB.System)
        cur  = db.cursor()
        cur.execute(f"SELECT Total FROM C{CId}")
        data = [list(tup) for tup in  cur.fetchall()]
        Total=0
        for One in data[0]:
            Total += int(One)
        Items = SelectAll(f'C{CId}') 
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True) 
    return render_template('Order Side/Bill Page.html', title="Bill Page" , User = "Client" , Status = 1 , Total = Total , Cart = Items , CId = CId , Name = Name )

@app.route('/Details'  , methods=["POST","GET"])
def Details():
    if request.method == "POST":
        CId = request.form.get("CId")
        Total = request.form.get("Total")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
    return render_template('Order Side/Details Page.html', title="Details Page" , User = "Client" , Status = 1 , Total = Total , CId = CId , Name = Name)

@app.route('/BuyMethod'  , methods=["POST","GET"])
def BuyMethod():
    if request.method == "POST":
        Name = request.form.get("Name")
        Address = request.form.get("Address")
        Mobile = request.form.get("Mobile")
        DeliveryDate = request.form.get("DeliveryDate")
        DeliveryTime = request.form.get("DeliveryTime")
        BuyMethod = request.form.get("BuyMethod")
        CId = request.form.get("CId")
        Total = request.form.get("Total")
        try:
            with sqlite3.connect(DB.System) as con:
                cur = con.cursor()
                cur.execute(f"SELECT OrderId FROM C{CId}  ORDER BY rowid  DESC LIMIT 1")
                data = [list(tup) for tup in cur.fetchall()]
                cur.execute(f"INSERT INTO Orders VALUES({data[0][0]},{CId} , {Total} , '{Address}' , '{Name}' , {Mobile} , '{DeliveryDate}' , '{DeliveryTime}' , 'A')")
                Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
                Code =GenrateOTP()
                if BuyMethod == '1':
                    cur.execute(f"UPDATE Orders SET BuyingMethod = 'Cash' WHERE ClientId = {CId}")
                    return render_template('Order Side/Cash Page.html', title="Cash Page" , User = "Client" , Status = 1 , CId = CId, Name = Name , OrderId = data[0][0])
                elif BuyMethod == '2':
                    cur.execute(f"UPDATE Orders SET BuyingMethod = 'Visa' WHERE ClientId = {CId}")
                    return render_template('Order Side/Visa Page.html', title="Visa Page" , User = "Client" , Status = 1 , CId = CId, Name = Name , OrderId = data[0][0])
                elif BuyMethod == '3':
                    cur.execute(f"UPDATE Orders SET BuyingMethod = 'Fawry' WHERE ClientId = {CId}")
                    return render_template('Order Side/Fawry Page.html', title="Fawry Page" , User = "Client" , Status = 1 , CId = CId, Name = Name, OrderId = data[0][0] , Code = Code)
                elif BuyMethod == '4':
                    cur.execute(f"UPDATE Orders SET BuyingMethod = 'EWallet' WHERE ClientId = {CId}")
                    return render_template('Order Side/EWallet Page.html', title="EWallet Page" , User = "Client" , Status = 1 , CId = CId, Name = Name , OrderId = data[0][0] , Code = Code)
                else:
                    return render_template('Error Page.html', title="Error Page" , User = "Client" , Status = 1)
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
        
@app.route('/Visa' , methods=["POST","GET"])
def Visa():
    if request.method == "POST":
        OrderId = request.form.get("OrderId")
        CId = request.form.get("CId")
        Items = GetAllWhere(f'C{CId}' , "OrderId" , OrderId , True)
        data = GetAllWhere("Orders" , "ClientId" , CId , True)
    return render_template('Order Side/FinallBill Page.html', title="FinallBill Page" , User = "Client" , Status = 1 , Items = Items , data = data, CId = CId) 

@app.route('/EWallet' , methods=["POST","GET"])
def EWallet():
    if request.method == "POST":
        OrderId = request.form.get("OrderId")
        CId = request.form.get("CId")
        Items = GetAllWhere(f'C{CId}' , "OrderId" , OrderId , True)
        data = GetAllWhere("Orders" , "ClientId" , CId , True)
    return render_template('Order Side/FinallBill Page.html', title="FinallBill Page" , User = "Client" , Status = 1 , Items = Items , data = data, CId = CId)

@app.route('/Fawry' , methods=["POST","GET"])
def Fawry():
    if request.method == "POST":
        OrderId = request.form.get("OrderId")
        CId = request.form.get("CId")
        Items = GetAllWhere(f'C{CId}' , "OrderId" , OrderId , True)
        data = GetAllWhere("Orders" , "ClientId" , CId , True)
    return render_template('Order Side/FinallBill Page.html', title="FinallBill Page" , User = "Client" , Status = 1 , Items = Items , data = data, CId = CId)

@app.route('/Cash' , methods=["POST","GET"])
def Cash():
    if request.method == "POST":
        OrderId = request.form.get("OrderId")
        CId = request.form.get("CId")
        Items = GetAllWhere(f'C{CId}' , "OrderId" , OrderId , True)
        data = GetAllWhere("Orders" , "ClientId" , CId , True)
    return render_template('Order Side/FinallBill Page.html', title="FinallBill Page" , User = "Client" , Status = 1 , Items = Items , data = data , CId = CId)

@app.route('/CheckOut' , methods=["POST","GET"])
def CheckOut():
    if request.method == "POST":
        CId = request.form.get("CId")
        Name = GetOneWhere("Username" , "Clients" , "Id" , CId , True)
        Items = SelectAll("Items")
        
    return render_template('Home Page.html', title="Client Home Page" , User = "Client" , Status = 1 , CId = CId , Name  = Name , Items = Items )

############################################################################
##################### Owner Functions 
@app.route('/OwnerHome' , methods=["POST","GET"])
def OwnerHome():
    return render_template('Home Page.html', title="Owner Home Page" , User = "Owner" , Status = 1)

@app.route('/OwnerStore' , methods=["POST","GET"])
def OwnerStore():
    Items = SelectAll("Items")
    return render_template('Owner Side/Owner Store Page.html', title="Owner Store Page" , User = "Owner" , Status = 1 ,  Items = Items)

@app.route('/OwnerOrders' , methods=["POST","GET"])
def OwnerOrders():
    Items = SelectAll("Orders")
    return render_template('Owner Side/Owner Orders Page.html', title="Owner Orders Page" , User = "Owner" , Status = 1 , Items = Items)

@app.route('/OwnerAnalysis' , methods=["POST","GET"])
def OwnerAnalysis():
    return render_template('Owner Side/Owner Analysis Page.html', title="Owner Analysis Page" , User = "Owner" , Status = 1)

@app.route('/OwnerProfile' , methods=["POST","GET"])
def OwnerProfile():
    return render_template('Owner Side/Owner Profile Page.html', title="Owner Profile Page" , User = "Owner" , Status = 1)

############################################################################

@app.route('/DEV' , methods=["POST","GET"])
def DEV():
    return render_template('Controlling Side/Add.html', title="Add Page" , User = "Visitor" , Status = 0)

@app.route('/GGG' , methods = ["POST" , "GET"])
def GGG():
    if request.method == "POST":
        try:
            Username = request.form.get("Username")
            Password = request.form.get("Password")
            Type = request.form.get("Type")
            with sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}\System.db") as con:
                cur = con.cursor()
                cur.execute(f"INSERT INTO Users VALUES('{Username}' , '{Password}' , {Type})")
                con.commit()
        except sqlite3.Error as er:
            print(er)
        finally:
            con.close()
    return render_template('Controlling Side/Add.html', title="Add Page" , User = "Visitor" , Status = 0)


if __name__ ==  "__main__":
    app.run()