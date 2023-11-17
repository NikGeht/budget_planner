import os
from validEmail import check
import handler_db
os.system('clear')
login_bool = False
login = ""
def mainMenu():

    print("Меню")
    if login_bool == False:
        print("1. Регистрация")
        print("2. Авторизация")

        choice = input("< ")

        match choice:
            case 1:
                while True:
                    print("Введите ваш логин")
                    user_login = input("< ")
                    print("Введите ваш пароль")
                    user_password = input("< ")
                    print("Введите ваш email")
                    user_email = input("< ")
                    print("Если все данные верные, то напишите Y\N")
                    ready = input("< ")
                    if ready == "Y":
                        if user_login and user_password and check(user_email):

                            break
                    else:
                        pass
            
            case 2:
                while True:
                    print("Введите ваш логин")
                    user_login = input("< ")
                    print("Введите ваш пароль")
                    user_password = input("< ")

                    if handler_db.validUser(user_login, user_password):
                        global login
                        login = user_login
                        login_bool = True
                        break
                    else:
                        pass
    else:
        print("1. Создание новой записи")
        print("2. Изменение записи")
        print("3. Удаление записи")
        print("4. Изменить пароль пользователя")
        print("5. Установить значение баланса")
        print("6. Запросить баланс(доходы + расходы)")
        print("7. Вывод всех записей")
        print("8. Вывести определенную категорию")


        choice = input("< ")

        match choice:
            case 1:
                print

    

    
