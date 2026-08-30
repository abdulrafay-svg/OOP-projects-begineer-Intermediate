import requests
from product import Product
from discount import DiscountFactory
from exceptions import OutOfStockError

def get_json_data():
    r = requests.get("https://dummyjson.com/products") 
    return (r.json()["products"])

def get_user_product(product):
    for i in range(len(product)):
        print(f"{i+1} {product[i]["title"]}")
    while True:
        try:
            I_D = int(input("choose id (1-30): "))
            if 1<= I_D<= 30:
                prod = product[I_D-1]
                PD = Product(prod)
                print("="*30)
                return PD
            else:
                print("\n[Error] please select from product (1-30): ")
                continue
        except ValueError:
            print("\n[Error] Index must be integer: ")

def get_product_price(selected_product):
    return selected_product.price

def get_customer_type():
    while True:
        try:
            print("\nSelect your customer type:")
            print("1. VIP customer")
            print("2. Regular customer")
            print("3. Wholesale customer")
            
            customer_category = int(input("Choose (1-2-3): "))

            if customer_category == 1:
                return "VIP customer"
            elif customer_category == 2:
                return "Regular customer"
            elif customer_category == 3 :
                return "Wholesale customer"
            else:
                print("\n[Error] Not a valid choice (choose from 1,2 or 3). ")
                continue
        except ValueError:
            print("\n[Error] Choose from 1-2-3 number not string.")
            continue

    
def get_order_quantity(product):
    while True:
        quantity = int(input("order Amount? "))
        try:
            product.reduce_stock(quantity)
            return quantity
        except OutOfStockError:
            print(f"\n[Error] Only {product.stock} left, requested {quantity}")
            continue

def get_strategy(customer_type,subtotal):
    strategy = DiscountFactory.get_discount_strategy(customer_type,subtotal)
    return strategy

def main():
    product = get_user_product(get_json_data())
    product_price = get_product_price(product)
    customer_type = get_customer_type()
    order_quantity = get_order_quantity(product)
    subtotal= product_price * order_quantity
    strategy = get_strategy(customer_type,subtotal)
    final_amount = strategy.calculate_discounted_amount()
    print("\n--- Receipt ---")
    print(f"Customer Category: {customer_type.title()}")
    print(f"Original Subtotal: ${subtotal}")
    print(f"Final Total Due:   ${final_amount:.2f}")


if __name__=="__main__":
    main()