from dataclasses import dataclass

@dataclass
class VacationRequest:
    request_id: int
    employee_id: int
    vacation_type_id: int
    start_date: str             #даты хранятся текстом ГГГГ-ММ-ДД
    duration_days: int
    request_status: int         #здесь номер статуса (1, 2 или 3), как в таблице
    #дополнительные поля для красивого вывода в меню
    employee_full_name: str | None = None
    type_name: str | None = None
    status_name: str | None = None