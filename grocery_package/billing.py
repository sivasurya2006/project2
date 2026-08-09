import json
import os
from datetime import datetime

from grocery_package.customer import customer
from grocery_package.products import product
from grocery_package.discount import discountt


class billing:
    BILL_FILE = "bills.json"
    GST_RATE = 0.05

    def __init__(self):
        self.product = []
        self.customer = None
        self.discount = discountt()
        self.bill_number = self.generate_bill_number()
        self.bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_bill_number(self):
        return datetime.now().strftime("BILL%Y%m%d%H%M%S")

    def reset_bill(self):
        self.product = []
        self.customer = None
        self.bill_number = self.generate_bill_number()
        self.bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_non_empty_input(self, message):
        while True:
            value = input(message).strip()
            if value:
                return value
            print("Input cannot be empty")

    def get_float_input(self, message):
        while True:
            try:
                value = float(input(message))
                if value > 0:
                    return value
                print("Please enter a value greater than 0")
            except ValueError:
                print("Invalid amount. Please enter a number")

    def get_int_input(self, message):
        while True:
            try:
                value = int(input(message))
                if value > 0:
                    return value
                print("Please enter a quantity greater than 0")
            except ValueError:
                print("Invalid quantity. Please enter a whole number")

    def add_customer(self):
        name = self.get_non_empty_input("enter the customer name: ")

        while True:
            phonum = input("enter the customer phone number: ").strip()
            if customer.is_valid_phone(phonum):
                break
            print("Invalid phone number. Please enter exactly 10 digits")

        self.customer = customer(name, phonum)
        print("customer added successfully")

    def add_product(self):
        name = self.get_non_empty_input("enter the product name: ")
        category = self.get_non_empty_input("enter the product category: ")
        price = self.get_float_input("enter the price of the product: ")
        quantity = self.get_int_input("enter the product quantity: ")

        new_product = product(name, price, quantity, category)
        self.product.append(new_product)
        print("product added successfully")

    def search_product(self):
        userinput = input("enter the product name: ")

        for item in self.product:
            if userinput.lower() == item.name.lower():
                print("Product Name:", item.name)
                print("Category:", item.category)
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
                newquantity = self.get_int_input("enter the new product quantity: ")
                item.quantity = newquantity
                print("quantity updated successfully")
                return

        print("product not found")

    def calculate_total(self):
        total = 0

        for item in self.product:
            total += item.total_price()

        return total

    def calculate_gst(self, amount):
        return amount * self.GST_RATE

    def get_bill_data(self):
        total = self.calculate_total()
        dis_amnt = self.discount.calculate_discount(total)
        taxable_amount = total - dis_amnt
        gst_amount = self.calculate_gst(taxable_amount)

        return {
            "bill_number": self.bill_number,
            "bill_date": self.bill_date,
            "customer": self.customer.to_dict(),
            "products": [item.to_dict() for item in self.product],
            "total": total,
            "discount": dis_amnt,
            "gst_rate": self.GST_RATE,
            "gst_amount": gst_amount,
            "final_amount": taxable_amount + gst_amount
        }

    def show_bill(self):
        if self.customer is None:
            print("add customer first")
            return

        if len(self.product) == 0:
            print("no product added yet")
            return

        data = self.get_bill_data()

        print("\n GROCERY STORE BILL")
        print("Bill Number:", data["bill_number"])
        print("Bill Date:", data["bill_date"])
        print("Customer Name:", self.customer.name)
        print("Customer Phone:", self.customer.phnum)
        print("------------------------------------------------------------")
        print("Product\t\tCategory\tPrice\tQty\tTotal")

        for item in self.product:
            print(f"{item.name}\t\t{item.category}\t\t{item.price}\t{item.quantity}\t{item.total_price()}")

        print("------------------------------------------------------------")
        print("TOTAL AMOUNT:", data["total"])
        print("DISCOUNT:", data["discount"])
        print(f"GST ({int(self.GST_RATE * 100)}%):", data["gst_amount"])
        print("FINAL AMOUNT:", data["final_amount"])
        print("============================================================")

    def save_bill(self):
        if self.customer is None:
            print("Please add customer before saving")
            return

        if len(self.product) == 0:
            print("Please add at least one product before saving")
            return

        data = self.get_bill_data()
        saved_bills = []

        if os.path.exists(self.BILL_FILE):
            try:
                with open(self.BILL_FILE, "r") as file:
                    saved_bills = json.load(file)
            except (json.JSONDecodeError, OSError):
                print("Saved bill file is not readable. Starting a new bill list")

        saved_bills.append(data)

        with open(self.BILL_FILE, "w") as file:
            json.dump(saved_bills, file, indent=4)

        print(f"Bill saved successfully in {self.BILL_FILE}")
        print("Bill Number:", self.bill_number)

    def load_bill(self):
        if not os.path.exists(self.BILL_FILE):
            print("No saved bill found")
            return

        try:
            with open(self.BILL_FILE, "r") as file:
                saved_bills = json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Unable to read saved bills")
            return

        if len(saved_bills) == 0:
            print("No saved bill found")
            return

        print("\nSaved Bills")
        for index, data in enumerate(saved_bills, start=1):
            customer_name = data.get("customer", {}).get("name", "Unknown")
            print(f"{index}. {data.get('bill_number')} - {customer_name} - {data.get('bill_date')}")

        bill_index = self.get_int_input("Enter bill number to load: ") - 1
        if bill_index < 0 or bill_index >= len(saved_bills):
            print("Invalid saved bill selection")
            return

        data = saved_bills[bill_index]

        self.customer = customer(
            data["customer"]["name"],
            data["customer"]["phnum"]
        )
        self.bill_number = data.get("bill_number", self.generate_bill_number())
        self.bill_date = data.get("bill_date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        self.product = []

        for item in data["products"]:
            new_product = product(
                item["name"],
                item["price"],
                item["quantity"],
                item.get("category", "General")
            )
            self.product.append(new_product)

        print("Bill loaded successfully")
