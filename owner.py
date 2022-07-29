import sqlite3

def db_request(request):
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute(request)
    if request.split()[0].upper() == 'SELECT':
        col_names = [description[0] for description in c.description]
        return {'data': c.fetchall(), 'col_names': col_names}
    else:
        db.commit()


def change_price():
    a = db_request("SELECT * FROM catalog")['data']
    col_names = db_request("SELECT * FROM catalog")['col_names']
    print(*col_names, sep=' ')
    print(*a, sep='\n')

    print('Введите номер товара:')
    inp = input()
    if_order = False
    for data in a:
        if inp in str(data[0]):
            print('Введите цену:')
            price = input()
            if_order = True

    if not if_order:
        print('Заказа с таким номером в базе нет, проверьте введенный номер и повторите попытку.')
        return change_order_status()
    try:
        db_request(f"UPDATE catalog SET price = {price} WHERE id = {inp}")
    except sqlite3.OperationalError:
        print('В разделе цена нужно вводить целочисленное значение')
    choose_command()


def change_quan():
    a = db_request("SELECT * FROM catalog")['data']
    col_names = db_request("SELECT * FROM catalog")['col_names']
    print(*col_names, sep=' ')
    print(*a, sep='\n')

    print('Введите номер товара:')
    inp = input()
    if_order = False
    for data in a:
        if inp in str(data[0]):
            print('Введите колличество:')
            amount = input()
            if_order = True
    if not if_order:
        print('Заказа с таким номером в базе нет, проверьте введенный номер и повторите попытку.')
        return change_order_status()
    try:
        db_request(f"UPDATE catalog SET amount = {amount} WHERE id = {inp}")
    except sqlite3.OperationalError:
        print('В разделе колличество нужно указать целое число')
        return change_quan()

    choose_command()


def non_payed_orders():
    a = db_request("SELECT order_id, status, userID, catID FROM orders WHERE status < 4 GROUP BY order_id")
    print(a['col_names'])
    print(*a['data'], sep='\n')
    choose_command()


def change_order_status():
    a = db_request("SELECT order_id, status, userID, catID FROM orders GROUP BY order_id")['data']
    print(db_request("SELECT order_id, status, userID, catID FROM orders GROUP BY id")['col_names'])
    print(*a, sep='\n')

    print('Введите номер заказа:')
    inp = input()
    if_order = False
    for data in a:
        if inp in str(data[0]):
            print('Чтобы установить новый статус заказа, выберите его номер в списке:')
            print(db_request("SELECT *  FROM status")['col_names'])
            print(*db_request("SELECT *  FROM status")['data'], sep='\n')
            st_id = input()
            if_order = True
    if not if_order:
            print('Заказа с таким номером в базе нет, проверьте введенный номер и повторите попытку.')
            return change_order_status()
    try:
        db_request(f"UPDATE orders SET status = {st_id} WHERE id = {inp}")
    except sqlite3.OperationalError:
        print('В разделе колличество нужно указать целое число')
        return change_order_status()
    choose_command()


def watch_items(user):
    print('Наименование, Цена, Количество')
    print(*db_request("SELECT name, price, amount FROM catalog")['data'], sep='\n')
    if user == 'admin':
        choose_command()


def choose_command():
    commands = {
        'watch_items("admin")': '0. Просмотреть каталог',
        'change_price()': '1. Изменить цену товара',
        'change_quan()': '2. Изменить количество товара',
        'non_payed_orders()': '3. Посмотреть открытые заказы',
        'change_order_status()': '4. Изменить статус заказа',
        'exit()': '5. Выйти'
    }

    print('Введите номер команды:')
    print(*commands.values(), sep='\n')
    command = input()
    if int(command) in range(len(list(commands.keys()))):
        return eval(list(commands.keys())[int(command)])
    else:
        print('Команды с таким номером нет, поробуйте еще раз.')
        return choose_command()

def exit():
    import common
    return common.main()
