import os
import sys
from validEmail import check
import handler_db

login_bool = False
login = ""

def registration():
    while True:
        os.system('clear')
        print("Введите ваш логин")
        user_login = input("< ")
        print("Введите ваш пароль")
        user_password = input("< ")
        print("Введите ваш email")
        user_email = input("< ")
        print("Если все данные верные, то напишите Y-N")
        ready = input("< ")
        if ready == "Y":
            if user_login and user_password and check(user_email):
                handler_db.createUser(user_login, user_password, user_email)
                break

def authorization():
    while True:
        os.system('clear')
        print("Введите ваш логин")
        user_login = input("< ")
        print("Введите ваш пароль")
        user_password = input("< ")

        if handler_db.validUser(user_login, user_password):
            global login
            global login_bool
            login = user_login
            login_bool = True
            break



def mainMenu():
    global login
    global login_bool
    while True:
        os.system('clear')
        print("Меню")
        if login_bool == False:
            print("1. Регистрация")
            print("2. Авторизация")

            choice = int(input("< "))

            match choice:
                case 1:
                    registration()
                
                case 2:
                    authorization()
                        
        else:
            print("1. Создание новой записи")
            print("2. Изменение записи")
            print("3. Удаление записи")
            print("4. Изменить пароль пользователя")
            print("5. Установить значение баланса")
            print("6. Запросить баланс(доходы + расходы)")
            print("7. Вывод всех записей")
            print("8. Вывести определенную категорию")
            print("20. Выход")


            choice_2 = int(input("< "))

            match choice_2:
                case 1:
                    print("Введите название категории")
                    category_name = input("< ")
                    print("Введите стоимость(доход или расход)")
                    cost = int(input("< "))
                    owner = handler_db.getIdUser(login=login)
                    handler_db.createNote(category_name=category_name, cost=cost, owner=owner)
                    print("Запись успешно добавлена")
                    

                case 2:
                    print("Введите id для изменения записи")
                    id = int(input("< "))
                    print("Введите название категории")
                    category_name = input("< ")
                    print("Введите стоимость(доход или расход)")
                    cost = int(input("< "))
                    owner = handler_db.getIdUser(login=login)
                    handler_db.changeNote(id=id, category_name=category_name, cost=cost, owner=owner)
                    print("Запись успешно обновлена")
                    
                
                case 3:
                    print("Введите id для удаления записи")
                    id = int(input("< "))
                    handler_db.deleteNote(id=id)
                    print("Запись успешно удалена")
                    
                
                case 4:
                    print("Введите новый пароль")
                    password = input("< ")
                    handler_db.setPassword(login=login, password=password)
                    print("Пароль успешно изменен")
                
                case 5:
                    print("Введите начальное количество денежных средств")
                    money = int(input("< "))
                    handler_db.setMoney(money, login)
                
                case 6:

                    money = handler_db.getBalance(login)
                    print("На данный ваши доходы и расходы суммарно равны: ", money)
                    pause = input()

                case 7:

                    id = handler_db.getIdUser(login)
                    result = handler_db.selectAll(id)
                    for i in result:
                        
                        print("id: ", i.id, i.category_name)
                        print(i.cost)
                        print(i.created_at)
                        print("")
                    pause = input()

                case 8:
                    id = handler_db.getIdUser(login)
                    res = handler_db.selectAll(id)
                    print("Напишите выбранную категорию")
                    for i in res:
                       print(i.category_name)

                    print("\n")
                    category = input()
                    res = handler_db.selectAllFromCategory(id, category)
                    for i in res:
                        
                        print("id: ", i.id, i.category_name)
                        print(i.cost)
                        print(i.created_at)
                        print("")
                    pause = input()

                case 20:
                    sys.exit()

mainMenu()






    

    
