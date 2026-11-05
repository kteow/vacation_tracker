import os
from services import vacation_request_service, employee_service

# папка reports появится рядом с папкой services
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_FOLDER = os.path.join(BASE_FOLDER, "reports")

def employee_report(employee):
    # отчёт по одному сотруднику: его одобренные отпуска и сумма дней
    approved = vacation_request_service.get_approved_by_employee(employee.employee_id)
    lines = [
        f"Отчёт по отпускам: {employee.surname} {employee.name}",
        f"Должность: {employee.position}",
        ""
    ]
    total = 0
    for r in approved:
        end = vacation_request_service.get_end_date(r.start_date, r.duration_days)
        lines.append(f"{r.type_name}: {r.start_date} - {end} ({r.duration_days} дн.)")
        total = total + r.duration_days
    lines.append("")
    lines.append(f"Всего дней отпуска: {total}")
    return "\n".join(lines)   # склеиваем строки в один текст

def general_report():
    # общий отчёт по всем сотрудникам
    lines = ["Общий отчёт по отпускам", ""]
    for e in employee_service.get_all_employees():
        approved = vacation_request_service.get_approved_by_employee(e.employee_id)
        total = 0
        for r in approved:
            total = total + r.duration_days
        lines.append(f"{e.surname} {e.name} ({e.department_name}): "
                     f"отпусков {len(approved)}, дней {total}")
    return "\n".join(lines)

def save_report(text, file_name):
    os.makedirs(REPORTS_FOLDER, exist_ok=True)   # создаём папку, если её нет
    path = os.path.join(REPORTS_FOLDER, file_name)
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)
    return path