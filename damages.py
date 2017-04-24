import csv
import time
from terminaltables import AsciiTable

main_menu_codes = {'1': 'Add new order damages report', '2': 'Add new warehouse damages report', '3': 'View Current Damages', '4': 'Tally Damages'}
order_damages_codes = {'1': 'Order lost in transit', '2': 'Returned product', '3': 'Bad Address', '4': 'Bad Product'}
warehouse_damages_codes = {'1': 'Box loss', '2': 'Item loss'}
order_product_list = {'beauty': 1, 'makeup': 0.4, 'food': 2, 'clothing': 4, 'consigner': 0, 'health': '1',
                      'household': '1.50', }
warehouse_product_list = {'beauty': 40, 'makeup': 50, 'food': 40, 'general': 20}


def main_menu():
    while True:
        print('')
        print('Welcome to the ShopCrownhouse damage tracking system')
        print('')
        print('What would you like to do?')
        for k, v in main_menu_codes.items():
            print(k, v)
        print('q Quit')
        print('')
        menu_choice = input('Please enter your choice: ')
        while menu_choice not in main_menu_codes.keys():
            if menu_choice == 'q':
                break
            print('That is not an option, please try again.')
            print('')
            menu_choice = input('Please enter your choice: ')
        return menu_choice


def add_damages_menu(loss_type):
    while True:
        print('What type of damage do you wish to log?')
        if loss_type == 'order':
            codes = order_damages_codes
        elif loss_type == 'warehouse':
            codes = warehouse_damages_codes
        for k, v in codes.items():
            print(k, v)
        print('b Go Back')
        print('')
        damage_choice = input('Please enter your choice: ')
        while damage_choice not in codes.keys():
            if damage_choice == 'b':
                break
            print('That is not an option, please try again.')
            print('')
            damage_choice = input('Please enter your choice: ')
        return damage_choice


def order_product_types():
    product_names = sorted(order_product_list.keys())
    print('We have the following product types:')
    print('')
    for name in product_names:
        print(name)
    print('')
    print("To enter a custom product type, please type 'c'")
    print('')
    type_choice = input('What type of product was lost? ')
    while type_choice not in order_product_list.keys():
        if type_choice == 'c':
            return type_choice
        print('That is not an option, please try again.')
        print('')
        type_choice = input('What type of product was lost? ')
    return type_choice


def warehouse_product_types():
    product_names = sorted(warehouse_product_list.keys())
    print('We have the following product types:')
    print('')
    for name in product_names:
        print(name)
    print('')
    print("To enter a custom product type, please type 'c'")
    print('')
    type_choice = input('What type of product was lost? ')
    while type_choice not in warehouse_product_list.keys():
        if type_choice == 'c':
            return type_choice
        print('That is not an option, please try again.')
        print('')
        type_choice = input('What type of product was lost? ')
    return type_choice


