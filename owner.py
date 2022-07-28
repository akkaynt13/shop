import sqlite3
status = [
    '1. Создан',
    '2. Оплачен',
    '3. Отправлен',
    '4. Доставлен',
]


def change_price():
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute("SELECT * FROM catalog")
        a = c.fetchall()

    col_names = [description[0] for description in c.description]
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

    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute(f"UPDATE catalog SET price = {price} WHERE id = {inp}")
        db.commit()
    choose_command()


def change_quan():
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute("SELECT * FROM catalog")
        a = c.fetchall()

    col_names = [description[0] for description in c.description]
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

    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute(f"UPDATE catalog SET amount = {amount} WHERE id = {inp}")
        db.commit()
    choose_command()


def non_payed_orders():
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute("SELECT * FROM orders WHERE status < 4")
        a = c.fetchall()
        print(*a, sep='\n')
    choose_command()


def change_order_status():
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute("SELECT id,* FROM orders GROUP BY id")
        a = c.fetchall()
    print(*a, sep='\n')
    print('Введите номер заказа:')
    inp = input()
    if_order = False
    for data in a:
        if inp in str(data[0]):
            print('Чтобы установить новый номер заказа, выберите его номер в списке:')
            print(*status, sep='\n')
            st_id = input()
            if_order = True
    if not if_order:
            print('Заказа с таким номером в базе нет, проверьте введенный номер и повторите попытку.')
            return change_order_status()
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute(f"UPDATE orders SET status = {st_id} WHERE id = {inp}")
        db.commit()
    choose_command()


def watch_items():
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute("SELECT name, price, amount FROM catalog")
        print('Наименование, Цена, Количество')
        print(*c.fetchall(), sep='\n')
    if __name__ == '__main__':
        choose_command()


def choose_command():
    commands = {
        'watch_items()': '0. Просмотреть каталог',
        'change_price()': '1. Изменить цену товара',
        'change_quan()': '2. Изменить количество товара',
        'non_payed_orders()': '3. Посмотреть открытые заказы',
        'change_order_status()': '4. Изменить статус заказа'
    }

    print('\nВведите номер команды.')
    print(*commands.values(), sep='\n')
    command = input()
    if int(command) in range(len(list(commands.keys()))):
        return eval(list(commands.keys())[int(command)])
    else:
        print('Команды с таким номером нет, поробуйте еще раз.')
        return choose_command()
