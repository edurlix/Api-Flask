class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.products = {}
            cls._instance.orders = {}
            cls._instance.order_counter = 0
        return cls._instance
    
    # Metodos para productos
    def add_product(self, product):
        self.products[product.id] = product
        return product
    
    def get_products(self):
        return list(self.products.values())
    
    def get_product(self, product_id):
        return self.products.get(product_id)
    
    # Metodos para pedidos
    def add_order(self, order):
        self.order_counter += 1
        order.id = f"ord-{self.order_counter:03d}"
        self.orders[order.id] = order
        return order
    
    def get_orders(self):
        return list(self.orders.values())
    
    def get_order(self, order_id):
        return self.orders.get(order_id)
    
    def update_order(self, order_id, updated_order):
        if order_id in self.orders:
            self.orders[order_id] = updated_order
            return True
        return False