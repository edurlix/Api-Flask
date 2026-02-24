from abc import ABC, abstractmethod
from datetime import datetime

class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

    @abstractmethod
    def get_name(self):
        pass

class CreditCardPayment(PaymentMethod):
    def process_payment(self, amount):
        return{
            'success': True, 
            'method': 'Tarjeta de Credito',
            'amount': amount,
            'transaction_id': f"CC-{datetime.now().timestamp()}",
            'message': 'Pago procesado con tarjeta de credito'
        }
    
    def get_name(self):
        return 'Tarjeta de Credito'

class PayPalPayment(PaymentMethod):
    def process_payment(self, amount):
        return {
            'success': True,
            'method': 'PayPal',
            'transaction_id': f'PP-{datetime.now().timestamp()}',
            'message': 'Pago procesado con PayPal'
        }
    
    def get_name(self):
        return 'PayPal'
    
class BankTransferPayment(PaymentMethod):
    def process_payment(self, amount):
        return {
            'success': True,
            'method': 'Transferencia Bancaria',
            'transaction_id': f'BT-{datetime.now().timestamp()}',
            'message': 'Pago procesado con transferencia bancaria'
        }
    
    def get_name(self):
        return 'Transferencia Bancaria'
    
class PaymentMethodFactory:
    @staticmethod
    def create_payment_method(method_type):
        methods = {
            'tarjeta': CreditCardPayment(),
            'credito': CreditCardPayment(),
            'credit': CreditCardPayment(),
            'paypal': PayPalPayment(),
            'transferencia': BankTransferPayment(),
            'bank': BankTransferPayment() 
        }

        method = methods.get(method_type.lower())
        if not method:
            raise ValueError(f"Metodo de pago no soportado: {method_type}")
        return method