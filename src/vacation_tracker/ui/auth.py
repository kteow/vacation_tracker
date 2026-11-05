from services import auth_service, reference_service
from services.auth_service import EMPLOYEE_ROLE_ID
from ui.helpers import input_int

def login():
    login_value = input("Логин: ")
    password_value = input("Пароль: ")
    user = auth_service.authenticate(login_value, password_value)
    if not user:
        print("Неверный логин или пароль")
        return None
    return user

def register(by_admin=False):
    # by_admin=True: сотрудника добавляет администратор и сам выбирает роль
    print("\n--- Добавление сотрудника ---" if by_admin else "\n--- Регистрация ---")
    name = input("Имя: ")
    surname = input("Фамилия: ")
    patronymic = input("Отчество (можно оставить пустым): ")
    login_value = input("Логин: ")
    password = input("Пароль (не короче 6 символов): ")
    position = input("Должность: ")

    departments = reference_service.get_departments()
    for d in departments:
        print(f"{d.department_id}. {d.name}")
    department_id = input_int("Номер подразделения: ")
    if department_id not in [d.department_id for d in departments]:
        print("Такого подразделения нет")
        return

    role_id = EMPLOYEE_ROLE_ID          # при обычной регистрации всегда сотрудник
    if by_admin:
        print("1. Администратор")
        print("2. Сотрудник")
        role_id = input_int("Номер роли: ")

    try:
        auth_service.register_employee(name, surname, patronymic, login_value,
                                       password, position, department_id, role_id)
        print("Сотрудник добавлен" if by_admin else "Регистрация прошла успешно, теперь войдите в систему")
    except Exception as e:
        print("Ошибка:", e)