import csv


def read_rows(paths):
    '''
    Считывает строки из списка CSV файлов и возвращает их как список словарей
    '''
    rows = []
    for p in paths:
        with open(p, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            rows.extend(reader)
    return rows
