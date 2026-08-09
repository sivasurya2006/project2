class product:
    def __init__(self, name, price, quantity, category="General"):
        self.name = name.strip()
        self.price = price
        self.quantity = quantity
        self.category = category.strip() or "General"

    def total_price(self):
        return self.price * self.quantity

    def to_dict(self):
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "total": self.total_price()
        }
