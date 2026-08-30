from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    def __init__(self, subtotal):
        self.subtotal = subtotal
        
    @abstractmethod
    def calculate_discounted_amount(self):
        pass

class VipCustomer(DiscountStrategy):
    def calculate_discounted_amount(self):
        discount = self.subtotal * 0.20
        return self.subtotal - discount       
        

class RegularCustomer(DiscountStrategy):
    def calculate_discounted_amount(self):
        discount = self.subtotal * 0.05
        return self.subtotal - discount

class WholesaleCustomer(DiscountStrategy):
    def calculate_discounted_amount(self):
        discount = self.subtotal * 0.15
        return self.subtotal - discount

class DiscountFactory:
    @staticmethod
    def get_discount_strategy(customer_type, subtotal):
        customer_type = customer_type.lower()
        strategies = {
            "vip customer":VipCustomer,
            "regular customer":RegularCustomer,
            "wholesale customer":WholesaleCustomer,
        }
        if customer_type in strategies:
            return strategies[customer_type](subtotal)
        raise ValueError("Unknown customer type")


