from services import (employee_service, vacation_request_service,
                      reference_service, report_service)
from ui.auth import register
from ui.helpers import input_int, print_requests, print_schedule

def admin_menu(user):
    while True:
        print(f"\n===== Администратор: {user.surname} {user.name} =====")
        print("1. Меню заявок")
        print("2. Меню отпусков")
        print("3. Меню сотрудников")
        print("4. Формирование отчётов")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            requests_menu()
        elif choice == "2":
            vacations_menu()
        elif choice == "3":
            employees_menu(user)
        elif choice == "4":
            make_general_report()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")

# ---------- Меню заявок ----------

def requests_menu():
    while True:
        print("\n--- Меню заявок ---")
        print("1. Просмотр всех заявок")
        print("2. Обработка заявок (подтвердить / отклонить)")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            print_requests(vacation_request_service.get_all_requests())
        elif choice == "2":
            process_requests()
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")

def process_requests():
    # собираем заявки на рассмотрении (статус 1)
    pending = []
    for r in vacation_request_service.get_all_requests():
        if r.request_status == 1:
            pending.append(r)
    if not pending:
        print("Заявок на рассмотрении нет")
        return

    print_requests(pending)
    request_id = input_int("Номер заявки (0 - назад): ")
    if request_id == 0:
        return

    print("1. Подтвердить")
    print("2. Отклонить")
    decision = input("Решение: ")
    try:
        if decision == "1":
            vacation_request_service.approve_request(request_id)
            print("Заявка одобрена")
        elif decision == "2":
            vacation_request_service.reject_request(request_id)
            print("Заявка отклонена")
        else:
            print("Нет такого пункта")
    except Exception as e:
        print("Ошибка:", e)

# ---------- Меню отпусков ----------

def vacations_menu():
    while True:
        print("\n--- Меню отпусков ---")
        print("1. Учёт отпусков сотрудника")
        print("2. График отпусков")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            vacation_accounting()
        elif choice == "2":
            print("\n--- Общий график отпусков ---")
            print_schedule(vacation_request_service.get_approved())
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")

def vacation_accounting():
    # выбор сотрудника, проверка одобренных заявок, история, отчёт
    show_employees()
    employee_id = input_int("Номер сотрудника: ")
    try:
        employee = employee_service.get_employee(employee_id)
    except Exception as e:
        print("Ошибка:", e)
        return

    approved = vacation_request_service.get_approved_by_employee(employee_id)
    if not approved:
        print("Одобренных заявок нет")
    else:
        total = 0
        for r in approved:
            total = total + r.duration_days
        print(f"В учёт внесено отпусков: {len(approved)}, всего дней: {total}")

    print("\n--- История отпусков ---")
    print_requests(vacation_request_service.get_my_requests(employee_id))

    answer = input("Сформировать отчёт? (д/н): ")
    if answer.lower() == "д":
        text = report_service.employee_report(employee)
        print("\n" + text)
        path = report_service.save_report(text, f"report_{employee.employee_id}.txt")
        print("Отчёт сохранён:", path)

# ---------- Меню сотрудников ----------

def employees_menu(user):
    while True:
        print("\n--- Меню сотрудников ---")
        print("1. Список сотрудников")
        print("2. Добавить сотрудника")
        print("3. Изменить данные сотрудника")
        print("4. Удалить сотрудника")
        print("0. Назад")
        choice = input("Выберите действие: ")

        if choice == "1":
            show_employees()
        elif choice == "2":
            register(by_admin=True)
        elif choice == "3":
            edit_employee()
        elif choice == "4":
            delete_employee(user)
        elif choice == "0":
            break
        else:
            print("Нет такого пункта")

def show_employees():
    for e in employee_service.get_all_employees():
        print(f"{e.employee_id}. {e.surname} {e.name} | {e.position} | "
              f"{e.department_name} | {e.role_name}")

def edit_employee():
    employee_id = input_int("Номер сотрудника: ")
    name = input("Новое имя: ")
    surname = input("Новая фамилия: ")
    patronymic = input("Новое отчество (можно пустое): ")
    position = input("Новая должность: ")
    for d in reference_service.get_departments():
        print(f"{d.department_id}. {d.name}")
    department_id = input_int("Номер подразделения: ")
    try:
        employee_service.update_employee(employee_id, name, surname,
                                         patronymic, position, department_id)
        print("Данные изменены")
    except Exception as e:
        print("Ошибка:", e)

def delete_employee(user):
    employee_id = input_int("Номер сотрудника для удаления: ")
    if employee_id == user.employee_id:
        print("Нельзя удалить самого себя")
        return
    try:
        employee_service.delete_employee(employee_id)
        print("Сотрудник удалён")
    except Exception as e:
        print("Ошибка:", e)

# ---------- Отчёты ----------

def make_general_report():
    text = report_service.general_report()
    print("\n" + text)
    path = report_service.save_report(text, "general_report.txt")
    print("Отчёт сохранён:", path)