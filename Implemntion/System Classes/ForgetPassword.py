import OTP as OT , Database as DB , Validation as VA
class ForgetPassword:
    Email = ''
    Username = ''
    VaildUsername = False
    NewPassword = ''
    ReNewPassword =''
    Vaild = False
    Database = DB.DB("Users")
    PassVaild = VA.Validation()

    def __init__(self , Email):
        self.Email = Email
        Code = OT.OTP(self.Email) 
        if Code.Vaild == True:
            self.Vaild = True
        return self.Vaild
    
    def SetUsername(self , Username):
        self.Username = Username
        if self.Database.SelectOneWhere("Username" , "Username" , self.Username , False):
            self.VaildUsername = True
        return self.VaildUsername
    
    def SetPassword(self , NewPassword , ReNewPassword):
        self.PassVaild.SetPassword(NewPassword)
        if self.PassVaild.Check("Password") == True:
            if NewPassword == ReNewPassword:
                self.NewPassword = NewPassword
                self.ReNewPassword = ReNewPassword
                self.Database.UpdateOne("Password" , NewPassword , False , "Username" , self.Username , False)
                return True
            else:
                raise ValueError("The Passwords Are not Samiler! ")
        else:
            raise ValueError("The Password Is Not Vaild! ")

        