def get_order_number():
    while True:
        try:
            ebay_order_number = int(input('What is the ebay order number? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return ebay_order_number


def get_order_cost():
    while True:
        try:
            order_cost = float(input('What is the total order cost? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return order_cost


def get_shipping_cost():
    while True:
        try:
            shipping_cost = float(input('What is the shipping cost? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return shipping_cost


def get_shipping_lost():
    while True:
        try:
            shipping_lost = float(input('How much did we lose on shipping? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return shipping_lost


def get_order_number_damaged():
    while True:
        try:
            number_product_damaged = int(input('How many individual items were lost? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return number_product_damaged


def get_warehouse_number_damaged():
    while True:
        try:
            number_product_damaged = int(input('How many boxes are being thrown away? '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return number_product_damaged


def get_custom_cost():
    while True:
        try:
            cost = float(input('Please enter a custom item cost: '))
        except ValueError:
            print('Please enter a number.')
            continue
        else:
            return cost


def order_info_form():
    while True:
        todays_date = time.strftime("%m/%d/%Y")
        ebay_order_number = get_order_number()
        order_cost = get_order_cost()
        shipping_cost = get_shipping_cost()
        shipping_lost = get_shipping_lost()
        product_type_lost = order_product_types()
        lost_product_cost = order_product_cost(product_type_lost)
        if product_type_lost == 'c':
            product_type_lost = input('Please enter your custom item type: ')
        number_product_damaged = get_order_number_damaged()
        form = [todays_date, ebay_order_number, order_cost, shipping_cost, shipping_lost,
                product_type_lost, lost_product_cost, number_product_damaged]
        return form


def warehouse_info_form():
    while True:
        todays_date = time.strftime("%m/%d/%Y")
        product_type_lost = warehouse_product_types()
        lost_product_cost = warehouse_product_cost(product_type_lost)
        if product_type_lost == 'c':
            product_type_lost = input('Please enter your custom item type: ')
        number_product_damaged = get_warehouse_number_damaged()
        form = [todays_date, product_type_lost, lost_product_cost, number_product_damaged]
        return form


def order_product_cost(product):
    if product == 'c':
        cost = get_custom_cost()
    else:
        cost = order_product_list[product]
    return cost


def warehouse_product_cost(product):
    if product == 'c':
        cost = get_custom_cost()
    else:
        cost = warehouse_product_list[product]
    return cost


def tally_warehouse_damages(csv_file):
    reader = csv.DictReader(csv_file, delimiter=',')
    box_loss_tally = 0
    for line in reader:
        box_loss_tally += float(str(line['Item Cost'])) * float(str(line['# Lost']))
    print('')
    print('Total Warehouse Loss: $' + str('{:.2f}'.format(box_loss_tally)))


def tally_order_damages(csv_file):
    reader = csv.DictReader(csv_file, delimiter=',')
    shipping_tally = 0
    product_tally = 0
    for line in reader:
        shipping_tally += float(line['Ship Loss'])
        product_tally += float(str(line['Item Cost'])) * float(str(line['# Lost']))
    print('')
    print('Order Losses')
    print('Total Shipping Loss: $' + str('{:.2f}'.format(shipping_tally)))
    print('Total Product Loss: $' + str('{:.2f}'.format(product_tally)))


def order_damages_writer(data, path):
    """

    :param data: 
    :param path: 
    :return: 
    """
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)


def order_damages_reader(file_obj):
    """

    :param file_obj: 
    :return: 
    """
    csv_data = []
    reader = csv.reader(file_obj)
    for row in reader:
        csv_data.append(row)
    return csv_data


def warehouse_damages_writer(data, path):
    """
    
    :param data: 
    :param path: 
    :return: 
    """
    with open(path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)


def warehouse_damages_reader(file_obj):
    """

    :param file_obj: 
    :return: 
    """
    csv_data = []
    reader = csv.reader(file_obj)
    for row in reader:
        csv_data.append(row)
    return csv_data


while True:
    menu = main_menu()
    order_csv_path = 'damages.csv'
    warehouse_csv_path = 'warehouse.csv'
    if menu == 'q':
        break
    elif menu == '1':
        loss_type = 'order'
        damage_type = add_damages_menu(loss_type)
        if damage_type == 'b':
            continue
        data = order_info_form()
        damage_type = order_damages_codes[damage_type]
        data.append(damage_type)
        order_damages_writer(data, order_csv_path)
    elif menu == '2':
        loss_type = 'warehouse'
        damage_type = add_damages_menu(loss_type)
        if damage_type == 'b':
            continue
        data = warehouse_info_form()
        damage_type = warehouse_damages_codes[damage_type]
        data.append(damage_type)
        warehouse_damages_writer(data, warehouse_csv_path)
    elif menu == '3':
        with open(order_csv_path, 'r') as f_obj:
            csv_data = order_damages_reader(f_obj)
        damages_table = AsciiTable(csv_data)
        print(damages_table.table)
    elif menu == '4':
        with open('damages.csv') as f_obj:
            tally_order_damages(f_obj)
        with open('warehouse.csv') as f_obj:
            tally_warehouse_damages(f_obj)
    continue
