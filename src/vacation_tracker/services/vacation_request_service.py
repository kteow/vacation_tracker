from datetime import datetime, timedelta   # для работы с датами
from repositories import vacation_request_repository, vacation_type_repository

STATUS_PENDING = 1    # номера статусов из таблицы request_statuses
STATUS_APPROVED = 2
STATUS_REJECTED = 3

def _parse_date(text):
    # превращаем текст "2026-12-21" в дату; если формат неверный, будет ошибка
    try:
        return datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise Exception("Дата должна быть в формате ГГГГ-ММ-ДД")

def create_request(employee_id, vacation_type_id, start_date, duration_days):
    if not vacation_type_repository.get_by_id(vacation_type_id):
        raise Exception("Такого вида отпуска нет")

    start = _parse_date(start_date)
    if duration_days <= 0:
        raise Exception("Продолжительность должна быть больше 0")

    end = start + timedelta(days=duration_days - 1)   # последний день отпуска

    # проверяем пересечение с другими заявками этого сотрудника
    for r in vacation_request_repository.get_by_employee(employee_id):
        if r.request_status == STATUS_REJECTED:
            continue                                   # отклонённые не считаем
        other_start = _parse_date(r.start_date)
        other_end = other_start + timedelta(days=r.duration_days - 1)
        # два периода пересекаются, если каждый начинается до конца другого
        if start <= other_end and other_start <= end:
            raise Exception("Эти даты пересекаются с другой вашей заявкой")

    vacation_request_repository.create(
        employee_id, vacation_type_id, start_date, duration_days
    )

def get_my_requests(employee_id):
    return vacation_request_repository.get_by_employee(employee_id)

def get_all_requests():
    return vacation_request_repository.get_all()

def _change_status(request_id, new_status):
    request = vacation_request_repository.get_by_id(request_id)
    if not request:
        raise Exception("Заявка не найдена")
    # решение принимается только по заявке, которая ещё на рассмотрении
    if request.request_status != STATUS_PENDING:
        raise Exception("Эта заявка уже обработана")
    vacation_request_repository.update_status(request_id, new_status)

def approve_request(request_id):
    _change_status(request_id, STATUS_APPROVED)

def reject_request(request_id):
    _change_status(request_id, STATUS_REJECTED)

def cancel_request(request_id, employee_id):
    request = vacation_request_repository.get_by_id(request_id)
    # сотрудник может удалить только свою заявку
    if not request or request.employee_id != employee_id:
        raise Exception("Заявка не найдена")
    if request.request_status != STATUS_PENDING:
        raise Exception("Можно отменить только заявку на рассмотрении")
    vacation_request_repository.delete(request_id)

def get_approved():
    # все одобренные заявки (общий график отпусков)
    result = []
    for r in vacation_request_repository.get_all():
        if r.request_status == STATUS_APPROVED:
            result.append(r)
    return result

def get_approved_by_employee(employee_id):
    # одобренные заявки одного сотрудника
    result = []
    for r in vacation_request_repository.get_by_employee(employee_id):
        if r.request_status == STATUS_APPROVED:
            result.append(r)
    return result

def get_end_date(start_date, duration_days):
    # считаем последний день отпуска и возвращаем текстом ГГГГ-ММ-ДД
    start = _parse_date(start_date)
    end = start + timedelta(days=duration_days - 1)
    return end.strftime("%Y-%m-%d")