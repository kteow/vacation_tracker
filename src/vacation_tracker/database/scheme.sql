-- Схема базы данных "Учёт отпусков сотрудников"

-- Сначала удаляем таблицы (сначала те, что ссылаются на другие),
-- чтобы файл можно было запускать много раз
DROP TABLE IF EXISTS vacation_requests;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS request_statuses;
DROP TABLE IF EXISTS vacation_types;
DROP TABLE IF EXISTS departments;

-- Роли пользователей (Администратор, Сотрудник)
CREATE TABLE user_roles (
    user_role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Подразделения организации
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Виды отпусков (Ежегодный, Учебный и т.д.)
CREATE TABLE vacation_types (
    vacation_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_name TEXT NOT NULL UNIQUE
);

-- Статусы заявок (На рассмотрении, Одобрена, Отклонена)
CREATE TABLE request_statuses (
    request_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL UNIQUE
);

-- Сотрудники (они же пользователи системы, у каждого есть логин и роль)
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,                 -- отчества может не быть
    login TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,     -- пароль хранится в виде хеша, а не открытым текстом
    position TEXT NOT NULL,          -- должность
    user_role_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (user_role_id) REFERENCES user_roles (user_role_id),
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
);

-- Заявки на отпуск
CREATE TABLE vacation_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    vacation_type_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,        -- дата начала (ГГГГ-ММ-ДД)
    duration_days INTEGER NOT NULL,  -- продолжительность в днях
    request_status INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
    FOREIGN KEY (vacation_type_id) REFERENCES vacation_types (vacation_type_id),
    FOREIGN KEY (request_status) REFERENCES request_statuses (request_status_id)
);

-- Тестовые данные (сначала справочники, потом остальное)
INSERT INTO user_roles (name) VALUES
    ('Администратор'),
    ('Сотрудник');

INSERT INTO departments (name) VALUES
    ('Отдел кадров'),
    ('Бухгалтерия'),
    ('IT-отдел');

INSERT INTO vacation_types (type_name) VALUES
    ('Ежегодный оплачиваемый'),
    ('Учебный'),
    ('За свой счёт');

INSERT INTO request_statuses (status) VALUES
    ('На рассмотрении'),
    ('Одобрена'),
    ('Отклонена');


INSERT INTO vacation_requests (employee_id, vacation_type_id, start_date, duration_days, request_status) VALUES
    (2, 1, '2026-07-01', 14, 2),
    (3, 1, '2026-08-03', 21, 2),
    (4, 1, '2026-12-21', 10, 1),
    (5, 3, '2026-10-26', 5, 3),
    (4, 2, '2026-11-02', 14, 2);
