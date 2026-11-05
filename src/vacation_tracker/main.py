from ui.auth import login, register
from ui.admin_menu import admin_menu
from ui.employee_menu import employee_menu
from services.auth_service import ADMIN_ROLE_ID

def main():
    while True:
        print("\n===== Учёт отпусков сотрудников =====")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            user = login()
            if user:
                # в зависимости от роли открываем нужное меню
                if user.user_role_id == ADMIN_ROLE_ID:
                    admin_menu(user)
                else:
                    employee_menu(user)
        elif choice == "2":
            register()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Нет такого пункта")

# этот блок запускает программу, только если запустить именно main.py
if __name__ == "__main__":
    main()