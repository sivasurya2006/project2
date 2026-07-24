  Grocery Billing System

This is a simple Python grocery billing system. It allows users to add customer details, add products, search products, update product quantities, remove products, show the final bill, save the bill in a JSON file, and load the saved bill.

  Features

- Add customer details
- Add products with price and quantity
- Search product by name
- Remove product from bill
- Update product quantity
- Calculate total amount
- Apply discount automatically
- Show formatted grocery bill
- Save bill data in `bill.json`
- Load saved bill from `bill.json`

  Project Structure

```text
project2/
│
├── main.py
├── .gitignore
│
└── grocery_package/
    ├── __init__.py
    ├── billing.py
    ├── customer.py
    ├── discount.py
    └── products.py
Files Description
main.py
This file contains the menu-driven program. Users can choose options like adding customers, adding products, showing the bill, saving the bill, and loading the bill.
billing.py
This file contains the billing class. It handles the main billing operations such as adding products, calculating total amount, applying discount, displaying bill, saving bill, and loading bill.
customer.py
This file contains the customer class. It stores customer name and phone number.
products.py
This file contains the product class. It stores product name, price, quantity, and calculates total product price.
discount.py
This file contains the discountt class. It calculates discount based on the total bill amount.
Discount Rules
Total Amount	Discount
5000 or more	20%
3000 or more	15%
1000 or more	10%
Below 1000	No discount

How to Run
Clone the repository:
git clone https://github.com/sivasurya2006/project2.git
Go to the project folder:
cd project2
Run the program:
python main.py
Menu Options
===== GROCERY STORE BILLING SYSTEM =====
1. Add Customer
2. Add Product
3. Search Product
4. Remove Product
5. Update Product Quantity
6. Show Bill
7. Save Bill
8. Load Bill
9. Exit
Example Output
GROCERY STORE BILL
Customer Name: Surya
Customer Phone: 9876543210
----------------------------------------
Product         Price   Qty     Total
Rice            500     2       1000
Oil             200     3       600
----------------------------------------
TOTAL AMOUNT: 1600
DISCOUNT: 160
FINAL AMOUNT: 1440
========================================
Requirements
This project uses only built-in Python modules:
json
os
No external packages are required.
.gitignore
The project ignores Python cache files and saved bill data:
__pycache__/
*.pyc
bill.json
Important Notes
Make sure constructors are written like this in Python:
def __init__(self):
not like this:
def **init**(self):
Also, in customer.py, use to_dict() because billing.py calls:
self.customer.to_dict()
Correct method:
def to_dict(self):
    return {
        "name": self.name,
        "phnum": self.phnum
    }
Future Improvements
Add proper phone number validation
Add bill number and date
Save multiple bills instead of overwriting bill.json
Add GST or tax calculation
Improve error handling
Add product categories
Create a GUI version
Author
Created by sivasurya2006 as a Python beginner project.



