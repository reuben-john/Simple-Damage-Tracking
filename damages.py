"""
This is a simple script to track ebay shipping and warehouse related damages.

It currently saves all data to csv files instead of a database.
"""

import csv
import time

from terminaltables import AsciiTable


def main_menu():
    """
    This displays the main menu and allows the user to navigate to submenus  
    :return: str 
    """
    while True:
        print('')
        print('Welcome to the ShopCrownhouse damage tracking system')
        print('')
        print('What would you like to do?')
        for k, v in main_menu_codes.items():  # Prints out main menu
            print(k, v)
        print('q Quit')
        print('')
        menu_choice = input('Please enter your choice: ')
        while menu_choice not in main_menu_codes.keys():  # Quits if q is chosen
            if menu_choice == 'q':
                break
            print('That is not an option, please try again.')
            print('')
            menu_choice = input('Please enter your choice: ')
        return menu_choice


def add_damages_menu(loss_type):
    """
    This displays the damage entry menu. It allows users to choose what type of damage they wish to log.
    It uses the loss_type to pull the appropriate variable then prints out the menu.
    :param loss_type: str
    :return: str
    """
    while True:
        print('What type of damage do you wish to log?')
        # Checks if logging order damages or warehouse damages then pulls the appropriate menu data
        if loss_type == 'order':
            codes = order_damages_codes
        elif loss_type == 'warehouse':
            codes = warehouse_damages_codes
        for k, v in codes.items():  # Prints out damage menu choices
            print(k, v)
        print('b Go Back')
        print('')
        damage_choice = input('Please enter your choice: ')
        while damage_choice not in codes.keys():  # Goes to previous menu is b is chosen
            if damage_choice == 'b':
                break
            print('That is not an option, please try again.')
            print('')
            damage_choice = input('Please enter your choice: ')
        return damage_choice


def tally_warehouse_damages(csv_file):
    """
    This calculates warehouse damages from the warehouse_damages.csv file.
    It looks at each line in the csv file and multiplies the item cost by the number lost then adds it to the tally
    It prints the tally out at the end.
    :param csv_file: str 
    :return: None 
    """
    reader = csv.DictReader(csv_file, delimiter=',')
    box_loss_tally = 0
    for line in reader:
        # Tallies (Item Cost * Number Lost)
        box_loss_tally += float(str(line['Item Cost'])) * float(str(line['# Lost']))
    print('')
    print('Total Warehouse Loss: $' + str('{:.2f}'.format(box_loss_tally)))  # Prints tallied warehouse losses


def tally_order_damages(csv_file):
    """
    This calculates product losses and shipping losses from the order_damages.csv file.
    For each line in the csv file, it multiplies the item cost by the number lost then adds it to the product tally
    It then also reads the shipping loss for that line and adds it to the shipping tally.
    It prints both tallies out at the end.
    :param csv_file: str
    :return: None
    """
    reader = csv.DictReader(csv_file, delimiter=',')
    shipping_tally = 0
    product_tally = 0
    for line in reader:
        shipping_tally += float(line['Ship Loss'])  # Tallies shipping losses
        # Tallies (Item Cost * Number Lost)
        product_tally += float(str(line['Item Cost'])) * float(str(line['# Lost']))
    print('')
    print('Order Losses')
    print('Total Shipping Loss: $' + str('{:.2f}'.format(shipping_tally)))  # Prints tallied shipping losses
    print('Total Product Loss: $' + str('{:.2f}'.format(product_tally)))    # Prints tallied product losses


def damages_writer(data, path):
    """
    csv data writer to write the damages info to a new row of the csv file
    :param data: list
    :param path: str
    :return: None
    """
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)


def damages_reader(path):
    """
    csv data reader to read the csv files and return them
    :param path: str 
    :return: list
    """
    csv_data = []
    reader = csv.reader(path)
    for row in reader:
        csv_data.append(row)
    return csv_data


