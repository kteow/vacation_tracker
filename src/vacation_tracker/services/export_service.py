import os
import json
import csv
import xml.etree.ElementTree as ET   # встроенный модуль для работы с XML
import yaml                          # библиотека PyYAML

from repositories import employee_repository
from constants import (OUT_FOLDER, OUT_FILE_NAME, NESTED_SEPARATOR,
                       EXPORT_ROOT_TAG, EXPORT_ITEM_TAG)

def build_records(rows):
    # превращаем плоские строки в записи с вложенными объектами:
    # {"department__name": "IT"} -> {"department": {"name": "IT"}}
    records = []
    for row in rows:
        record = {}
        for key, value in row.items():
            if NESTED_SEPARATOR in key:
                group, field = key.split(NESTED_SEPARATOR, 1)
                if group not in record:
                    record[group] = {}      # создаём вложенный объект
                record[group][field] = value
            else:
                record[key] = value
        records.append(record)
    return records

def flatten(record):
    # для CSV: вложенный объект разворачиваем в обычные столбцы
    # {"department": {"name": "IT"}} -> {"department_name": "IT"}
    flat = {}
    for key, value in record.items():
        if isinstance(value, dict):
            for inner_key, inner_value in value.items():
                flat[key + "_" + inner_key] = inner_value
        else:
            flat[key] = value
    return flat

def add_to_xml(parent, data):
    # рекурсивно добавляем данные в XML: словарь становится вложенными тегами
    for key, value in data.items():
        child = ET.SubElement(parent, key)
        if isinstance(value, dict):
            add_to_xml(child, value)
        else:
            child.text = "" if value is None else str(value)

def save_json(records, path):
    with open(path, "w", encoding="utf-8") as file:
        # ensure_ascii=False оставляет русские буквы читаемыми, indent делает отступы
        json.dump(records, file, ensure_ascii=False, indent=4)

def save_csv(records, path):
    rows = [flatten(r) for r in records]
    # utf-8-sig нужен, чтобы Excel правильно показывал русские буквы
    with open(path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()        # первая строка с названиями столбцов
        writer.writerows(rows)

def save_xml(records, path):
    root = ET.Element(EXPORT_ROOT_TAG)             # корневой тег
    for record in records:
        item = ET.SubElement(root, EXPORT_ITEM_TAG)
        add_to_xml(item, record)
    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")                 # красивые отступы
    tree.write(path, encoding="utf-8", xml_declaration=True)

def save_yaml(records, path):
    with open(path, "w", encoding="utf-8") as file:
        # allow_unicode оставляет русские буквы, sort_keys=False сохраняет порядок полей
        yaml.dump(records, file, allow_unicode=True, sort_keys=False)

def export_all():
    rows = employee_repository.get_export_rows()
    if not rows:
        raise Exception("Нет данных для экспорта")

    records = build_records(rows)
    os.makedirs(OUT_FOLDER, exist_ok=True)         # создаём папку out, если её нет

    paths = {
        "json": os.path.join(OUT_FOLDER, OUT_FILE_NAME + ".json"),
        "csv": os.path.join(OUT_FOLDER, OUT_FILE_NAME + ".csv"),
        "xml": os.path.join(OUT_FOLDER, OUT_FILE_NAME + ".xml"),
        "yaml": os.path.join(OUT_FOLDER, OUT_FILE_NAME + ".yaml"),
    }
    save_json(records, paths["json"])
    save_csv(records, paths["csv"])
    save_xml(records, paths["xml"])
    save_yaml(records, paths["yaml"])
    return list(paths.values())