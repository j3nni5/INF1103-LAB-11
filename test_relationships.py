from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def check(description: str, condition: bool) -> None:
    if condition:
        print(f"  PASS: {description}")
    else:
        print(f"  FAIL: {description}")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


print("=== Section 2: Association (Supplier and Product) ===")
supplier = Supplier("S100", "Acme Supplies", "sales@acme.com")
laptop = PhysicalProduct("P100", "Gaming Laptop", 1500.00, 5, supplier, 2.5)
ebook = DigitalProduct("D100", "Python Ebook", 19.90, 100, supplier, 5)

print("Supplier info through the physical product:")
laptop.get_supplier().display_information()
print("Supplier info through the digital product:")
ebook.get_supplier().display_information()
check("Both products refer to the same Supplier object",
      laptop.get_supplier() is supplier and ebook.get_supplier() is supplier)


del supplier
print("After 'del supplier' (only the variable name is deleted):")
laptop.get_supplier().display_information()
check("Product can still show its supplier information", True)


print("\n=== Section 3: Aggregation (Inventory and Product) ===")
inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(laptop)
inventory_a.add_product(ebook)
check("Inventory A has the laptop", inventory_a.find_product("P100") is laptop)


inventory_a.remove_product("P100")
check("Laptop is no longer in Inventory A", inventory_a.find_product("P100") is None)
print("Using the laptop after removing it from Inventory A:")
laptop.display_information()

inventory_b.add_product(laptop)
check("The SAME laptop object is now in Inventory B",
      inventory_b.find_product("P100") is laptop)

inventory_a.remove_product("D100")
check("Inventory A is now empty", len(inventory_a.get_products()) == 0)
check("Ebook still exists after Inventory A was emptied",
      ebook.get_name() == "Python Ebook")


print("\n=== Section 4: Composition (Order and OrderLine) ===")
order_1 = Order("O001")
order_1.add_order_line(laptop, 1)
order_1.add_order_line(ebook, 2)
order_1.display_information()
check("Order total is correct (1500.00 + 2 x 19.90 = 1539.80)",
      round(order_1.calculate_total(), 2) == 1539.80)


order_2 = Order("O002")
order_2.add_order_line(laptop, 3)
line_1 = order_1.get_order_lines()[0]
line_2 = order_2.get_order_lines()[0]
check("Each Order created its OWN OrderLine", line_1 is not line_2)
check("Both lines point to the SAME Product object",
      line_1.get_product() is line_2.get_product())

order_1.remove_order_line("D100")
print("After removing the ebook line from order 1:")
order_1.display_information()


print("\n=== Section 6: Liskov Substitution Principle ===")
print("show_product_details() with a PhysicalProduct:")
show_product_details(laptop)
print("show_product_details() with a DigitalProduct:")
show_product_details(ebook)

print("update_stock() works the same way on both subclasses:")
def update_is_rejected(product: Product, quantity: int) -> bool:
    try:
        product.update_stock(quantity)
    except ValueError:
        return True
    return False


laptop.update_stock(10)
ebook.update_stock(10)
check("Physical: update_stock(10) accepted", laptop.get_stock() == 10)
check("Digital: update_stock(10) accepted", ebook.get_stock() == 10)
check("Physical: negative stock rejected", update_is_rejected(laptop, -1))
check("Digital: negative stock rejected", update_is_rejected(ebook, -1))


print("\n=== Section 7: Polymorphism ===")
shop = Inventory()
shop.add_product(laptop)
shop.add_product(ebook)


for product in shop.get_products():
    product.display_information()
    print("  Fulfilment:", product.get_fulfilment_info())