def cost_reader(path):
    """
    Opens csv file and converts the data to a dictionary. 
    This gives a dictionary containing a product key with a cost value.
    :param path: str
    :return: dict
    """
    reader = csv.reader(path)
    next(reader)
    costs = {rows[0]: rows[1] for rows in reader}
    return costs


def get_order_number():
    """
    Gets ebay order number from user then converts it to an int
    :return: int 
    """
    while True:
        try:
            ebay_order_number = int(input('What is the ebay order number? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return ebay_order_number


def get_order_cost():
    """
    Gets order cost from user then converts it to an float
    :return: float
    """
    while True:
        try:
            order_cost = float(input('What is the total order cost? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return order_cost


def get_shipping_cost():
    """
    Gets shipping cost from user then converts it to an float
    :return: float 
    """
    while True:
        try:
            shipping_cost = float(input('What is the shipping cost? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return shipping_cost


def get_shipping_lost():
    """
    Gets shipping loss from user then converts it to an float
    :return: float
    """
    while True:
        try:
            shipping_lost = float(input('How much did we lose on shipping? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return shipping_lost


def get_number_damaged():
    """
    Gets number of products damaged from user then converts it to an int
    :return: int
    """
    while True:
        try:
            if loss_type == 'warehouse':
                number_product_damaged = int(input('How many boxes are being thrown away? '))
            elif loss_type == 'order':
                number_product_damaged = int(input('How many individual items were lost? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return number_product_damaged


def get_custom_cost():
    """
    Allows user to enter a custom item cost for the items. This is to replace the default data entered in the starting
    variables
    :return: float 
    """
    while True:
        try:
            cost = float(input('Please enter a custom item cost: '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return cost

def get_product_cost(product, loss_type):
    """
    This uses the loss_type to pull the correct list of products. It then matches the product against the list and
    pulls the appropriate item cost. If the user has chosen custom, it asks the user for the custom cost.
    :param product: str
    :param loss_type: str
    :return: float
    """
    # Checks if logging order damages or warehouse damages then pulls the appropriate product list data
    if loss_type == 'order':
        codes = order_products
    elif loss_type == 'warehouse':
        codes = warehouse_products
    if product == 'c':  # Checks for custom item selection and allows user to enter the cost of it
        cost = get_custom_cost()
    else:
        cost = float(codes[product])  # Pulls cost value from product list and converts to float
    return cost


def get_product_types(loss_type):
    """
    This uses loss_Type to pull the correct list of products. It then sorts the product types and prints them out for
    the user to choose from. It also allows for a custom entry to be selected.
    :param loss_type: str 
    :return: str
    """
    # Checks if logging order damages or warehouse damages then pulls the appropriate product list data
    if loss_type == 'order':
        codes = order_products
    elif loss_type == 'warehouse':
        codes = warehouse_products
    product_names = sorted(codes.keys())  # Sorts the product types alphabetically for consistent display
    print('We have the following product types:')
    print('')
    for name in product_names:
        print(name)
    print('')
    print("To enter a custom product type, please type 'c'")
    print('')
    type_choice = input('What type of product was lost? ')
    while type_choice not in codes.keys():  # Allows for custom item type to be entered
        if type_choice == 'c':
            return type_choice
        print('That is not an option, please try again.')
        print('')
        type_choice = input('What type of product was lost? ')
    return type_choice


def info_form(loss_type):
    """
    This form goes through a list of questions for the user, collecting data on the loss to be logged. It then returns
    the results as a list.
    :param loss_type: str 
    :return: list
    """
    while True:
        todays_date = time.strftime("%m/%d/%Y")  # Date entered as mm/dd/yyyy
        if loss_type == 'order':  # only applies to order damages
            ebay_order_number = get_order_number()  # Asks user for ebay order number
            order_cost = get_order_cost()  # Asks user for total order cost (what the customer paid)
            shipping_cost = get_shipping_cost()  # Asks user for shipping cost (what the customer paid)
            shipping_lost = get_shipping_lost()  # Asks user for shipping loss (what we paid and lost)
        product_type_lost = get_product_types(loss_type)  # Asks user for the product type - accepts custom choice
        lost_product_cost = get_product_cost(product_type_lost, loss_type)  # Pulls item cost (custom allows user entry)
        if product_type_lost == 'c':  # If custom item was chosen, asks user for custom product type
            product_type_lost = input('Please enter your custom item type: ')
        number_product_damaged = get_number_damaged()  # Asks user for number of items lost
        # Checks if loss_type chosen is order damages or warehouse damages then compiles the variables to a list
        if loss_type == 'order':
            form = [todays_date, ebay_order_number, order_cost, shipping_cost, shipping_lost,
                    product_type_lost, lost_product_cost, number_product_damaged]
        elif loss_type == 'warehouse':
            form = [todays_date, product_type_lost, lost_product_cost, number_product_damaged]
        return form

# These 3 variables contain our menu choices for navigating the damage tracker
main_menu_codes = {'1': 'Add new order damages report', '2': 'Add new warehouse damages report',
                   '3': 'View Current Damages', '4': 'Tally Damages'}
order_damages_codes = {'1': 'Order lost in transit', '2': 'Returned product', '3': 'Bad Address', '4': 'Bad Product'}
warehouse_damages_codes = {'1': 'Box loss', '2': 'Item loss'}

order_csv = 'order_damages.csv'  # Path to order damages csv data file
warehouse_csv = 'warehouse_damages.csv'  # Path to warehouse damages csv data file
order_cost_csv = 'order_product_costs.csv'  # Path to product costs for order damages
warehouse_cost_csv = 'warehouse_product_costs.csv'  # Path to product costs for warehouse damages

# These 2 variables contain a list of product types we sell and a basic cost of goods
# These are used to calculate losses
# csv was chosen so other uses can easily edit product costs as they change
with open(order_cost_csv, 'r') as f_obj:  # Generates product cost list from csv file
    order_products = cost_reader(f_obj)

with open(warehouse_cost_csv, 'r') as f_obj:  # Generates product cost list from csv file
    warehouse_products = cost_reader(f_obj)

# This is the main program loop for the damage tracking system.
# It starts the main menu processes user input from that menu
while True:
    menu = main_menu()  # Loads the main menu
    if menu == 'q':  # Quits program if selected from main menu
        break
    elif menu == '1':
        loss_type = 'order'  # Assigns order identifier to specify this as order damages
        damage_type = add_damages_menu(loss_type)  # Opens damages menu
        if damage_type == 'b':  # Goes back to main menu if selected from damages menu
            continue
        data = info_form(loss_type)  # Starts data collection form
        damage_type = order_damages_codes[damage_type]  # Swaps number for text description of the type of damage
        data.append(damage_type)  # Adds damage to the end of the list containing info entered by user
        damages_writer(data, order_csv)  # Writes entry to csv file
    elif menu == '2':
        loss_type = 'warehouse'  # Assigns order identifier to specify this as warehouse damages
        damage_type = add_damages_menu(loss_type)  # Opens damages menu
        if damage_type == 'b':  # Goes back to main menu if selected from damages menu
            continue
        data = info_form(loss_type)  # Starts data collection form
        damage_type = warehouse_damages_codes[damage_type]  # Swaps number for text description of the type of damage
        data.append(damage_type)
        damages_writer(data, warehouse_csv)  # Writes entry to csv file
    elif menu == '3':
        with open(order_csv, 'r') as f_obj:  # Opens order damages csv file and reads the data
            csv_data = damages_reader(f_obj)
        damages_table = AsciiTable(csv_data)  # Creates table from csv data
        print(damages_table.table)  # Displays table to user
    elif menu == '4':
        with open(order_csv) as f_obj:  # Opens order csv file and tallies then prints order losses
            tally_order_damages(f_obj)
        with open(warehouse_csv) as f_obj:  # Opens warehouse csv file and tallies then prints warehouse losses
            tally_warehouse_damages(f_obj)
    continue  # Restarts main menu loop
