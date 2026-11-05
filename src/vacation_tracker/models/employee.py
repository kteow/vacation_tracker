from dataclasses import dataclass

@dataclass
class Employee:
    #поля идут в том же порядке, что и столбцы в таблице employees
    employee_id: int
    name: str
    surname: str
    patronymic: str | None      #отчества может не быть, тогда здесь будет None
    login: str
    password_hash: str
    position: str
    user_role_id: int
    department_id: int
    #дополнительные поля: в базе их нет, в них мы потом положим названия вместо номеров
    role_name: str | None = None
    department_name: str | None = None