from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product import Product
from supplier import Supplier 

class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
                stock: int, supplier: Supplier) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")