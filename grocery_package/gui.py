import tkinter as tk
from tkinter import messagebox, ttk

from grocery_package.billing import billing
from grocery_package.customer import customer
from grocery_package.products import product


class GroceryBillingGUI:
    def __init__(self, root):
        self.root = root
        self.bill = billing()
        self.root.title("Grocery Billing System")
        self.root.geometry("820x620")

        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_category = tk.StringVar(value="General")
        self.product_price = tk.StringVar()
        self.product_quantity = tk.StringVar()

        self.build_layout()

    def build_layout(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        customer_frame = ttk.LabelFrame(main, text="Customer", padding=10)
        customer_frame.pack(fill="x")

        ttk.Label(customer_frame, text="Name").grid(row=0, column=0, sticky="w")
        ttk.Entry(customer_frame, textvariable=self.customer_name, width=28).grid(row=0, column=1, padx=8)
        ttk.Label(customer_frame, text="Phone").grid(row=0, column=2, sticky="w")
        ttk.Entry(customer_frame, textvariable=self.customer_phone, width=18).grid(row=0, column=3, padx=8)
        ttk.Button(customer_frame, text="Add Customer", command=self.add_customer).grid(row=0, column=4, padx=8)

        product_frame = ttk.LabelFrame(main, text="Product", padding=10)
        product_frame.pack(fill="x", pady=10)

        labels = ["Name", "Category", "Price", "Quantity"]
        variables = [self.product_name, self.product_category, self.product_price, self.product_quantity]
        for index, label in enumerate(labels):
            ttk.Label(product_frame, text=label).grid(row=0, column=index * 2, sticky="w")
            ttk.Entry(product_frame, textvariable=variables[index], width=16).grid(row=0, column=index * 2 + 1, padx=6)

        ttk.Button(product_frame, text="Add Product", command=self.add_product).grid(row=0, column=8, padx=8)

        self.tree = ttk.Treeview(main, columns=("category", "price", "quantity", "total"), show="tree headings")
        self.tree.heading("#0", text="Product")
        self.tree.heading("category", text="Category")
        self.tree.heading("price", text="Price")
        self.tree.heading("quantity", text="Qty")
        self.tree.heading("total", text="Total")
        self.tree.pack(fill="both", expand=True, pady=10)

        button_frame = ttk.Frame(main)
        button_frame.pack(fill="x")
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected).pack(side="left")
        ttk.Button(button_frame, text="Show Bill", command=self.show_bill).pack(side="left", padx=8)
        ttk.Button(button_frame, text="Save Bill", command=self.save_bill).pack(side="left")
        ttk.Button(button_frame, text="New Bill", command=self.new_bill).pack(side="left", padx=8)

        self.output = tk.Text(main, height=12)
        self.output.pack(fill="x", pady=10)

    def add_customer(self):
        name = self.customer_name.get().strip()
        phone = self.customer_phone.get().strip()

        if not name:
            messagebox.showerror("Invalid Customer", "Customer name is required")
            return
        if not customer.is_valid_phone(phone):
            messagebox.showerror("Invalid Customer", "Phone number must contain exactly 10 digits")
            return

        self.bill.customer = customer(name, phone)
        messagebox.showinfo("Customer Added", "Customer added successfully")

    def add_product(self):
        try:
            name = self.product_name.get().strip()
            category = self.product_category.get().strip() or "General"
            price = float(self.product_price.get())
            quantity = int(self.product_quantity.get())

            if not name:
                raise ValueError("Product name is required")
            if price <= 0 or quantity <= 0:
                raise ValueError("Price and quantity must be greater than 0")
        except ValueError as error:
            messagebox.showerror("Invalid Product", str(error))
            return

        new_product = product(name, price, quantity, category)
        self.bill.product.append(new_product)
        self.tree.insert("", "end", text=name, values=(category, price, quantity, new_product.total_price()))
        self.product_name.set("")
        self.product_category.set("General")
        self.product_price.set("")
        self.product_quantity.set("")

    def remove_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("No Selection", "Select a product to remove")
            return

        index = self.tree.index(selected[0])
        del self.bill.product[index]
        self.tree.delete(selected[0])

    def show_bill(self):
        if self.bill.customer is None:
            messagebox.showerror("Missing Customer", "Add customer first")
            return
        if not self.bill.product:
            messagebox.showerror("Missing Products", "Add at least one product")
            return

        data = self.bill.get_bill_data()
        lines = [
            "GROCERY STORE BILL",
            f"Bill Number: {data['bill_number']}",
            f"Bill Date: {data['bill_date']}",
            f"Customer Name: {data['customer']['name']}",
            f"Customer Phone: {data['customer']['phnum']}",
            "-" * 55,
            "Product\tCategory\tPrice\tQty\tTotal",
        ]

        for item in data["products"]:
            lines.append(
                f"{item['name']}\t{item['category']}\t{item['price']}\t{item['quantity']}\t{item['total']}"
            )

        lines.extend([
            "-" * 55,
            f"TOTAL AMOUNT: {data['total']}",
            f"DISCOUNT: {data['discount']}",
            f"GST ({int(data['gst_rate'] * 100)}%): {data['gst_amount']}",
            f"FINAL AMOUNT: {data['final_amount']}",
        ])

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n".join(lines))

    def save_bill(self):
        if self.bill.customer is None or not self.bill.product:
            messagebox.showerror("Cannot Save", "Add customer and products before saving")
            return

        self.bill.save_bill()
        messagebox.showinfo("Saved", f"Bill saved as {self.bill.bill_number}")

    def new_bill(self):
        self.bill.reset_bill()
        self.customer_name.set("")
        self.customer_phone.set("")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.output.delete("1.0", tk.END)


def start_gui():
    root = tk.Tk()
    GroceryBillingGUI(root)
    root.mainloop()
