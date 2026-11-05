from services import vacation_request_service

def input_int(text):
    # спрашиваем число, пока пользователь не введёт его правильно
    while True:
        value = input(text)
        if value.isdigit():
            return int(value)
        print("Нужно ввести число")

def print_requests(requests):
    # список заявок со статусами
    if not requests:
        print("Заявок нет")
        return
    for r in requests:
        print(f"№{r.request_id} | {r.employee_full_name} | {r.type_name} | "
              f"с {r.start_date} на {r.duration_days} дн. | {r.status_name}")

def print_schedule(requests):
    # график отпусков: с датой начала и датой окончания
    if not requests:
        print("Одобренных отпусков нет")
        return
    for r in requests:
        end = vacation_request_service.get_end_date(r.start_date, r.duration_days)
        print(f"{r.employee_full_name} | {r.type_name} | "
              f"{r.start_date} — {end} ({r.duration_days} дн.)")