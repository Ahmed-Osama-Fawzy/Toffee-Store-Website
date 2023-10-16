import Person as P , Items as IT

class Admin(P.Person):
    ManageItem = IT.Item()
    
    def __init__(self, Id, Name, Password, Email):
        super().__init__(Id, Name, Password, Email)

    
    