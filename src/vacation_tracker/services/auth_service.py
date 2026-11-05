from repositories import employee_repository
from services.password_service import hash_password, check_password

ADMIN_ROLE_ID = 1      # номера ролей из таблицы user_roles
EMPLOYEE_ROLE_ID = 2

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
    if len(password) < 6:
        raise Exception("Пароль должен быть не короче 6 символов")
    if not position.strip():
        raise Exception("Должность не может быть пустой")
    if role_id not in (ADMIN_ROLE_ID, EMPLOYEE_ROLE_ID):
        raise Exception("Такой роли нет")
    if employee_repository.get_by_login(login):
        raise Exception("Такой логин уже занят")

    patronymic = patronymic.strip() or None

    employee_repository.create(
        name.strip(), surname.strip(), patronymic, login.strip(),
        hash_password(password),
        position.strip(), role_id, department_id
    )