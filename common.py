import owner
import client
import sqlite3
admin_log_pass = ['admin', '123']


class Order:
    def __init__(self, status, contains):
        self.status = status
        self.contains = contains

    def change_status(self, status):
        self.status = status

    def show_status(self):
        if self.status == 0:
            return 'Created'
        elif self.status == 1:
            return 'Payed'
        elif self.status == 2:
            return 'Sent'
        elif self.status == 3:
            return 'Finished'


def watch_items():
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        c.execute("SELECT name, price, amount FROM catalog")
        print('Наименование, Цена, Количество')
        print(*c.fetchall(), sep='\n')


def registration():
    with sqlite3.connect('shop.db') as db:
        c = db.cursor()
        print('Введите логин:')
        login = input()
        c.execute("SELECT login FROM users")
        a = c.fetchall()

        for user in a:
            if login in user[0]:
                print('Этот логин уже занят, пожалуйста выберите другой.')
                return registration()

        print('Введите пароль:')
        password = input()
        c.execute(f"INSERT INTO users VALUES('{len(a)+1}','{login}', '{password}')")
        db.commit()


def autorization():
    print('Введите ваш логин. Чтобы зарегистрироваться, введите "r".')
    inp = input()
    # Регистрация
    if inp.lower() == 'r':
        return registration()

    # Авторизация админа
    elif inp == admin_log_pass[0]:
        print('Введите пароль:')
        if input() == admin_log_pass[1]:
            admin = owner.Owner()
            return main(admin)
        else:
            print('Вы ввели неверный пароль, пожалуйста повторите ввод данных.')
            return autorization()

    # Авторизация клиентов
    else:
        with sqlite3.connect('shop.db') as db:
            c = db.cursor()
            c.execute("SELECT login,pass FROM users")
            a = c.fetchall()
            if_login_in_file = False

            for data in a:
                if inp in data[0]:
                    if_login_in_file = True
                    print('Введите пароль:')
                    if input() in data[1]:
                        user = client.Client(inp)
                        return main(user)
                    else:
                        print('Вы ввели неверныyй пароль, пожалуйста повторите ввод данных')
                        return autorization()

        # Ошибочный ввод
        if not if_login_in_file:
            print('Вы ввели неверные данные, пожалуйста повторите ввод')
            return autorization()


def intro():
    print('Добро пожаловать, вот наш каталог товаров:')
    watch_items()
    while True:
        print('Чтобы сделать заказ необходимо авторизоваться, чтобы авторизоваться, введите "y".')
        if input().lower() == 'y':
            return autorization()


def main(user):
    if type(user) == type(owner.Owner()):
        owner.choose_command()
    else:
        client.choose_command()



if __name__ == '__main__':
    intro()
