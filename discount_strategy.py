from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, subtotal):
        pass

class NormalDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal):
        return 0
    
class PremiumDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal):
        return subtotal * 0.10

class VIPDiscount(DiscountStrategy):
    def calculate_discount(self, subtotal):
        return subtotal * 0.20
    
class DiscountStrategyFactory:
    @staticmethod
    def get_strategy(client_type):
        strategies = {
            'normal': NormalDiscount(),
            'premium': PremiumDiscount(),
            'vip':VIPDiscount()
        }
        return strategies.get(client_type.lower(), NormalDiscount())