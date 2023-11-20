import os
import sys

import handler_db
from valid_email import check

login_bool: bool = False
login: str = ""


def registration() -> None:
    """Registrate user for using program"""
    while True:
        os.system('clear')
        print("Введите ваш логин")
        user_login: str = input("< ")
        print("Введите ваш пароль")
        user_password: str = input("< ")
        print("Введите ваш email")
        user_email: str = input("< ")
        print("Если все данные верные, то напишите Y-N")
        ready: str = input("< ")
        if ready == "Y" and user_login and user_password and check(user_email):
            handler_db.create_user(user_login, user_password, user_email)
            break


def authorization() -> None:
    """Authentication for users"""
    while True:
        os.system('clear')
        print("Введите ваш логин")
        user_login: str = input("< ")
        print("Введите ваш пароль")
        user_password: str = input("< ")

        if handler_db.valid_user(user_login, user_password):
            global login
            global login_bool
            login: str = user_login
            login_bool: bool = True
            break


def main_menu() -> None:
    """Main menu for users"""
    global login
    global login_bool
    while True:
        os.system('clear')
        print("Меню")
        if not login_bool:
            print("1. Регистрация")
            print("2. Авторизация")

            choice: int = int(input("< "))

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
            print("5. Запросить баланс(доходы + расходы)")
            print("6. Вывод всех записей")
            print("7. Вывести определенную категорию")
            print("20. Выход")

            choice_2: int = int(input("< "))

            match choice_2:
                case 1:
                    print("Введите название категории")
                    category_name: str = input("< ")
                    print("Введите стоимость(доход или расход)")
                    cost: int = int(input("< "))
                    owner: int = handler_db.get_id_user(login=login)
                    handler_db.create_note(category_name=category_name, cost=cost, owner=owner)
                    print("Запись успешно добавлена")

                case 2:
                    print("Введите id для изменения записи")
                    note_id: int = int(input("< "))
                    print("Введите название категории")
                    category_name: str = input("< ")
                    print("Введите стоимость(доход или расход)")
                    note_cost: int = int(input("< "))
                    note_owner: int = handler_db.get_id_user(login=login)
                    handler_db.change_note(note_id=note_id, category_name=category_name,
                                           cost=note_cost, owner=note_owner)
                    print("Запись успешно обновлена")

                case 3:
                    print("Введите id для удаления записи")
                    note_id: int = int(input("< "))
                    handler_db.delete_note(note_id=note_id)
                    print("Запись успешно удалена")

                case 4:
                    print("Введите новый пароль")
                    new_password: str = input("< ")
                    handler_db.set_password(login=login, password=new_password)
                    print("Пароль успешно изменен")

                case 5:
                    user_balance: int = handler_db.get_balance(login)
                    print("На данный ваши доходы и расходы суммарно равны: ", user_balance)
                    pause = input()  # wait while user press enter

                case 6:
                    user_id: int = handler_db.get_id_user(login)
                    all_notes = handler_db.select_all(user_id)
                    for note in all_notes:
                        print("id: ", note.id, note.category_name)
                        print(note.cost)
                        print(note.created_at)
                        print("")
                    pause = input()  # wait while user press enter

                case 7:
                    user_id: int = handler_db.get_id_user(login)
                    all_notes = handler_db.select_all(user_id)
                    print("Напишите выбранную категорию")
                    for note in all_notes:
                        print(note.category_name)

                    print("\n")
                    category = input()
                    notes_from_category = handler_db.select_all_from_category(user_id, category)
                    for note in notes_from_category:
                        print("id: ", note.id, note.category_name)
                        print(note.cost)
                        print(note.created_at)
                        print("")
                    pause = input()  # wait while user press enter

                case 20:
                    sys.exit()


main_menu()
