from models import Order, OrderItem
from database import Database

class OrderBuilder:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.client_name = None
        self.client_type = None
        self.payment_method = None
        self.items = []
        self.db = Database()
        return self
    
    def set_client(self, name, client_type):
        self.client_name = name
        self.client_type = client_type
        return self
    
    def set_payment_method(self, payment_method):
        self.payment_method = payment_method
        return self
    
    def add_item(self, product_id, quantity):
        product = self.db.get_product(product_id)
        if not product:
            raise ValueError(f"Producto {product_id} no encontrado")
        
        self.items.append(OrderItem(product, quantity))
        return self
    
    def build(self):
        if not all([self.client_name, self.client_type, self.payment_method, self.items]):
            raise ValueError("Faltan datos requeridos para construir el pedido")
        
        order = Order(self.client_name, self.client_type, self.payment_method)
        order.items = self.items
        order.calculate_totals()

        return order
