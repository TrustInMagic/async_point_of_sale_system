class Order:
    @classmethod
    def make_menus(cls, order):
        burgers = []
        sides = []
        drinks = []

        order_copy = order[:]
        menu = []

        for item in order_copy:
            if item["category"] == "Burgers":
                burgers.append(item)
            elif item["category"] == "Sides":
                sides.append(item)
            elif item["category"] == "Drinks":
                drinks.append(item)
        
        if len(burgers) > 0 and len(sides) > 0 and len(drinks) > 0:
            price_ordered_burgers = cls.price_ordering(burgers)
            price_ordered_sides = cls.price_ordering(sides)
            price_ordered_drinks = cls.price_ordering(drinks)

        menu_number = min(len(burgers), len(sides), len(drinks))

        for i in range(menu_number):
            menu.append([price_ordered_burgers[i], price_ordered_sides[i], price_ordered_drinks[i]])
        
        for each_menu in menu:
            for menu_item in each_menu:
                for item in order_copy:
                    if menu_item == item:
                        order_copy.remove(menu_item)

        return menu, order_copy


    @classmethod
    def price_ordering(cls, item_list):
        working_list = item_list[:]
        ordered_by_price = []

        while len(working_list) > 0:
            item_to_be_moved = working_list[0]
            for item in working_list:
                if item["price"] > item_to_be_moved["price"]:
                    item_to_be_moved = item
            ordered_by_price.append(item_to_be_moved)
            working_list.remove(item_to_be_moved)
        
        return ordered_by_price


    @classmethod
    def print_order_summary(cls, menu, rest_of_order):
        TAX = 0.05
        subtotal = 0

        print("Here is a summary of your order: \n")
        for individual_menu in menu:
            print(f"${cls.calculate_menu_price(individual_menu)} Burger Combo")
            subtotal += cls.calculate_menu_price(individual_menu)
            for item in individual_menu:
                if item["id"] in range(1, 7):
                    print(cls.indent_lines(item["name"]))
                else:
                    print(cls.indent_lines(item['size'] + " " + item['subcategory']))
        
        for item in rest_of_order:
            if item["id"] in range(1, 7):
                print(f"${item['price']} {item['name']}")
                subtotal += item['price']
            else:
                print(f"${item['price']} {item['size']} {item['subcategory']}")
                subtotal += item['price']

        tax_amount = subtotal * TAX
        total = subtotal + tax_amount
        return round(subtotal, 2), round(tax_amount, 2), round(total, 2)
        

        
    @classmethod
    def calculate_menu_price(cls, menu):
        total_price = 0

        for item in menu:
            total_price += item["price"]

        discounted_price = total_price * 0.85
        return round(discounted_price, 2)

    
    @staticmethod
    def indent_lines(text):
        spaces = "  "
        return spaces + text        






