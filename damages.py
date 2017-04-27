"""
This is a simple script to track ebay shipping and warehouse related damages.

It currently saves all data to csv files instead of a database.
"""

import csv
from os import path
from time import strftime

from terminaltables import AsciiTable
from colorama import init, Fore


def file_check(ordam, orpro_cost, wardam, warpro_cost, master):
    """
    Checks if csv files already exist. If not, it creates them using the appropriate header info from the csv_master
    It then checks if the created file is one containing pricing data and warns the user that they need
    to add data in to the csv file. It adds in dummy data.
    
    :param str ordam: Order Damages csv file
    :param str orpro_cost: Order Product Costs csv file 
    :param str wardam: Warhouse Damages csv file
    :param str warpro_cost: Warhouse Product Costs csv file
    :param dict master: Contains the master header info linked to the csv file name
    :return: None
    """
    for file in (ordam, orpro_cost, wardam, warpro_cost):
        if path.isfile(file) is False:
            damages_writer(master[file], file)
            print('{}{} did not exist and was created for you.'.format(col_ltwht, file))
            print('')
            if file in (orpro_cost, warpro_cost):
                damages_writer(['ENTER PRODUCT DATA',0], file)
                print('')
                print('       {}{} contains price data used to calculate costs.'.format(col_ltred, file))
                print('       It is currently EMPTY')
                print('       Please enter pricing data into {} before proceeding'.format(file))
                print('')


def main_menu():
    """
    This displays the main menu and allows the user to navigate to submenus
    
    :return: Returns the key entered by the user
    """
    while True:
        print('')
        print('{}Welcome to the ShopCrownhouse damage tracking system'.format(col_ltwht))
        print('')
        print('What would you like to do?')
        print('')
        for k, v in main_menu_codes.items():  # Prints out main menu
            print(' {}{}  {}{}'.format(col_ltred, k, col_wht, v))
        print(' {}q  {}Quit'.format(col_ltred, col_wht))
        print(col_ltwht)
        menu_choice = key_check('Please enter your choice: ')
        while menu_choice not in main_menu_codes.keys():  # Quits if q is chosen
            if menu_choice == 'q':
                break
            print('That is not an option, please try again.')
            print('')
            menu_choice = key_check('Please enter your choice: ')
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
        else:
            codes = warehouse_damages_codes
        # Prints out damage menu choices
        for k, v in codes.items():
            print(' {}{}  {}{}'.format(col_ltred, k, col_wht, v))
        print(' {}b  {}Go Back'.format(col_ltred, col_wht))
        print(col_ltwht)
        damage_choice = key_check('Please enter your choice: ')
        # Goes to previous menu if b is chosen
        while damage_choice not in codes.keys():
            if damage_choice == 'b':
                break
            print('That is not an option, please try again.')
            print('')
            damage_choice = key_check('Please enter your choice: ')
        return damage_choice


def tally_damages(order_file, warehouse_file):
    """
    This calculates product losses and shipping losses from the order_damages.csv file.
    For each line in the csv file, it multiplies the item cost by the number lost then adds it to the product tally
    It then also reads the shipping loss for that line and adds it to the shipping tally.
    It prints both tallies out at the end.
    
    :param str order_file: Order Damages csv file
    :param str warehouse_file: Warehouse Damages csv file
    :return: None
    """
    order = csv.DictReader(order_file, delimiter=',')
    warehouse = csv.DictReader(warehouse_file, delimiter=',')
    shipping_tally = 0
    product_tally = 0
    for line in order:
        # Tallies shipping losses
        shipping_tally += float(line['Ship Loss'])
        # Tallies (Item Cost * Number Lost)
        product_tally += float(str(line['Item Cost'])) * float(str(line['# Lost']))
    box_loss_tally = 0
    for line in warehouse:
        # Tallies (Item Cost * Number Lost)
        box_loss_tally += float(str(line['Item Cost'])) * float(str(line['# Lost']))
    print('')
    # Prints tallied shipping losses
    print('{}Total Shipping Loss: {}${:.2f}'.format(col_ltcyn, col_ltgrn, shipping_tally))
    # Prints tallied product losses
    print('{}Total Product Loss: {}${:.2f}'.format(col_ltcyn, col_ltgrn, product_tally))
    print('')
    # Prints tallied warehouse losses
    trim_loss = str('{:.2f}'.format(box_loss_tally))
    print('{}Total Warehouse Loss: {}${}{}'.format(col_ltcyn, col_ltgrn, trim_loss, col_ltwht))


