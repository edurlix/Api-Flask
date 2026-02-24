import uuid
from datetime import datetime
from order_state import PendingState
from discount_strategy import DiscountStrategyFactory
from payment_methods import PaymentMethodFactory
from notifier import Observable

class Product:
    def __init__(self, name, price, category):
        self.id = str(uuid.uuid4())[:3]
        self.name = name
        self.price = float(price)
        self.category = category
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.name,
            "precio": self.price,
            "categoria": self.category
        }

class OrderItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.subtotal = product.price * quantity

    def to_dict(self):
        return {
            "product_id": self.product.id,
            "nombre_producto": self.product.name,
            "cantidad": self.quantity,
            "precio_unitario": self.product.price,
            "subtotal": self.subtotal
        }
    
class Order(Observable):
    def __init__(self, client_name, client_type, payment_method_type):
        super().__init__()
        self.id = None
        self.client_name = client_name
        self.client_type = client_type
        self.payment_method_type = payment_method_type
        self.payment_method = None
        self.items = []
        self.subtotal = 0.0
        self.discount = 0.0
        self.total = 0.0
        self.state = PendingState(self)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        from notifier import CustomerNotifier, WarehouseNotifier, BillingNotifier
        self.add_observer(CustomerNotifier())
        self.add_observer(WarehouseNotifier())
        self.add_observer(BillingNotifier())

    def calculate_totals(self):
        self.subtotal = sum(item.subtotal for item in self.items)

        discount_stategy = DiscountStrategyFactory.get_strategy(self.client_type)
        self.discount = discount_stategy.calculate_discount(self.subtotal)
        self.total = self.subtotal - self.discount
        
        self.updated_at = datetime.now()
        return self.total
    
    def process_payment(self):
        if not self.payment_method:
            self.payment_method = PaymentMethodFactory.create_payment_method(self.payment_method_type)

        payment_result = self.payment_method.process_payment(self.total)
        return payment_result

    def next_state(self):
        self.state.next()
        self.updated_at = datetime.now()
        return self.state

    def cancel(self):
        self.state.cancel()
        self.updated_at = datetime.now()
        return self.state
    
    def to_dict(self):
        return {
            "id": self.id,
            "cliente": self.client_name,
            "tipo_cliente": self.client_type,
            "estado": self.state.get_name(),
            "items": [item.to_dict() for item in self.items],
            "subtotal": self.subtotal,
            "descuento": self.discount,
            "total": self.total,
            "metodo_pago": self.payment_method.get_name() if self.payment_method else self.payment_method_type,
            "creado_en": self.created_at.isoformat(),
            "actualizado_en": self.updated_at.isoformat()
        }