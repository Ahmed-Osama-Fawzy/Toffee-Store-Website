import re
class Validation:
    Id = ''
    Name = ''
    Password = ''
    Email = ''
    Mobile = ''
    Address = ''

    def __init__(self , Id='' , Name='' , Password='' , Email='' , Mobile='' , Address=''):
        self.id = Id
        self.Name = Name
        self.Password = Password
        self.Email = Email
        self.Mobile = Mobile
        self.Address = Address

    def SetId(self,I):
        self.Id = I

    def SetName(self,N):
        self.Name = N
    
    def SetPassword(self,P):
        self.Password = P

    def SetEmail(self,E):
        self.Email = E

    def SetMobile(self,M):
        self.Mobile = M

    def SetAddress(self,A):
        self.Address = A

    def Check(self, Key):
        if Key == "Id":
            if self.Id:
                pattern = r'^(C|O|A)\d+$'
                return re.match(pattern, self.Name) is not None
            else:
                print("Please Set Name First")
        if Key == "Name":
            if self.Name:
                pattern = r'^[a-zA-Z_][a-zA-Z0-9_-]{2,19}$'
                return re.match(pattern, self.Name) is not None
            else:
                print("Please Set Name First")
        
        elif Key == "Password":
            if self.Password:
                pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+={}[\]\\|;:\'",.<>/?-]).{8,}$'
                return re.match(pattern, self.Password) is not None
            else:
                print("Please Set Password First")

        elif Key == "Email":
            if self.Email:
                pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                return re.match(pattern, self.Email) is not None
            else:
                print("Please Set Email First")
        
        elif Key == "Mobile":
            if self.Mobile:
                pattern = r'^(011|012|015|010)\d{8}$'
                return re.match(pattern, self.Mobile) is not None
            else:
                print("Please Set Mobile First")
        
        elif Key == "Address":
            if self.Address:
                pattern = r'^\d+[a-zA-Z ,]+?$'
                return re.match(pattern, self.Address) is not None
            else:
                print("Please Set Address First")
        else:
            print("Sorry Invaild Inputs")