def damages_writer(data, path):
    """
    csv data writer to write the damages info to a new row of the csv file
    
    :param list data: Data to be written to csv file
    :param str path: csv file to write data to
    :return: None
    """
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)


def damages_reader(path):
    """
    csv data reader to read the csv files and return them
    
    :param str path: csv file to pull data from
    :return: data pulled from csv file
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
    
    :param str path: csv file to pull data from
    :return: data read from csv file
    """
    reader = csv.reader(path)
    next(reader)
    costs = {rows[0]: rows[1] for rows in reader}
    return costs


def int_check(question):
    """
    Asks for user inputs and converts to int. 
    It asks them to try again if they enter something else
    
    :param str question: question to ask user 
    :return: answer as an int
    """
    while True:
        try:
            checked_input = int(key_check(question))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return checked_input


def float_check(question):
    """
    Asks for user inputs and converts to float. 
    It asks them to try again if they enter something else
    
    :param str question: question to ask user
    :return: answer as a float
    """
    while True:
        try:
            checked_input = float(key_check(question))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return checked_input


def key_check(line):
    while True:
        try:
            answer = input(line)

        except KeyboardInterrupt:
            print('')
            print('To copy something, please highlight the text first')
            print('To exit, please use the menu instead')
            continue
        else:
            return answer


def get_product_cost(product, loss_type):
    """
    This uses the loss_type to pull the correct list of products. It then matches the product against the list and
    pulls the appropriate item cost. If the user has chosen custom, it asks the user for the custom cost.
    
    :param str product: type of product used to cost lookup
    :param str loss_type: type of loss we are tracking
    :return: cost of product as float
    """
    # Checks if logging order damages or warehouse damages then pulls the appropriate product list data
    if loss_type == 'order':
        codes = order_products
    else:
        codes = warehouse_products
    # Checks for custom item selection and allows user to enter the cost of it
    if product == 'c':
        cost = float_check('Please enter a custom item cost: ')
    else:
        # Pulls cost value from product list and converts to float
        cost = float(codes[product])
    return cost


def get_product_types(loss_type):
    """
    This uses loss_Type to pull the correct list of products. It then sorts the product types and prints them out for
    the user to choose from. It also allows for a custom entry to be selected.
    
    :param str loss_type: type of loss we are tracking 
    :return: product type chosen from list
    """
    # Checks if logging order damages or warehouse damages then pulls the appropriate product list data
    if loss_type == 'order':
        codes = order_products
    else:
        codes = warehouse_products
    # Sorts the product types alphabetically for consistent display
    product_names = sorted(codes.keys())
    print('We have the following product types:')
    print('')
    for name in product_names:
        print(' {}{}'.format(col_ltred, name))
    print('')
    print("{}To enter a custom product type, please type '{}c{}'".format(col_wht, col_ltred, col_wht))
    print(col_ltwht)
    type_choice = key_check('What type of product was lost? ')
    # Allows for custom item type to be entered
    while type_choice not in codes.keys():
        if type_choice == 'c':
            break
        print('That is not an option, please try again.')
        print('')
        type_choice = key_check('What type of product was lost? ')
    return type_choice


def info_form(loss_type):
    """
    This form goes through a list of questions for the user, collecting data on the loss to be logged. It then returns
    the results as a list.
    
    :param str loss_type: type of loss we are tracking
    :return: answers to input questions in form of list
    """
    while True:
        # We want to log the date the damage report was filed as mm/dd/yyyy
        todays_date = strftime("%m/%d/%Y")
        # These questions are only pertinent to order losses
        if loss_type == 'order':
            # We use the ebay order number here so we have an identifier if we need to verify data
            ebay_order_number = int_check('What is the ebay order number? ')
            order_cost = float_check('What is the total order cost? ')
            shipping_cost = float_check('What is the shipping cost? ')
            shipping_lost = float_check('How much did we lose on shipping? ')
        # Product types and costs are customizable by the user via csv files
        # It also allows for a custom item type/price to be entered
        product_type_lost = get_product_types(loss_type)
        lost_product_cost = get_product_cost(product_type_lost, loss_type)
        # If custom item was chosen, gets custom product type
        if product_type_lost == 'c':
            product_type_lost = key_check('Please enter your custom item type: ')
        # Warehouse damages are measured in boxes not items, thus the split between the two
        if loss_type == 'order':
            number_product_damaged = float_check('How many individual items were lost? ')
        else:
            number_product_damaged = float_check('How many boxes are being thrown away? ')
        # Since we use different csv sheets for orders vs warehouse damages, we need the data ordered differently
        if loss_type == 'order':
            form = [todays_date, ebay_order_number, order_cost, shipping_cost, shipping_lost,
                    product_type_lost, lost_product_cost, number_product_damaged]
        else:
            form = [todays_date, product_type_lost, lost_product_cost, number_product_damaged]
        return form

