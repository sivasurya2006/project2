class customer:
    def __init__(self,name,phnum):
        self.name=name
        self.phnum=phnum
        if len(str(self.phnum))==10:
            print("your number is valid:")
        else:
            print("you enter the invalid number plz enter the corrct number:")
    
    def customerdetails(self):
        userinput=int(input("Enter the your number:"))

        if(userinput == self.phnum):
            print("customer:",self.name)
            print("customer phone number",self.phnum)
        else:
            print("customer is not found!!")
    def customer(self):
        return{

        "name":self.name,
        "phnum":self.phnum
        }
        

        
