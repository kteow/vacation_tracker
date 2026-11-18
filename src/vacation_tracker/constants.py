import os

# роли пользователей (номера из таблицы user_roles)
ADMIN_ROLE_ID = 1
EMPLOYEE_ROLE_ID = 2

# статусы заявок (номера из таблицы request_statuses)
STATUS_PENDING = 1      # на рассмотрении
STATUS_APPROVED = 2     # одобрена
STATUS_REJECTED = 3     # отклонена

# минимальная длина пароля
MIN_PASSWORD_LENGTH = 6

# администратор по умолчанию (создаётся при первом запуске программы)
DEFAULT_ADMIN_LOGIN = "admin"
DEFAULT_ADMIN_PASSWORD = "1234567890"

# ---------- экспорт данных (лабораторная 5) ----------

# корень проекта: поднимаемся на три папки вверх от этого файла
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_FOLDER = os.path.join(PROJECT_ROOT, "out")   # сюда сохраняются файлы

OUT_FILE_NAME = "data"            # data.json, data.csv, data.xml, data.yaml
NESTED_SEPARATOR = "__"           # department__name в запросе -> вложенный объект
EXPORT_ROOT_TAG = "employees"     # корневой тег в XML
EXPORT_ITEM_TAG = "employee"      # тег одной записи в XML