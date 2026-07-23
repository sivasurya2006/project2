import json
import os

from grocery_package.customer import customer
from grocery_package.products import product
from grocery_package.discount import discountt


class billing:
    def __init__(self):
        self.product = []
        self.customer = None
        self.discount = discountt()

    def add_customer(self):
        name = input("enter the customer name: ")
        phonum = input("enter the customer phone number: ")

        self.customer = customer(name, phonum)
        print("customer added successfully")

    def add_product(self):
        name = input("enter the product name: ")
        price = float(input("enter the price of the product: "))
        quantity = int(input("enter the product quantity: "))

        new_product = product(name, price, quantity)
        self.product.append(new_product)
        print("product added successfully")

    def search_product(self):
        userinput = input("enter the product name: ")

        for item in self.product:
            if userinput.lower() == item.name.lower():
                print("Product Name:", item.name)
                print("Price:", item.price)
                print("Quantity:", item.quantity)
                print("Total:", item.total_price())
                return

        print("product not found")

    def remove_product(self):
        userinput = input("enter the product name: ")

        for item in self.product:
            if userinput.lower() == item.name.lower():
                self.product.remove(item)
                print("product deleted successfully")
                return

        print("product not found")

    def update_product(self):
        userinput = input("enter the product name: ")

        for item in self.product:
            if userinput.lower() == item.name.lower():
                newquantity = int(input("enter the new product quantity: "))
                item.quantity = newquantity
                print("quantity updated successfully")
                return

        print("product not found")

    def calculate_total(self):
        total = 0

        for item in self.product:
            total += item.total_price()

        return total

    def show_bill(self):
        if self.customer is None:
            print("add customer first")
            return

        if len(self.product) == 0:
            print("no product added yet")
            return

        total = self.calculate_total()
        dis_amnt = self.discount.calculate_discount(total)
        final_amnt = total - dis_amnt

        print("\n GROCERY STORE BILL")
        print("Customer Name:", self.customer.name)
        print("Customer Phone:", self.customer.phnum)
        print("----------------------------------------")
        print("Product\t\tPrice\tQty\tTotal")

        for item in self.product:
            print(f"{item.name}\t\t{item.price}\t{item.quantity}\t{item.total_price()}")

        print("----------------------------------------")
        print("TOTAL AMOUNT:", total)
        print("DISCOUNT:", dis_amnt)
        print("FINAL AMOUNT:", final_amnt)
        print("========================================")

    def save_bill(self):
        if self.customer is None:
            print("Please add customer before saving")
            return

        data = {
            "customer": self.customer.to_dict(),
            "products": [],
            "total": self.calculate_total()
        }

        for item in self.product:
            data["products"].append(item.to_dict())

        discount_amount = self.discount.calculate_discount(data["total"])
        data["discount"] = discount_amount
        data["final_amount"] = data["total"] - discount_amount

        with open("bill.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Bill saved successfully in bill.json")

    def load_bill(self):
        if not os.path.exists("bill.json"):
            print("No saved bill found")
            return

        with open("bill.json", "r") as file:
            data = json.load(file)

        self.customer = customer(
            data["customer"]["name"],
            data["customer"]["phnum"]
        )

        self.product = []

        for item in data["products"]:
            new_product = product(item["name"], item["price"], item["quantity"])
            self.product.append(new_product)

        print("Bill loaded successfully")
