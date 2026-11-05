from dataclasses import dataclass  # сам создаёт конструктор класса

@dataclass
class UserRole:
    user_role_id: int
    name: str