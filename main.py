from grocery_package.billing import billing
from grocery_package.gui import start_gui


def main():
    bill = billing()

    while True:
        print("\n===== GROCERY STORE BILLING SYSTEM =====")
        print("1. Add Customer")
        print("2. Add Product")
        print("3. Search Product")
        print("4. Remove Product")
        print("5. Update Product Quantity")
        print("6. Show Bill")
        print("7. Save Bill")
        print("8. Load Bill")
        print("9. New Bill")
        print("10. Open GUI")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            bill.add_customer()
        elif choice == "2":
            bill.add_product()
        elif choice == "3":
            bill.search_product()
        elif choice == "4":
            bill.remove_product()
        elif choice == "5":
            bill.update_product()
        elif choice == "6":
            bill.show_bill()
        elif choice == "7":
            bill.save_bill()
        elif choice == "8":
            bill.load_bill()
        elif choice == "9":
            bill.reset_bill()
            print("New bill started")
        elif choice == "10":
            start_gui()
        elif choice == "11":
            print("Thank you! Visit again")
            break
        else:
            print("Invalid choice")


main()
