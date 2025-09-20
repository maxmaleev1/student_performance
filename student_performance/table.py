def _simple_grid(headers, rows):
    '''Строит таблицу, если tabulate недоступен'''
    index_width = max(len(str(len(rows))), 1)
    widths = [len(h) for h in headers]

    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))

    def line(sep_left='+', sep_mid='+', sep_right='+', fill='-'):
        '''Создаёт горизонтальные линии таблицы'''
        parts = [fill * (index_width + 2)]
        for w in widths:
            parts.append(fill * (w + 2))
        return sep_left + sep_mid.join(parts) + sep_right

    def fmt_row(idx, r):
        '''Форматирует строку таблицы с индексом и данными'''
        cells = [f' {str(idx).rjust(index_width)} ']
        for i, cell in enumerate(r):
            cells.append(f' {str(cell).ljust(widths[i])} ')
        return '|' + '|'.join(cells) + '|'

    out = [line(), fmt_row('#', headers), line()]
    for i, r in enumerate(rows, 1):
        out.append(fmt_row(i, r))
    out.append(line())
    return '\n'.join(out)


def render_table(headers, rows):
    '''
    Возвращает таблицу через tabulate, если он доступен, иначе через
    _simple_grid
    '''
    try:
        from tabulate import tabulate
        return tabulate(
            rows,
            headers=headers,
            tablefmt='psql',
            showindex=range(1, len(rows) + 1),
        )
    except Exception:
        return _simple_grid(headers, rows)
