from services import vacation_request_service, reference_service
from ui.helpers import input_int, print_requests, print_schedule

def employee_menu(user):
    while True:
        print(f"\n===== Сотрудник: {user.surname} {user.name} =====")
        print("1. Личные данные и история отпусков")
        print("2. Создать заявку на отпуск")
        print("3. Статус моих заявок")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            show_personal_data(user)
        elif choice == "2":
            new_request(user)
        elif choice == "3":
            print_requests(vacation_request_service.get_my_requests(user.employee_id))
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")

def show_personal_data(user):
    full_name = f"{user.surname} {user.name} {user.patronymic or ''}"
    print("\n--- Личные данные ---")
    print("ФИО:", full_name.strip())
    print("Логин:", user.login)
    print("Должность:", user.position)
    print("Подразделение:", user.department_name)
    print("Роль:", user.role_name)
    print("\n--- История моих отпусков ---")
    print_schedule(vacation_request_service.get_approved_by_employee(user.employee_id))

def new_request(user):
    # перед созданием заявки показываем общий график отпусков
    print("\n--- График отпусков ---")
    print_schedule(vacation_request_service.get_approved())

    while True:
        print()
        for t in reference_service.get_vacation_types():
            print(f"{t.vacation_type_id}. {t.type_name}")
        type_id = input_int("Номер вида отпуска: ")
        start_date = input("Дата начала (ГГГГ-ММ-ДД): ")
        days = input_int("Сколько дней: ")
        try:
            vacation_request_service.create_request(user.employee_id, type_id,
                                                    start_date, days)
            print("Заявка сохранена, она ожидает рассмотрения")
            break                              # данные верные, выходим
        except Exception as e:
            print("Ошибка:", e)
            again = input("Повторить ввод? (д/н): ")
            if again.lower() != "д":
                break