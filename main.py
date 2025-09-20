from student_performance.cli import build_parser
from student_performance.io import read_rows
from student_performance.table import render_table
from student_performance.registry import get_report


def main():
    '''Обрабатывает аргументы, формирует отчёт и выводит таблицу'''
    parser = build_parser()
    args = parser.parse_args()
    rows = read_rows(args.files)
    headers, data = get_report(args.report)(rows)
    print(render_table(headers, data))


if __name__ == '__main__':
    main()
