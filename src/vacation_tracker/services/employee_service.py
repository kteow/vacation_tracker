from repositories import employee_repository, vacation_request_repository

def get_all_employees():
    return employee_repository.get_all()

def get_employee(employee_id):
    # нужна для меню "Учёт отпусков сотрудника"
    employee = employee_repository.get_by_id(employee_id)
    if not employee:
        raise Exception("Сотрудник не найден")
    return employee

def update_employee(employee_id, name, surname, patronymic, position, department_id):
    if not employee_repository.get_by_id(employee_id):
        raise Exception("Сотрудник не найден")
    if not name.strip() or not surname.strip() or not position.strip():
        raise Exception("Имя, фамилия и должность не могут быть пустыми")
    employee_repository.update(
        employee_id, name.strip(), surname.strip(),
        patronymic.strip() or None, position.strip(), department_id
    )

def delete_employee(employee_id):
    if not employee_repository.get_by_id(employee_id):
        raise Exception("Сотрудник не найден")
    # нельзя удалить сотрудника, у которого есть заявки (иначе будет ошибка базы)
    if vacation_request_repository.get_by_employee(employee_id):
        raise Exception("Нельзя удалить сотрудника, у которого есть заявки")
    employee_repository.delete(employee_id)