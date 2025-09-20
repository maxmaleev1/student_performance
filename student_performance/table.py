from tabulate import tabulate


def _normalize_rows(headers, rows):
    '''
    Приводит строки к длине заголовков, чтобы tabulate не падал при ошибках
    или неполных данных в CSV-файле
    '''
    h = len(headers)
    out = []
    for r in rows:
        r = list(r)
        if len(r) >= h:
            out.append(r[:h])
        else:
            out.append(r + [''] * (h - len(r)))
    return out


def render_table(headers, rows):
    '''Формирует таблицу в формате psql с колонкой индекса'''
    if not headers:
        return ''
    rows = _normalize_rows(headers, rows)
    numbered = [(i, *r) for i, r in enumerate(rows, 1)]
    headers = ['#'] + list(headers)
    return tabulate(numbered, headers=headers, tablefmt='psql')
