from flask import Flask, request, jsonify
from database import Database
from models import Product, Order, OrderItem
from order_builder import OrderBuilder
from export_decorator import ExporterFactory

app = Flask(__name__)
db = Database()

# Endpoints de products
@app.route('/productos', methods=['GET'])
def list_products():
    products = db.get_products()
    return jsonify([p.to_dict() for p in products]), 200

@app.route('/productos', methods=['POST'])
def create_product():
    data = request.get_json()

    if not all(k in data for k in ('nombre', 'precio', 'categoria')):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    product = Product(data['nombre'], data['precio'], data['categoria'])
    db.add_product(product)

    return jsonify(product.to_dict()), 201

# endpoint de pedidos con todos los patrones
@app.route('/pedidos', methods=['POST'])
def create_order():
    data = request.get_json()

    try:
        builder = OrderBuilder()
        builder.set_client(data['cliente'], data['tipo_cliente'])
        builder.set_payment_method(data['metodo_pago'])

        for item_data in data['items']:
            builder.add_item(item_data['producto_id'], item_data['cantidad'])

        order = builder.build()

        payment_result = order.process_payment()
        print(f"Resultado del pago {payment_result}")

        saved_order = db.add_order(order)

        return jsonify(saved_order.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pedidos', methods=['GET'])
def list_orders():
    orders = db.get_orders()
    return jsonify([o.to_dict() for o in orders]), 200

@app.route('/pedidos/<id>', methods=['GET'])
def get_order(id):
    order = db.get_order(id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404
    return jsonify(order.to_dict()), 200

@app.route('/pedidos/<id>/avanzar', methods=['PUT'])
def advance_order(id):
    order = db.get_order(id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404
    
    try:
        order.next_state()
        db.update_order(id, order)
        return jsonify({
            "mensaje": "Estado actualizado",
            "nuevo_estado": order.state.get_name()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/pedidos/<id>/cancelar', methods=['PUT'])
def cancel_order(id):
    order = db.get_order(id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404
    
    try:
        order.cancel()
        db.update_order(id, order)
        return jsonify({
            "mensaje": "Pedido cancelado",
            "estado": order.state.get_name()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/pedidos/<id>/exportar', methods=['GET'])
def export_order(id):
    order = db.get_order(id)
    if not order:
        return jsonify({"error": "Pedido no encontrado"}), 404
    format_type = request.args.get('formato', 'json')

    try:
        exporter = ExporterFactory.get_exporter(format_type)
        exported_data = exporter.export(order)

        if format_type.lower() == 'json':
            return app.response_class(
                response=exported_data,
                status=200,
                mimetype='application/json'
            )
        else:
            return app.response_class(
                response=exported_data,
                status=200,
                mimetype='text/plain'
            )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)