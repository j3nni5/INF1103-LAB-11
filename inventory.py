from __future__ import annotations
from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        for item in self.__products:
            if item.get_product_id() == product.get_product_id():
                print(f"Product ID '{product.get_product_id()}' already exists.")
                return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        for item in self.__products:
            if item.get_product_id() == product_id:
                self.__products.remove(item)
                return True
        return False

    def find_product(self, product_id: str) -> Product | None:
        for item in self.__products:
            if item.get_product_id() == product_id:
                return item
        return None

    def search_product(self, name: str) -> Product | None:
        for item in self.__products:
            if item.get_name().lower() == name.lower():
                return item
        return None

    def display_all(self) -> None:
        if len(self.__products) == 0:
            print("The inventory is empty.")
            return
        for item in self.__products:
            item.display_information()

    def get_products(self) -> list[Product]:
        return list(self.__products)

    def get_products_as_dicts(self) -> list[dict]:
        result = []
        for item in self.__products:
            result.append(item.to_dict())
        return result