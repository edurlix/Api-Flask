from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, order):
        pass

class CustomerNotifier(Observer):
    def update(self, order):
        print(f"[NOTIFICACION - Cliente {order.client_name}]")
        print(f"    tu pedido {order.id} ha cambiado a estado: {order.state.get_name()}")
        if order.state.get_name() == "ENTREGADO":
            print(f"    Gracias por tu compra!")
        elif order.state.get_name() == "CANCELADO":
            print(f"    Tu pedido ha sido cancelado")

class WarehouseNotifier(Observer):
    def update(self, order):
        print(f"[NOTIFICACION - Almacen]")
        print(f"    Pedido {order.id} - Estado: {order.state.get_name()}")
        if order.state.get_name() == "PROCESANDO":
            print(f"        Preparar producto para envio")
        elif order.state.get_name() == "ENVIADO":
            print(f"        Actualizar inventario")

class BillingNotifier(Observer):
    def update(self, order):
        print(f"[NOTIFICACION - Facturacion]")
        print(f"    Pedido {order.id} - Total: ${order.total:.2f}")
        if order.state.get_name() == "ENTREGADO":
            print(f"        Generar factura para {order.client_name}")
        elif order.state.get_name() == "CANCELADO":
            print(f"        Porcesar reembolso de ${order.total:.2f}")

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)