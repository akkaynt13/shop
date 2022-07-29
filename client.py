import sqlite3
import owner

def create_order(user):
    print('Введите название товара из перечисленных ниже:')
    item_list = []
    a = owner.db_request('SELECT name FROM catalog')['data']
    for i in a:
        item_list.append(str(str(i).split(sep=','))[3:].replace('"', '').replace("'", '').split(sep=',')[0])
    print(item_list)
    name = input()
    if name in list:
        cat_id = list.index(name)
        print('Введите количество:')
        amount = input()
    else:
        print('Такого товара в каталоге нет, просмотрите список еще раз и повторите ввод')
        return create_order(user)

    user_id = str(owner.db_request(f"SELECT id FROM users WHERE login = '{user}'")['data'])[2:3]

    owner.db_request(f"INSERT INTO orders (id, order_id, status, userID, catID, amount) "
                     f"VALUES((SELECT COUNT(id) FROM orders)+1, "
                     f"(SELECT COUNT(id) FROM orders)+1, '0', '{user_id}', '{cat_id}', {amount})")

    choose_command(user)


def watch_orders(user):
    a = owner.db_request("SELECT orders.order_id, status.status, catalog.name, orders.amount "
                         "FROM ((orders "
                         "INNER JOIN catalog ON catalog.id = orders.catID)"
                         "INNER JOIN status ON status.id = orders.status)"
                         f"WHERE userid = (SELECT id FROM users WHERE login = '{user}')"
                         "ORDER BY orders.order_id")
    col_names = a['col_names']
    print(*col_names, sep=' ')
    print(*a['data'], sep='\n')
    choose_command(user)


def change_order(user):
    count = owner.db_request(f"SELECT order_id, status, date FROM orders "
                             f"WHERE userid = (SELECT id FROM users WHERE login = '{user}') GROUP BY order_id")['data']
    print(*count, sep='\n')
    if len(count) > 1:
        print('Введите номер заказа, который хотите изменить')
        order_id = input()
        if order_id in [str(i)[1] for i in count]:
            print('Выберите изменение из списка ниже:')
            options = {
                'add_item(order_id, user)': '0. Добавить товар',
                'change_amount(order_id, user)': '1. Поменять количество',
                'delete_order(order_id, user)': '2. Удалить заказ',
                'choose_command(user)': '3. Назад'
            }
            print(*options.values(), sep='\n')
            option = input()
            if int(option) in range(len(options.values())):
                return eval(list(options.keys())[int(option)])
            else:
                return change_order(user)
        else:
            print('Заказа с таким номером нет. Проверьте данные и повторите ввод.')
            return change_order(user)
    else:
        print('Выберите изменение из списка ниже:')
        print(*options.values(), sep='\n')
        order_id = str(count)[2]
        option = input()
        if int(option) in range(len(options.values())):
            return eval(list(options.keys())[int(option)])
        else:
            return change_order(user)


def choose_command(user):
    commands = {
        'create_order(user)': '0. Создать заказ',
        'watch_orders(user)': '1. Посмотреть мои заказы',
        'change_order(user)': '2. Изменить заказ',
        'watch_items(user)': '3. Посмотреть каталог',
        'owner.exit()': '4. Выход'
    }

    print('\nВведите номер команды.')
    print(*commands.values(), sep='\n')
    command = input()
    if int(command) in range(len(list(commands.keys()))):
        return eval(list(commands.keys())[int(command)])
    else:
        print('Команды с таким номером нет, поробуйте еще раз.')
        return choose_command(user)


def add_item(order_id, user):
    print('Введите название товара из перечисленных ниже:')
    item_list = []
    a = owner.db_request('SELECT name FROM catalog')['data']
    for i in a:
        item_list.append(str(str(i).split(sep=','))[3:].replace('"', '').replace("'", '').split(sep=',')[0])
    print(item_list)
    name = input()
    if name in list:
        cat_id = list.index(name)
        print('Введите количество:')
        amount = input()
    else:
        print('Такого товара в каталоге нет, просмотрите список еще раз и повторите ввод')
        return create_order(user)

    user_id = str(owner.db_request(f"SELECT id FROM users WHERE login = '{user}'")['data'])[2:3]

    owner.db_request(f"INSERT INTO orders (id, order_id, status, userID, catID, amount) "
                     f"VALUES((SELECT COUNT(id) FROM orders)+1, "
                     f"'{order_id}', '0', '{user_id}', '{cat_id}', {amount})")

    choose_command(user)


def change_amount(order_id, user):
    print('Введите название товара из перечисленных ниже:')
    a = owner.db_request(f"SELECT name FROM catalog "
                         f"INNER JOIN orders ON orders.catID = catalog.id "
                         f"WHERE order_id = '{order_id}'")['data']
    tmp = str(str(a).replace(',', '').split()).replace('[', '').replace(']', '').replace('(', '').replace(')', '')
    item_list = tmp.replace('"', '').replace("'", '').split(sep=',')
    print(item_list)

    item = input()
    tmp = owner.db_request(f"SELECT id FROM catalog WHERE name = '{item}'")['data']
    cat_id = int(str(tmp)[2])
    if item in item_list:
        print('Введите новое количество:')
        amount = input()
        owner.db_request(f"UPDATE orders SET amount = {amount} WHERE order_id = {order_id} AND catID = '{cat_id}'")
        return choose_command(user)
    else:
        print('В списке заказанных вами такого товара нет, повторите ввод.')
        return change_amount(order_id, user)


def delete_order(order_id, user):
    owner.db_request(f"DELETE FROM orders WHERE order_id = '{order_id}'")
    return choose_command(user)


def watch_items(user):
    owner.watch_items(user)
    choose_command(user)
