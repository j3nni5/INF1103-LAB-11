import json
import os
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from order import Order

FILENAME = "inventory.json"


def find_supplier(suppliers: list[Supplier], supplier_id: str):
    for supplier in suppliers:
        if supplier.get_supplier_id() == supplier_id:
            return supplier
    return None


def load_data(inventory: Inventory, suppliers: list[Supplier]) -> None:
    if not os.path.exists(FILENAME):
        tech = Supplier("S001", "TechSource", "sales@techsource.com")
        digital = Supplier("S002", "DigitalHub", "hello@digitalhub.com")
        suppliers.append(tech)
        suppliers.append(digital)
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 14, tech, 2.5))
        inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, tech, 0.1))
        inventory.add_product(DigitalProduct("D001", "Photo Editor", 59.90, 100, digital, 450))
        return

    with open(FILENAME, "r") as file:
        data = json.load(file)

    for item in data["suppliers"]:
        suppliers.append(Supplier(item["supplier_id"], item["name"],
                                  item["contact_email"]))

    for item in data["products"]:
        supplier = find_supplier(suppliers, item["supplier_id"])
        if supplier is None:
            print(f"Supplier '{item['supplier_id']}' not found. "
                  f"Skipping product '{item['name']}'.")
            continue
        if item["type"] == "physical":
            product = PhysicalProduct(item["product_id"], item["name"],
                                      item["price"], item["stock"],
                                      supplier, item["weight"])
        elif item["type"] == "digital":
            product = DigitalProduct(item["product_id"], item["name"],
                                     item["price"], item["stock"],
                                     supplier, item["download_size"])
        else:
            print(f"Unknown product type: {item['type']}")
            continue
        inventory.add_product(product)


def save_data(inventory: Inventory, suppliers: list[Supplier]) -> None:
    supplier_list = []
    for supplier in suppliers:
        supplier_list.append(supplier.to_dict())
    data = {
        "suppliers": supplier_list,
        "products": inventory.get_products_as_dicts()
    }
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)


def show_menu() -> None:
    print("""
----------- MENU -----------
1. Display All Products
2. Add Product
3. Update Stock
4. Search Product
5. Remove Product
6. Add Supplier
7. Create Order
8. Save Inventory
9. Exit
----------------------------""")


def add_supplier(suppliers: list[Supplier]) -> None:
    supplier_id = input("Enter supplier ID: ")
    if find_supplier(suppliers, supplier_id) is not None:
        print(f"Supplier ID '{supplier_id}' already exists.")
        return
    name = input("Enter supplier name: ")
    email = input("Enter supplier email: ")
    suppliers.append(Supplier(supplier_id, name, email))
    print(f"Supplier '{name}' added successfully.")


def add_new_product(inventory: Inventory, suppliers: list[Supplier]) -> None:
    if len(suppliers) == 0:
        print("There are no suppliers yet. Please add a supplier first.")
        return

    print("Product type: 1. Physical   2. Digital")
    type_choice = input("Enter product type (1 or 2): ")
    if type_choice != "1" and type_choice != "2":
        print("Invalid product type.")
        return

    print("Available suppliers:")
    for supplier in suppliers:
        supplier.display_information()
    supplier_id = input("Enter supplier ID for this product: ")
    supplier = find_supplier(suppliers, supplier_id)
    if supplier is None:
        print(f"Supplier '{supplier_id}' not found. Product not added.")
        return

    product_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    try:
        price = float(input("Enter product price: "))
        stock = int(input("Enter product stock: "))
        if type_choice == "1":
            weight = float(input("Enter weight in kg: "))
            product = PhysicalProduct(product_id, name, price, stock,
                                      supplier, weight)
        else:
            download_size = float(input("Enter download size in MB: "))
            product = DigitalProduct(product_id, name, price, stock,
                                     supplier, download_size)
    except ValueError:
        print("Invalid number. Product not added.")
        return

    if inventory.add_product(product):
        print(f"Product '{name}' added successfully.")


def create_order(inventory: Inventory) -> None:
    order_id = input("Enter order ID: ")
    order = Order(order_id)
    print("Add items to the order. Press Enter on the product name to finish.")
    while True:
        name = input("Enter product name: ")
        if name == "":
            break
        product = inventory.search_product(name)
        if product is None:
            print(f"Product '{name}' not found in inventory.")
            continue
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid number. Item not added.")
            continue
        order.add_order_line(product, quantity)
    order.display_information()


inventory = Inventory()
suppliers = []
load_data(inventory, suppliers)

while True:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        inventory.display_all()

    elif choice == "2":
        add_new_product(inventory, suppliers)

    elif choice == "3":
        name = input("Enter product name to update stock: ")
        product = inventory.search_product(name)
        if product is None:
            print(f"Product '{name}' not found in inventory.")
        else:
            try:
                new_stock = int(input("Enter new stock quantity: "))
            except ValueError:
                print("Invalid number. Stock not changed.")
                continue
            if product.update_stock(new_stock):
                print(f"Stock for '{name}' updated to {new_stock}.")

    elif choice == "4":
        name = input("Enter product name to search: ")
        product = inventory.search_product(name)
        if product is None:
            print(f"Product '{name}' not found in inventory.")
        else:
            product.display_information()
            print("    Fulfilment:", product.get_fulfilment_info())
            if isinstance(product, CanBeShipped):
                print(f"    Shipping cost: ${product.calculate_shipping_cost():.2f}")

    elif choice == "5":
        product_id = input("Enter product ID to remove: ")
        if inventory.remove_product(product_id):
            print(f"Product '{product_id}' removed from the inventory.")
        else:
            print(f"Product '{product_id}' not found in inventory.")

    elif choice == "6":
        add_supplier(suppliers)

    elif choice == "7":
        create_order(inventory)

    elif choice == "8":
        save_data(inventory, suppliers)
        print("Inventory saved successfully.")

    elif choice == "9":
        save_data(inventory, suppliers)
        print("Exiting the program. Inventory saved.")
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 9.")