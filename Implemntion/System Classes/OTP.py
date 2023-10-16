import Validation as V , random , math ,smtplib
class OTP:
    VaildEmail = V.Validation()
    Email = ''
    Code = ''
    Vaild = False

    def __init__(self , Email):
        self.VaildEmail.SetEmail(Email)
        if self.VaildEmail.Check("Email") == True :
            self.Email = Email
            digits="0123456789"
            for i in range(6):
                self.Code += digits[math.floor(random.random()*10)]
            return self.Code
        else:
            raise ValueError("Sorry Email Is not Valid! ")
    
    def SendCode(self):
        if self.Email and self.Code:
            msg = self.Code + " is your OTP Code"
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('ahmd.osama2611@gmail.com', 'yvhvsvqismmbfwiz')
            s.sendmail('ahmd.osama2611@gmail.com',self.Email,msg)
            s.quit()
        else:
            raise ValueError("Sorry The Inputs Are Wrong! ")

    def CheckCode(self , Input):
        if self.Code == Input:
            self.Vaild = True
        return self.Vaild