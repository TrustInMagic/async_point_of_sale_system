import asyncio
from inventory import Inventory
from order import Order


def display_catalogue(catalogue):
    burgers = catalogue["Burgers"]
    sides = catalogue["Sides"]
    drinks = catalogue["Drinks"]

    print("--------- Burgers -----------\n")
    for burger in burgers:
        item_id = burger["id"]
        name = burger["name"]
        price = burger["price"]
        print(f"{item_id}. {name} ${price}")

    print("\n---------- Sides ------------")
    for side in sides:
        sizes = sides[side]

        print(f"\n{side}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n---------- Drinks ------------")
    for beverage in drinks:
        sizes = drinks[beverage]

        print(f"\n{beverage}")
        for size in sizes:
            item_id = size["id"]
            size_name = size["size"]
            price = size["price"]
            print(f"{item_id}. {size_name} ${price}")

    print("\n------------------------------")


async def take_order():
    i = Inventory()
    order_id_list = []
    item_list = []
    
    order_list = []
    items_to_remove = []

    print("\nPlease enter the number of the items that you would like to add to your order. Enter q to complete your order.")

    while True: 
        order_id = input("Enter an item number: ")
        if order_id == "q":
            print("Placing order...")
            await asyncio.sleep(2)
            break
        
        if order_id.isdigit() == False or int(order_id) < 1:
            print("Please enter a valid number")
            continue
        elif int(order_id) > 20:
            print("Please enter a number below 21.")
            continue
        
        order_id_list.append(int(order_id))
 
        _ = asyncio.create_task(i.get_stock(int(order_id)))
        item = asyncio.create_task(i.get_item(int(order_id)))
      
        item_list.append(item)
    
    for item in item_list:
        order_list.append(await item)

    for idx, order_id in enumerate(order_id_list):
        item_in_stock = await i.decrement_stock(order_id)
        if item_in_stock == False:
            print(f"Unfortunately item number {order_id_list[idx]} is out of stock and has been removed from your order. Sorry!")
            item_to_remove = order_list[idx]
            items_to_remove.append(item_to_remove)
            
    for individual_item in items_to_remove:
        for each_item in order_list:
            if individual_item == each_item:
                order_list.remove(each_item)
    
    return order_list
   

async def main():
    i = Inventory()
    print("Welcome to the ProgrammingExpert Burger Bar!")
    print("Loading catalogue...")

    catalogue = await i.get_catalogue()
    display_catalogue(catalogue)

    menus, rest_of_order = Order.make_menus(await take_order())
    subtotal, tax, total = Order.print_order_summary(menus, rest_of_order)
    print()
    print(f"Subtotal: ${subtotal} \nTax: ${tax} \nTotal: ${total}")
    
    purchase_decision = input(f"Would you like to purchase this order for ${total}? ")

    if purchase_decision == "no":
        print("No problem, please come again!")
        another_order = input("Would you like to make another order (yes/no)? ")
        if another_order == "yes":
            await main()
        if another_order == "no":
            print("Goodbye!")
    if purchase_decision == "yes":
        print("Thank you for your order!")
        another_order = input("Would you like to make another order (yes/no)? ")
        if another_order == "yes":
            await main()
        if another_order == "no":
            print("Goodbye!")



if __name__ == "__main__":
    asyncio.run(main())

