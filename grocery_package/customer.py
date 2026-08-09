class customer:
    def __init__(self, name, phnum):
        self.name = name.strip()
        self.phnum = str(phnum).strip()

    @staticmethod
    def is_valid_phone(phnum):
        return str(phnum).isdigit() and len(str(phnum)) == 10

    def customerdetails(self):
        userinput = input("Enter the customer phone number: ").strip()

        if userinput == self.phnum:
            print("customer:", self.name)
            print("customer phone number:", self.phnum)
        else:
            print("customer is not found!!")

    def to_dict(self):
        return {
            "name": self.name,
            "phnum": self.phnum
        }
