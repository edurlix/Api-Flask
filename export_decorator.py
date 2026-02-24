import json
from abc import ABC, abstractmethod

class OrderExporter(ABC):
    @abstractmethod
    def export(self, order):
        pass

class BaseOrderExporter(OrderExporter):
    def export(self, order):
        return order.to_dict()
    
class OrderExporterDecorator(OrderExporter):
    def __init__(self, exporter):
        self._exporter = exporter
    
    def export(self, order):
        return self._exporter.export(order)
    
class JSONExporter(OrderExporterDecorator):
    def export(self, order):
        data = self._exporter.export(order)
        return json.dumps(data, indent=2, ensure_ascii=False)
    
class PlainTextExporter(OrderExporterDecorator):
    def export(self, order):
        data = self._exporter.export(order)
        text = f"""
            PEDIDO: {data['id']}
            CLIENTE: {data['cliente']}
            TIPO: {data['tipo_cliente']}
            ESTADO: {data['estado']}
            {'='*30}
            PRODUCTOS:
            """
        for item in data['items']:
            text += f" - {item['cantidad']}x {item['nombre_producto']} @ ${item['precio_unitario']:.2f} = ${item['subtotal']:.2f}\n"
            text += f"""
                SUBTOTAL: ${data['subtotal']:.2f}
                DESCUENTO: ${data['descuento']:.2f}
                TOTAL: ${data['total']:.2f}
                METODO DE PAGO: {data['metodo_pago']}
                FECHA: {data['creado_en']}
                {'='*30}
                """
        return text

class ExporterFactory:
    @staticmethod
    def get_exporter(format_type):
        base_exporter = BaseOrderExporter()
        if format_type.lower() == 'json':
            return JSONExporter(base_exporter)
        elif format_type.lower() in ['texto', 'txt', 'plain', 'text']:
            return PlainTextExporter(base_exporter)
        else:
            raise ValueError(f"Formato no soportado: {format_type}")
