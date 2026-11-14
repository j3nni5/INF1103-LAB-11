from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory 
import csv

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else: 
        with file:
            reader = csv.reader(file)
            next(reader) #skips header row 
            for row in reader:
                load = 0
                try:
                    product_type,product_id,name,price,stock = row #everything read from a csv is text
                    price = float(price)
                    stock = int(stock)
                    product = ProductFactory.create(product_type,product_id,name,price,stock) #create product, then need to update inventory
                    if inventory.add_product(product): #add_product returns True then load += 1/False if ID alrdy exist 
                        load += 1
                except ValueError as error:
                    print(f"Invalid row: {error}.")
    finally:
        print(f"Load attempt finished.")