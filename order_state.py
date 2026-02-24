from abc import ABC, abstractmethod

class OrderState(ABC):
    def __init__(self, order):
        self.order = order
    
    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def cancel(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

class PendingState(OrderState):
    def next(self):
        print("Avanzando de PENDIENTE A PROCESANDO")
        self.order.state = ProcessingState(self.order)
        self.order.notify_observers()
        return self.order.state
    
    def cancel(self):
        print("Cancelando pedido en estado PENDIENTE")
        self.order.state = CancelledState(self.order)
        self.order.notify_observers()
        return self.order.state
    
    def get_name(self):
        return "PENDIENTE"
    
class ProcessingState(OrderState):
    def next(self):
        print("Avanzando de PROCESANDO a ENVIADO")
        self.order.state = ShippedState(self.order)
        self.order.notify_observers()
        return self.order.state
    
    def cancel(self):
        print("No se puede cancelar un pedido en estado PROCESANDO")
        raise Exception("No se puede cancelar un pedido en estado PROCESANDO")
    
    def get_name(self):
        return "PROCESANDO"
    
class ShippedState(OrderState):
    def next(self):
        print('Avanzando de ENVIO A ENTREGADO')
        self.order.state = DeliveredState(self.order)
        self.order.notify_observers()
        return self.order.state

    def cancel(self):
        print("No se puede cancelar un pedido en estado ENVIADO")
        raise Exception("No se puede cancelar un pedido en estado ENVIADO")
    
    def get_name(self):
        return "ENVIADO"

class DeliveredState(OrderState):
    def next(self):
        print("El pedido ya esta ENTREGADO, no se puede avanzar mas")
        raise Exception("El pedido ya esta entregado")
    
    def cancel(self):
        print("No se peude cancelar un pedido entregado")
        raise Exception("No se puede cancelar un pedido entregado")
    
    def get_name(self):
        return "ENTREGADO"
    
class CancelledState(OrderState):
    def next(self):
        print("No se puede avanzar un pedido cancelado")
        raise Exception("No se peude avanzar un pedido cancelado")
    
    def cancel(self):
        print("El pedido ya esta cancelado")
        raise Exception("El pedido ya esta cancelado")
    
    def get_name(self):
        return "CANCELADO"