# These 3 variables contain our menu choices for navigating the damage tracker
main_menu_codes = {'1': 'Add new order damages report',
                   '2': 'Add new warehouse damages report',
                   '3': 'View Current Damages',
                   '4': 'Tally Damages'}
order_damages_codes = {'1': 'Order lost in transit',
                       '2': 'Returned product',
                       '3': 'Bad Address',
                       '4': 'Bad Product'}
warehouse_damages_codes = {'1': 'Box loss',
                           '2': 'Item loss'}

# I assigned the file paths to variables in case the locations change in the future.
# Currently they are in the same folder
order_csv = 'order_damages.csv'
warehouse_csv = 'warehouse_damages.csv'
order_cost_csv = 'order_product_costs.csv'
warehouse_cost_csv = 'warehouse_product_costs.csv'

# This is the header data for the csv files
# It is used to create new csv files if someone deletes one
csv_master = {order_csv: ['Date', 'Order #', 'Order Cost', 'Ship Cost', 'Ship Loss', 'Item Type',
                                    'Item Cost', '# Lost', 'Loss Type'],
              order_cost_csv: ['Product Type', 'Product Cost'],
              warehouse_csv: ['Date', 'Item Type', 'Item Cost', '# Lost', 'Loss Type'],
              warehouse_cost_csv: ['Product Type', 'Product Cost']}

# Colorama needs initialized before it works. It allows terminal colors in Windows
init()

# Assigns colors used in menus to shorter variables
col_ltwht = Fore.LIGHTWHITE_EX
col_ltred = Fore.LIGHTRED_EX
col_wht = Fore.WHITE
col_ltcyn = Fore.LIGHTCYAN_EX
col_ltgrn = Fore.LIGHTGREEN_EX
col_reset = Fore.RESET

# This checks that the csv files are created. It does not verify the header data
file_check(order_csv, order_cost_csv, warehouse_csv, warehouse_cost_csv, csv_master)


# These 2 variables contain a list of product types we sell and a basic cost of goods
# These are used to calculate losses
# csv was chosen so other uses can easily edit product costs as they change
with open(order_cost_csv, 'r') as order_obj:
    order_products = cost_reader(order_obj)

with open(warehouse_cost_csv, 'r') as warehouse_obj:
    warehouse_products = cost_reader(warehouse_obj)

# This is the main program loop for the damage tracking system.
# It starts the main menu and processes user input from that menu
# loss_type is used in few if/else switches
# It lets functions know whether they should return info for order damages or warehouse damages
while True:
    # Opens the main menu
    menu = main_menu()
    # Quits program if selected from main menu
    if menu == 'q':
        break
    elif menu == '1':
        loss_type = 'order'
        # Opens damages menu
        damage_type = add_damages_menu(loss_type)
        # Goes back to main menu if selected from damages menu
        if damage_type == 'b':
            continue
        # Starts data collection form
        data = info_form(loss_type)
        # Swaps number for text description of the type of damage
        # then adds it to the end the generated list before writing the data to a csv file
        damage_type = order_damages_codes[damage_type]
        data.append(damage_type)
        damages_writer(data, order_csv)
    elif menu == '2':
        # Opens damages menu
        loss_type = 'warehouse'
        damage_type = add_damages_menu(loss_type)
        # Goes back to main menu if selected from damages menu
        if damage_type == 'b':
            continue
        # Starts data collection form
        data = info_form(loss_type)
        # Swaps number for text description of the type of damage
        # then adds it to the end the generated list before writing the data to a csv file
        damage_type = warehouse_damages_codes[damage_type]
        data.append(damage_type)
        damages_writer(data, warehouse_csv)
    # Menu 3 generates a table from csv data. This is the data the user previously entered
    # Currently it only shows the order damages
    elif menu == '3':
        with open(order_csv, 'r') as order_obj:
            csv_data = damages_reader(order_obj)
        damages_table = AsciiTable(csv_data)
        print(damages_table.table)
    # Menu 4 generates loss tallies for order and warehouse losses and prints them out
    elif menu == '4':
        with open(order_csv) as order_obj:
            with open(warehouse_csv) as warehouse_obj:
                tally_damages(order_obj, warehouse_obj)
    continue
