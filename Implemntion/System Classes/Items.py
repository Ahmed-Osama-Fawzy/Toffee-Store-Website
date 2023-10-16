import Database as DB
class Item:
    Id = 0
    Name = ''
    Brand = ''
    Category = ''
    Description = ''
    Commision = ''
    Photo = ''
    Price = 0
    Discount = 0
    Amount = 0
    Avilable = False
    Database = DB.DB("Items")

    def __init__(self):
        pass
    
    ### Add New Item To Table "Items"
    def Add(self,Id,Name,Brand,Category,Descripton,Commision,Photo,Price,Discount,Amount):
        self.Id = Id
        self.Name = Name
        self.Brand = Brand
        self.Category = Category
        self.Description = Descripton
        self.Commision = Commision
        self.Photo = Photo
        self.Price = Price
        self.Discount = Discount
        self.Amount = Amount     
        if self.Amount > 0:
            self.Avilable = True
        else:
            self.Avilable = False
        self.Database.InsertAll([self.Id,True],[self.Name,False],[self.Brand,False],[self.Category,False],[self.Description,False],[self.Commision,False],[self.Photo,False],[self.Price,True],[self.Discount,True],[self.Amount,True])

    ## Set Id For Item To Modify Or Remove IT
    def SetId(self , Id):
        self.Id = Id
        return self.Id
    
    ### Modify Item's data In Table "Items"
    def Modify(self ,*Many):
        if self.Id:
            self.Database.UpdateMany(*Many, "Id" , self.Id , True) 
        else:
            print("Please Enter Id First") 

    ### remove New Item From Table "Items"
    def Remove(self):
        if self.Id:
            self.Database.DeleteAllWhere( "Id" , self.Id , True)   
        else:
            print("Please Enter Id First")   

    def Store(self):
        return self.Database.SelectAll()