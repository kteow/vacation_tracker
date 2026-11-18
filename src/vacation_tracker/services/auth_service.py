from repositories import (employee_repository, user_role_repository,
                          department_repository)
from services.password_service import hash_password, check_password
from constants import (ADMIN_ROLE_ID, EMPLOYEE_ROLE_ID, MIN_PASSWORD_LENGTH,
                       DEFAULT_ADMIN_LOGIN, DEFAULT_ADMIN_PASSWORD)

def authenticate(login, password):
    # ищем сотрудника по логину
    user = employee_repository.get_by_login(login)
    # если не нашли или пароль не подошёл, возвращаем None
    if not user or not check_password(password, user.password_hash):
        return None
    return user

def register_employee(name, surname, patronymic, login, password,
                      position, department_id, role_id=EMPLOYEE_ROLE_ID):
    if not name.strip():
        raise Exception("Имя не может быть пустым")
    if not surname.strip():
        raise Exception("Фамилия не может быть пустой")
    if not login.strip():
        raise Exception("Логин не может быть пустым")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise Exception(f"Пароль должен быть не короче {MIN_PASSWORD_LENGTH} символов")
    if not position.strip():
        raise Exception("Должность не может быть пустой")
    if role_id not in (ADMIN_ROLE_ID, EMPLOYEE_ROLE_ID):
        raise Exception("Такой роли нет")
    if employee_repository.get_by_login(login):
        raise Exception("Такой логин уже занят")

    patronymic = patronymic.strip() or None

    employee_repository.create(
        name.strip(), surname.strip(), patronymic, login.strip(),
        hash_password(password),    # в базу попадает только хеш с солью
        position.strip(), role_id, department_id
    )

def create_default_admin():
    # вызывается при запуске программы: гарантирует, что в системе есть администратор

    # если справочники пустые, заполняем их (без них нельзя создать сотрудника)
    if not user_role_repository.get_all():
        user_role_repository.create("Администратор")
        user_role_repository.create("Сотрудник")
    if not department_repository.get_all():
        department_repository.create("Отдел кадров")

    # если администратор уже есть, ничего не делаем
    if employee_repository.get_by_login(DEFAULT_ADMIN_LOGIN):
        return

    department = department_repository.get_all()[0]
    employee_repository.create(
        "Админ", "Системный", None, DEFAULT_ADMIN_LOGIN,
        hash_password(DEFAULT_ADMIN_PASSWORD),
        "Администратор", ADMIN_ROLE_ID, department.department_id
    )