-- Схема базы данных "Учёт отпусков сотрудников"

-- Сначала удаляем таблицы (сначала те, что ссылаются на другие),
-- чтобы скрипт можно было запускать много раз
DROP TABLE IF EXISTS vacations;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS vacation_statuses;
DROP TABLE IF EXISTS vacation_types;
DROP TABLE IF EXISTS departments;

-- Отделы компании
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Типы отпусков (ежегодный, учебный и т.д.)
CREATE TABLE vacation_types (
    vacation_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Статусы отпусков (запланирован, одобрен и т.д.)
CREATE TABLE vacation_statuses (
    vacation_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Сотрудники
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    patronymic TEXT,                 -- отчество может отсутствовать
    position TEXT NOT NULL,          -- должность
    hire_date TEXT NOT NULL,         -- дата приёма на работу (ГГГГ-ММ-ДД)
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
);

-- Отпуска сотрудников
CREATE TABLE vacations (
    vacation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    vacation_type_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,        -- начало отпуска (ГГГГ-ММ-ДД)
    end_date TEXT NOT NULL,          -- конец отпуска (ГГГГ-ММ-ДД)
    vacation_status_id INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
    FOREIGN KEY (vacation_type_id) REFERENCES vacation_types (vacation_type_id),
    FOREIGN KEY (vacation_status_id) REFERENCES vacation_statuses (vacation_status_id)
);

-- Тестовые данные (порядок важен: сначала справочники, потом остальное)
INSERT INTO departments (name) VALUES
    ('Бухгалтерия'),
    ('Отдел кадров'),
    ('IT-отдел');

INSERT INTO vacation_types (name) VALUES
    ('Ежегодный оплачиваемый'),
    ('Учебный'),
    ('За свой счёт');

INSERT INTO vacation_statuses (name) VALUES
    ('Запланирован'),
    ('Одобрен'),
    ('Отклонён'),
    ('Завершён');

INSERT INTO employees (name, surname, patronymic, position, hire_date, department_id) VALUES
    ('Анна', 'Иванова', 'Петровна', 'Бухгалтер', '2020-03-15', 1),
    ('Олег', 'Смирнов', 'Игоревич', 'Главный бухгалтер', '2018-09-01', 1),
    ('Мария', 'Кузнецова', NULL, 'Специалист по кадрам', '2022-01-10', 2),
    ('Дмитрий', 'Попов', 'Сергеевич', 'Программист', '2021-06-20', 3),
    ('Елена', 'Соколова', 'Андреевна', 'Системный администратор', '2019-11-05', 3);

INSERT INTO vacations (employee_id, vacation_type_id, start_date, end_date, vacation_status_id) VALUES
    (1, 1, '2026-07-01', '2026-07-14', 4),
    (2, 1, '2026-08-03', '2026-08-23', 4),
    (3, 2, '2026-11-02', '2026-11-15', 2),
    (4, 1, '2026-12-21', '2026-12-31', 1),
    (5, 3, '2026-10-26', '2026-10-30', 3),
    (4, 1, '2026-02-02', '2026-02-15', 4);
