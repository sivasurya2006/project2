class discountt:
    def calculate_discount(self, amount):
        if amount >= 5000:
            return amount * 0.20
        elif amount >= 3000:
            return amount * 0.15
        elif amount >= 1000:
            return amount * 0.10
        else:
            return 0
