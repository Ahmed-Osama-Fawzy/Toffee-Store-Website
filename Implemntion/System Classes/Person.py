import Validation 
class Person:
    Id = ''
    Name = ''
    Password = ''
    Email =''
    Vaild = False

    def __init__(self , Id , Name , Password, Email):
        InputsValidation = Validation.Validation(Id,Name,Password,Email)
        if(InputsValidation.Check("Id") == True and InputsValidation.Check("Name") == True and InputsValidation.Check("Password") == True and InputsValidation.Check("Email") == True):
            self.Vaild = True
        else:
            raise ValueError("You Have Error at data!")
        return self.Vaild
    
